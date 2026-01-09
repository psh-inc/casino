#!/usr/bin/env python3
"""
Metabase CLI Tool
Command-line interface for Metabase API operations
"""

import sys
import os
import argparse
import json
from dotenv import load_dotenv
from metabase_helper import MetabaseClient, MetabaseError

# Load environment variables
load_dotenv()


def get_client():
    """Initialize and return Metabase client"""
    return MetabaseClient(
        base_url=os.getenv('METABASE_URL', 'http://localhost:3000'),
        username=os.getenv('METABASE_USERNAME', 'kaxgel11@gmail.com'),
        password=os.getenv('METABASE_PASSWORD', 'dwrstn11'),
        api_key=os.getenv('METABASE_API_KEY')
    )


def cmd_list_databases(args):
    """List all databases"""
    mb = get_client()
    databases = mb.list_databases()
    
    print("\nAvailable Databases:")
    print("-" * 60)
    for db in databases:
        print(f"ID: {db['id']:3d} | Name: {db['name']}")
        if args.verbose:
            print(f"      Engine: {db.get('engine', 'N/A')}")
    print(f"\nTotal: {len(databases)} database(s)")


def cmd_list_cards(args):
    """List all cards"""
    mb = get_client()
    cards = mb.list_cards()
    
    print("\nAll Cards:")
    print("-" * 60)
    for card in cards:
        print(f"ID: {card['id']:5d} | {card['name']}")
        if args.verbose and card.get('description'):
            print(f"         {card['description']}")
    print(f"\nTotal: {len(cards)} card(s)")


def cmd_create_card(args):
    """Create a new card"""
    mb = get_client()
    
    # Read SQL from file or argument
    if args.sql_file:
        with open(args.sql_file, 'r') as f:
            sql_query = f.read()
    else:
        sql_query = args.sql
    
    try:
        card = mb.create_card(
            name=args.name,
            sql_query=sql_query,
            database_id=args.database_id,
            collection_id=args.collection_id,
            description=args.description,
            display=args.display
        )
        
        print(f"\n✓ Card created successfully!")
        print(f"  ID: {card['id']}")
        print(f"  Name: {card['name']}")
        print(f"  URL: {mb.base_url}/question/{card['id']}")
        
        if args.json:
            print(f"\nFull response:")
            print(json.dumps(card, indent=2))
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_execute_query(args):
    """Execute an ad-hoc query"""
    mb = get_client()
    
    # Read SQL from file or argument
    if args.sql_file:
        with open(args.sql_file, 'r') as f:
            sql_query = f.read()
    else:
        sql_query = args.sql
    
    try:
        result = mb.execute_query(
            sql_query=sql_query,
            database_id=args.database_id
        )
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n✓ Query executed successfully!")
            print(f"  Status: {result.get('status')}")
            
            if result.get('data'):
                rows = result['data'].get('rows', [])
                cols = result['data'].get('cols', [])
                
                print(f"  Rows: {len(rows)}")
                
                if cols:
                    print("\nColumns:")
                    for col in cols:
                        print(f"  - {col.get('name', col.get('display_name', 'Unknown'))}")
                
                if rows and args.show_results:
                    print("\nFirst 10 rows:")
                    for i, row in enumerate(rows[:10]):
                        print(f"  {i+1}. {row}")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list_collections(args):
    """List all collections"""
    mb = get_client()
    collections = mb.list_collections()
    
    print("\nCollections:")
    print("-" * 60)
    for coll in collections:
        print(f"ID: {coll['id']:3d} | {coll['name']}")
        if args.verbose and coll.get('description'):
            print(f"      {coll['description']}")
    print(f"\nTotal: {len(collections)} collection(s)")


