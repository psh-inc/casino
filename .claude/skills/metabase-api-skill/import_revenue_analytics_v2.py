#!/usr/bin/env python3
"""
Import Revenue Analytics SQL Queries to Metabase - Version 2
Improved parsing and duplicate prevention
"""

import os
import sys
import re
from pathlib import Path
from metabase_helper import MetabaseClient, MetabaseError

# Metabase configuration
METABASE_URL = 'https://metabase-analytic-lroiw.ondigitalocean.app'
METABASE_USERNAME = 'kaxgel11@gmail.com'
METABASE_PASSWORD = 'cdv!kcq.EVT*qrz3nzj'

# Path to SQL files
SQL_DIR = Path(__file__).parent.parent.parent.parent / 'casino-b' / 'docs' / 'sql-reports' / 'revenue-analytics'

def parse_sql_file_v2(file_path):
    """
    Parse SQL file and extract individual queries with improved regex

    Returns:
        dict with file metadata and list of parsed queries
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract metric number and title from header
    metric_match = re.search(
        r'REVENUE ANALYTICS METRIC #(\d+):\s*(.+?)(?=\n--|\n\n)',
        content,
        re.IGNORECASE
    )

    if metric_match:
        metric_num = metric_match.group(1)
        metric_title = metric_match.group(2).strip()
    else:
        # Fallback to filename parsing
        filename = file_path.stem
        parts = filename.split('_', 1)
        metric_num = parts[0] if parts[0].isdigit() else None
        metric_title = ' '.join(parts[1:]).replace('_', ' ').title() if len(parts) > 1 else filename

    # Extract description
    desc_match = re.search(
        r'-- Description:\s*(.+?)(?=\n--\s*\n|-- Business)',
        content,
        re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""
    description = re.sub(r'\n--\s*', '\n', description).strip()

    # Extract business value
    business_match = re.search(
        r'-- Business Value:\s*(.+?)(?=\n--\s*\n|-- Data Source)',
        content,
        re.DOTALL
    )
    business_value = business_match.group(1).strip() if business_match else ""
    business_value = re.sub(r'\n--\s*', '\n', business_value).strip()

    # Combine into full description
    full_description = f"{description}"
    if business_value:
        full_description += f"\n\nBusiness Value: {business_value}"

    # Split queries - improved regex to handle WITH clauses and complex queries
    # Match "-- Query N: Title" followed by SQL until next query or end
    query_pattern = r'-- Query (\d+):\s*(.+?)\n((?:(?!-- Query \d+:).)+)'

    queries = []
    for match in re.finditer(query_pattern, content, re.DOTALL | re.IGNORECASE):
        query_num = match.group(1)
        query_title = match.group(2).strip()
        sql_block = match.group(3).strip()

        # Clean up the SQL - remove comment lines but keep the actual SQL
        sql_lines = []
        for line in sql_block.split('\n'):
            # Skip lines that are only comments
            if line.strip().startswith('--'):
                continue
            # Keep SQL lines
            if line.strip():
                sql_lines.append(line)

        sql_query = '\n'.join(sql_lines).strip()

        # Only add if we have actual SQL content
        if sql_query and any(keyword in sql_query.upper() for keyword in ['SELECT', 'WITH', 'INSERT', 'UPDATE']):
            queries.append({
                'number': query_num,
                'title': query_title,
                'sql': sql_query
            })

    return {
        'filename': file_path.name,
        'metric_num': metric_num,
        'metric_title': metric_title,
        'description': full_description,
        'queries': queries
    }

def main():
    print("=" * 80)
    print("Revenue Analytics SQL Import to Metabase (Version 2)")
    print("=" * 80)

    # Parse all SQL files first
    print("\n[1/6] Analyzing SQL files...")
    sql_files = sorted(SQL_DIR.glob('*.sql'))

    if not sql_files:
        print(f"✗ No SQL files found in: {SQL_DIR}")
        sys.exit(1)

    print(f"✓ Found {len(sql_files)} SQL file(s)\n")

    all_parsed_data = []
    total_queries = 0

    for sql_file in sql_files:
        print(f"  Analyzing: {sql_file.name}")
        parsed = parse_sql_file_v2(sql_file)
        all_parsed_data.append(parsed)

        print(f"    Metric #{parsed['metric_num']}: {parsed['metric_title']}")
        print(f"    Found {len(parsed['queries'])} queries:")
        for q in parsed['queries']:
            print(f"      - Query {q['number']}: {q['title'][:60]}...")
        print()

        total_queries += len(parsed['queries'])

    print(f"✓ Total queries to import: {total_queries}\n")

    # Connect to Metabase
    print("[2/6] Connecting to Metabase...")
    try:
        mb = MetabaseClient(
            base_url=METABASE_URL,
            username=METABASE_USERNAME,
            password=METABASE_PASSWORD
        )
        print("✓ Connected successfully!\n")
    except MetabaseError as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)

    # Get database
    print("[3/6] Fetching database information...")
    try:
        databases_response = mb.list_databases()
        databases = databases_response if isinstance(databases_response, list) else databases_response.get('data', [])

        print(f"✓ Found {len(databases)} database(s):")
        for db in databases:
            print(f"  - {db['name']} (ID: {db['id']})")

        # Find casinocore database or use first one
        target_db = next((db for db in databases if 'casino' in db['name'].lower()), databases[0] if databases else None)

        if not target_db:
            print("✗ No databases found")
            sys.exit(1)

        database_id = target_db['id']
        print(f"\n✓ Using database: {target_db['name']} (ID: {database_id})\n")
    except MetabaseError as e:
        print(f"✗ Failed to fetch databases: {e}")
        sys.exit(1)

    # Create or find collection
    print("[4/6] Setting up 'Revenue Analytics' collection...")
    try:
        collections = mb.list_collections()
        existing_collection = next(
            (c for c in collections if c['name'] == 'Revenue Analytics'),
            None
        )

        if existing_collection:
            collection_id = existing_collection['id']
            print(f"✓ Using existing collection (ID: {collection_id})\n")
        else:
            collection = mb.create_collection(
                name='Revenue Analytics',
                description='Casino revenue and gaming analytics metrics - Auto-generated from SQL files'
            )
            collection_id = collection['id']
            print(f"✓ Created new collection (ID: {collection_id})\n")
    except MetabaseError as e:
        print(f"! Warning: Could not create collection: {e}")
        print("  Continuing without collection...\n")
        collection_id = None

    # Check for existing cards to avoid duplicates
    print("[5/6] Checking for existing cards...")
    try:
        existing_cards = mb.list_cards()
        existing_card_names = {card['name'] for card in existing_cards}
        print(f"✓ Found {len(existing_cards)} existing cards in Metabase\n")
    except MetabaseError as e:
        print(f"! Warning: Could not list existing cards: {e}")
        existing_card_names = set()

    # Import queries
    print("[6/6] Importing queries to Metabase...")
    print("=" * 80)

    created_count = 0
    skipped_count = 0
    failed_count = 0

    for file_data in all_parsed_data:
        metric_num = file_data['metric_num']
        metric_title = file_data['metric_title']

        print(f"\n📊 Metric #{metric_num}: {metric_title}")
        print("-" * 80)

        for query in file_data['queries']:
            # Clean query title
            clean_title = query['title'].replace('\n', ' ').strip()
            clean_title = ' '.join(clean_title.split())

            # Build card name (max 200 chars)
            card_name = f"#{metric_num}.{query['number']} {metric_title} - {clean_title}"
            if len(card_name) > 200:
                card_name = card_name[:197] + "..."

            # Check if already exists
            if card_name in existing_card_names:
                print(f"  ⊘ Skipped (exists): {card_name}")
                skipped_count += 1
                continue

            # Build description
            card_desc = f"{file_data['description']}\n\n**Query:** {clean_title}"

            try:
                card = mb.create_card(
                    name=card_name,
                    sql_query=query['sql'],
                    database_id=database_id,
                    collection_id=collection_id,
                    description=card_desc,
                    display='table'
                )
                print(f"  ✓ Created: {card_name}")
                print(f"    → {METABASE_URL}/question/{card['id']}")
                created_count += 1
                existing_card_names.add(card_name)  # Add to set to prevent duplicates in same run

            except MetabaseError as e:
                print(f"  ✗ Failed: {card_name}")
                print(f"    Error: {str(e)[:200]}")
                failed_count += 1

    # Final summary
    print("\n" + "=" * 80)
    print("IMPORT SUMMARY")
    print("=" * 80)
    print(f"✓ Successfully created: {created_count} cards")
    if skipped_count > 0:
        print(f"⊘ Skipped (already exist): {skipped_count} cards")
    if failed_count > 0:
        print(f"✗ Failed: {failed_count} cards")
    print(f"\n📊 Total: {created_count + skipped_count + failed_count}/{total_queries} queries processed")

    if collection_id:
        print(f"\n🔗 View collection: {METABASE_URL}/collection/{collection_id}")

    print("=" * 80)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Import cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
