#!/usr/bin/env python3
"""
Import Revenue Analytics SQL Queries to Metabase
"""

import os
import sys
import re
from pathlib import Path
from metabase_helper import MetabaseClient, MetabaseError

# Metabase configuration
METABASE_URL = 'http://localhost:3000'
METABASE_USERNAME = 'kaxgel11@gmail.com'
METABASE_PASSWORD = 'dwrstn11'

# Path to SQL files
SQL_DIR = Path(__file__).parent.parent.parent.parent / 'casino-b' / 'docs' / 'sql-reports' / 'revenue-analytics'

def parse_sql_file(file_path):
    """
    Parse SQL file and extract metadata and individual queries

    Returns:
        dict with 'title', 'description', 'queries' (list of dicts with 'name' and 'sql')
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract metric number and title from header
    title_match = re.search(r'REVENUE ANALYTICS METRIC #(\d+): (.+)', content)
    if title_match:
        metric_num = title_match.group(1)
        title = title_match.group(2).strip()
    else:
        # Fallback to filename
        title = file_path.stem.replace('_', ' ').title()
        metric_num = None

    # Extract description
    desc_match = re.search(r'-- Description: (.+?)(?=\n--|\n\n)', content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract business value
    business_match = re.search(r'-- Business Value: (.+?)(?=\n--|\n\n)', content, re.DOTALL)
    business_value = business_match.group(1).strip() if business_match else ""

    # Combine description
    full_description = f"{description}\n\n{business_value}" if business_value else description

    # Split by individual queries (Query 1:, Query 2:, etc.)
    query_pattern = r'-- Query (\d+): (.+?)\n(SELECT.+?)(?=\n\n-- Query|\n\n$|$)'
    query_matches = re.findall(query_pattern, content, re.DOTALL | re.IGNORECASE)

    queries = []
    for query_num, query_title, sql_code in query_matches:
        queries.append({
            'number': query_num,
            'title': query_title.strip(),
            'sql': sql_code.strip()
        })

    return {
        'metric_num': metric_num,
        'title': title,
        'description': full_description,
        'queries': queries
    }

def main():
    print("=" * 80)
    print("Revenue Analytics SQL Import to Metabase")
    print("=" * 80)

    # Initialize client
    print("\n[1/5] Connecting to Metabase...")
    try:
        mb = MetabaseClient(
            base_url=METABASE_URL,
            username=METABASE_USERNAME,
            password=METABASE_PASSWORD
        )
        print("✓ Connected successfully!")
    except MetabaseError as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)

    # List databases
    print("\n[2/5] Fetching available databases...")
    try:
        databases_response = mb.list_databases()

        # Handle case where response might be wrapped in 'data' key
        if isinstance(databases_response, dict) and 'data' in databases_response:
            databases = databases_response['data']
        else:
            databases = databases_response

        # Ensure databases is a list
        if not isinstance(databases, list):
            print(f"✗ Unexpected database response format: {type(databases)}")
            print(f"  Response: {databases}")
            sys.exit(1)

        print(f"✓ Found {len(databases)} database(s):")
        for db in databases:
            print(f"  - {db['name']} (ID: {db['id']})")

        if not databases:
            print("✗ No databases found. Please add a database in Metabase first.")
            sys.exit(1)

        # Use the first database
        database_id = databases[0]['id']
        print(f"\nUsing database ID: {database_id}")
    except MetabaseError as e:
        print(f"✗ Failed to fetch databases: {e}")
        sys.exit(1)

    # Create collection
    print("\n[3/5] Creating 'Revenue Analytics' collection...")
    try:
        # Check if collection already exists
        collections = mb.list_collections()
        existing_collection = next(
            (c for c in collections if c['name'] == 'Revenue Analytics'),
            None
        )

        if existing_collection:
            collection_id = existing_collection['id']
            print(f"✓ Collection already exists (ID: {collection_id})")
        else:
            collection = mb.create_collection(
                name='Revenue Analytics',
                description='Casino revenue and gaming analytics metrics'
            )
            collection_id = collection['id']
            print(f"✓ Created collection (ID: {collection_id})")
    except MetabaseError as e:
        print(f"✗ Failed to create collection: {e}")
        print("  Continuing without collection...")
        collection_id = None

    # Find and parse SQL files
    print("\n[4/5] Parsing SQL files...")
    sql_files = sorted(SQL_DIR.glob('*.sql'))

    if not sql_files:
        print(f"✗ No SQL files found in: {SQL_DIR}")
        sys.exit(1)

    print(f"✓ Found {len(sql_files)} SQL file(s)")

    all_parsed_data = []
    for sql_file in sql_files:
        print(f"  - Parsing {sql_file.name}...")
        parsed = parse_sql_file(sql_file)
        all_parsed_data.append(parsed)
        print(f"    Found {len(parsed['queries'])} queries")

    # Import queries to Metabase
    print("\n[5/5] Importing queries to Metabase...")
    total_created = 0
    total_queries = sum(len(data['queries']) for data in all_parsed_data)

    print(f"  Creating {total_queries} card(s)...\n")

    for data in all_parsed_data:
        metric_num = data['metric_num']
        metric_title = data['title']

        for query in data['queries']:
            # Clean query title (remove newlines, limit length)
            clean_query_title = query['title'].replace('\n', ' ').replace('\r', ' ').strip()
            clean_query_title = ' '.join(clean_query_title.split())  # Normalize whitespace

            # Create card name (max 200 chars to be safe, Metabase limit is 254)
            if metric_num:
                card_name = f"#{metric_num}.{query['number']} {metric_title} - {clean_query_title}"
            else:
                card_name = f"{metric_title} - {clean_query_title}"

            # Truncate if too long
            if len(card_name) > 200:
                card_name = card_name[:197] + "..."

            # Create card description
            card_desc = f"{data['description']}\n\nQuery: {clean_query_title}"

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
                print(f"    URL: {METABASE_URL}/question/{card['id']}")
                total_created += 1
            except MetabaseError as e:
                print(f"  ✗ Failed to create '{card_name}': {e}")

    # Summary
    print("\n" + "=" * 80)
    print("IMPORT COMPLETE")
    print("=" * 80)
    print(f"✓ Successfully created {total_created} out of {total_queries} cards")
    if collection_id:
        print(f"✓ All cards are in the 'Revenue Analytics' collection")
        print(f"✓ View collection: {METABASE_URL}/collection/{collection_id}")
    print("\nYou can now access these queries in your Metabase instance!")
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