def cmd_create_collection(args):
    """Create a new collection"""
    mb = get_client()
    
    try:
        collection = mb.create_collection(
            name=args.name,
            parent_id=args.parent_id,
            description=args.description
        )
        
        print(f"\n✓ Collection created successfully!")
        print(f"  ID: {collection['id']}")
        print(f"  Name: {collection['name']}")
        
        if args.json:
            print(f"\nFull response:")
            print(json.dumps(collection, indent=2))
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_get_card(args):
    """Get card details"""
    mb = get_client()
    
    try:
        card = mb.get_card(args.card_id)
        
        print(f"\nCard Details:")
        print("-" * 60)
        print(f"ID: {card['id']}")
        print(f"Name: {card['name']}")
        print(f"Description: {card.get('description', 'N/A')}")
        print(f"Display: {card.get('display', 'N/A')}")
        print(f"Collection ID: {card.get('collection_id', 'N/A')}")
        
        if card.get('dataset_query', {}).get('native'):
            print(f"\nSQL Query:")
            print(card['dataset_query']['native']['query'])
        
        if args.json:
            print(f"\nFull JSON:")
            print(json.dumps(card, indent=2))
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_delete_card(args):
    """Delete a card"""
    mb = get_client()
    
    if not args.force:
        confirm = input(f"Are you sure you want to delete card {args.card_id}? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
    
    try:
        mb.delete_card(args.card_id)
        print(f"\n✓ Card {args.card_id} deleted successfully!")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_bulk_import(args):
    """Bulk import SQL files"""
    mb = get_client()
    
    import glob
    sql_files = glob.glob(args.pattern)
    
    if not sql_files:
        print(f"No files found matching: {args.pattern}")
        return
    
    print(f"\nFound {len(sql_files)} SQL file(s)")
    
    cards_to_create = []
    for sql_file in sql_files:
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Extract name from filename
        name = os.path.splitext(os.path.basename(sql_file))[0]
        name = name.replace('_', ' ').replace('-', ' ').title()
        
        cards_to_create.append({
            'name': name,
            'query': sql_content,
            'description': f"Imported from {sql_file}"
        })
    
    try:
        results = mb.bulk_create_cards(
            cards=cards_to_create,
            database_id=args.database_id,
            collection_id=args.collection_id
        )
        
        print(f"\n✓ Successfully imported {len(results)} card(s)")
        
        for result in results:
            print(f"  - {result['name']} (ID: {result['id']})")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Metabase API CLI Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List databases
    db_parser = subparsers.add_parser('databases', aliases=['db'], help='List databases')
    db_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed info')
    db_parser.set_defaults(func=cmd_list_databases)
    
    # List cards
    cards_parser = subparsers.add_parser('cards', help='List all cards')
    cards_parser.add_argument('-v', '--verbose', action='store_true', help='Show descriptions')
    cards_parser.set_defaults(func=cmd_list_cards)
    
    # Create card
    create_parser = subparsers.add_parser('create', help='Create a new card')
    create_parser.add_argument('name', help='Card name')
    create_parser.add_argument('-d', '--database-id', type=int, required=True, help='Database ID')
    create_parser.add_argument('-s', '--sql', help='SQL query string')
    create_parser.add_argument('-f', '--sql-file', help='SQL file path')
    create_parser.add_argument('-c', '--collection-id', type=int, help='Collection ID')
    create_parser.add_argument('--description', help='Card description')
    create_parser.add_argument('--display', default='table', help='Display type (default: table)')
    create_parser.add_argument('--json', action='store_true', help='Output full JSON response')
    create_parser.set_defaults(func=cmd_create_card)
    
    # Execute query
    exec_parser = subparsers.add_parser('query', aliases=['exec'], help='Execute ad-hoc query')
    exec_parser.add_argument('-d', '--database-id', type=int, required=True, help='Database ID')
    exec_parser.add_argument('-s', '--sql', help='SQL query string')
    exec_parser.add_argument('-f', '--sql-file', help='SQL file path')
    exec_parser.add_argument('--show-results', action='store_true', help='Display results')
    exec_parser.add_argument('--json', action='store_true', help='Output raw JSON')
    exec_parser.set_defaults(func=cmd_execute_query)
    
    # List collections
    coll_parser = subparsers.add_parser('collections', aliases=['coll'], help='List collections')
    coll_parser.add_argument('-v', '--verbose', action='store_true', help='Show descriptions')
    coll_parser.set_defaults(func=cmd_list_collections)
    
    # Create collection
    create_coll_parser = subparsers.add_parser('create-collection', help='Create a collection')
    create_coll_parser.add_argument('name', help='Collection name')
    create_coll_parser.add_argument('-p', '--parent-id', type=int, help='Parent collection ID')
    create_coll_parser.add_argument('--description', help='Collection description')
    create_coll_parser.add_argument('--json', action='store_true', help='Output JSON')
    create_coll_parser.set_defaults(func=cmd_create_collection)
    
    # Get card
    get_parser = subparsers.add_parser('get', help='Get card details')
    get_parser.add_argument('card_id', type=int, help='Card ID')
    get_parser.add_argument('--json', action='store_true', help='Output full JSON')
    get_parser.set_defaults(func=cmd_get_card)
    
    # Delete card
    del_parser = subparsers.add_parser('delete', help='Delete a card')
    del_parser.add_argument('card_id', type=int, help='Card ID to delete')
    del_parser.add_argument('-f', '--force', action='store_true', help='Skip confirmation')
    del_parser.set_defaults(func=cmd_delete_card)
    
    # Bulk import
    import_parser = subparsers.add_parser('import', help='Bulk import SQL files')
    import_parser.add_argument('pattern', help='File pattern (e.g., "queries/*.sql")')
    import_parser.add_argument('-d', '--database-id', type=int, required=True, help='Database ID')
    import_parser.add_argument('-c', '--collection-id', type=int, help='Collection ID')
    import_parser.set_defaults(func=cmd_bulk_import)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
