#!/usr/bin/env python3
"""
Example script demonstrating common Metabase API operations
"""

import os
from dotenv import load_dotenv
from metabase_helper import MetabaseClient, MetabaseError

# Load environment variables
load_dotenv()


def setup_client():
    """Initialize Metabase client from environment variables"""
    return MetabaseClient(
        base_url=os.getenv('METABASE_URL'),
        username=os.getenv('METABASE_USERNAME'),
        password=os.getenv('METABASE_PASSWORD'),
        api_key=os.getenv('METABASE_API_KEY')
    )


def example_list_databases(mb: MetabaseClient):
    """Example: List all available databases"""
    print("\n" + "="*50)
    print("Example 1: List Databases")
    print("="*50)
    
    databases = mb.list_databases()
    print(f"\nFound {len(databases)} database(s):")
    for db in databases:
        print(f"  • {db['name']} (ID: {db['id']})")
        print(f"    Engine: {db.get('engine', 'N/A')}")


def example_create_simple_card(mb: MetabaseClient, database_id: int):
    """Example: Create a simple SQL card"""
    print("\n" + "="*50)
    print("Example 2: Create Simple SQL Card")
    print("="*50)
    
    try:
        card = mb.create_card(
            name="Example: Count Query",
            sql_query="SELECT COUNT(*) as total FROM (SELECT 1) t",
            database_id=database_id,
            description="Simple count query created via API"
        )
        
        print(f"\n✓ Card created successfully!")
        print(f"  ID: {card['id']}")
        print(f"  URL: {mb.base_url}/question/{card['id']}")
        
        return card['id']
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")
        return None


def example_execute_adhoc_query(mb: MetabaseClient, database_id: int):
    """Example: Execute query without saving"""
    print("\n" + "="*50)
    print("Example 3: Execute Ad-hoc Query")
    print("="*50)
    
    try:
        result = mb.execute_query(
            sql_query="SELECT 'Hello' as message, 123 as number",
            database_id=database_id
        )
        
        print("\n✓ Query executed successfully!")
        print(f"  Rows returned: {len(result['data']['rows'])}")
        print(f"  Results: {result['data']['rows']}")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def example_create_collection_with_cards(mb: MetabaseClient, database_id: int):
    """Example: Create a collection and add cards to it"""
    print("\n" + "="*50)
    print("Example 4: Create Collection with Cards")
    print("="*50)
    
    try:
        # Create collection
        collection = mb.create_collection(
            name="API Examples",
            description="Collection created via Metabase API skill"
        )
        
        print(f"\n✓ Collection created: {collection['name']} (ID: {collection['id']})")
        
        # Create multiple cards in the collection
        queries = [
            {
                "name": "Query 1: Sum Example",
                "query": "SELECT SUM(x) as total FROM (SELECT 1 as x UNION SELECT 2 UNION SELECT 3) t",
                "description": "Example aggregation"
            },
            {
                "name": "Query 2: Date Example", 
                "query": "SELECT CURRENT_DATE as today",
                "description": "Current date query"
            },
            {
                "name": "Query 3: String Example",
                "query": "SELECT 'Example' as text, LENGTH('Example') as length",
                "description": "String manipulation"
            }
        ]
        
        created_cards = mb.bulk_create_cards(
            cards=queries,
            database_id=database_id,
            collection_id=collection['id']
        )
        
        print(f"\n✓ Created {len(created_cards)} cards in collection")
        
        return collection['id']
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")
        return None


def example_update_card(mb: MetabaseClient, card_id: int):
    """Example: Update an existing card"""
    print("\n" + "="*50)
    print("Example 5: Update Card")
    print("="*50)
    
    try:
        updated_card = mb.update_card(
            card_id=card_id,
            description="Updated description via API",
            sql_query="SELECT 'Updated!' as status, COUNT(*) as count FROM (SELECT 1 UNION SELECT 2) t"
        )
        
        print(f"\n✓ Card updated successfully!")
        print(f"  ID: {updated_card['id']}")
        print(f"  New description: {updated_card.get('description')}")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def example_list_collections_and_cards(mb: MetabaseClient):
    """Example: List all collections and their cards"""
    print("\n" + "="*50)
    print("Example 6: List Collections and Cards")
    print("="*50)
    
    try:
        collections = mb.list_collections()
        print(f"\nFound {len(collections)} collection(s):")
        
        for collection in collections[:5]:  # Show first 5
            print(f"\n  📁 {collection['name']} (ID: {collection['id']})")
            
            # Get items in collection
            items = mb.get_collection_items(collection['id'])
            if items:
                print(f"     Contains {len(items)} item(s)")
                for item in items[:3]:  # Show first 3 items
                    print(f"       - {item.get('name', 'Unnamed')}")
            else:
                print("     (empty)")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def example_complex_sql_card(mb: MetabaseClient, database_id: int):
    """Example: Create card with complex SQL"""
    print("\n" + "="*50)
    print("Example 7: Create Complex SQL Card")
    print("="*50)
    
    complex_query = """
    -- Multi-step query example
    WITH base_data AS (
        SELECT 
            1 as id,
            'Product A' as name,
            100 as price
        UNION ALL
        SELECT 2, 'Product B', 150
        UNION ALL
        SELECT 3, 'Product C', 200
    ),
    aggregated AS (
        SELECT 
            COUNT(*) as total_products,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM base_data
    )
    SELECT 
        total_products,
        ROUND(avg_price, 2) as average_price,
        min_price,
        max_price,
        max_price - min_price as price_range
    FROM aggregated
    """
    
    try:
        card = mb.create_card(
            name="Example: Complex Analytics Query",
            sql_query=complex_query,
            database_id=database_id,
            description="Demonstrates CTE usage and aggregations",
            display="table"
        )
        
        print(f"\n✓ Complex card created!")
        print(f"  ID: {card['id']}")
        print(f"  URL: {mb.base_url}/question/{card['id']}")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def example_run_saved_card(mb: MetabaseClient, card_id: int):
    """Example: Execute a saved card's query"""
    print("\n" + "="*50)
    print("Example 8: Run Saved Card Query")
    print("="*50)
    
    try:
        result = mb.run_card_query(card_id)
        print(f"\n✓ Card query executed!")
        print(f"  Status: {result.get('status')}")
        if result.get('data') and result['data'].get('rows'):
            print(f"  Rows: {len(result['data']['rows'])}")
            print(f"  First row: {result['data']['rows'][0]}")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def cleanup_example(mb: MetabaseClient, card_id: int):
    """Example: Clean up created resources"""
    print("\n" + "="*50)
    print("Cleanup: Delete Test Card")
    print("="*50)
    
    try:
        mb.delete_card(card_id)
        print(f"\n✓ Card {card_id} deleted")
    except MetabaseError as e:
        print(f"\n✗ Error: {e}")


def main():
    """Run all examples"""
    print("\n" + "="*50)
    print("Metabase API Examples")
    print("="*50)
    
    # Initialize client
    try:
        mb = setup_client()
        print("\n✓ Connected to Metabase successfully!")
    except Exception as e:
        print(f"\n✗ Failed to connect: {e}")
        print("\nMake sure to set environment variables:")
        print("  METABASE_URL")
        print("  METABASE_API_KEY (or METABASE_USERNAME and METABASE_PASSWORD)")
        return
    
    # Get first database ID
    databases = mb.list_databases()
    if not databases:
        print("\n✗ No databases found in Metabase")
        return
    
    database_id = databases[0]['id']
    
    # Run examples
    example_list_databases(mb)
    
    card_id = example_create_simple_card(mb, database_id)
    
    example_execute_adhoc_query(mb, database_id)
    
    collection_id = example_create_collection_with_cards(mb, database_id)
    
    if card_id:
        example_update_card(mb, card_id)
        example_run_saved_card(mb, card_id)
    
    example_list_collections_and_cards(mb)
    
    example_complex_sql_card(mb, database_id)
    
    # Optional cleanup
    # if card_id:
    #     cleanup_example(mb, card_id)
    
    print("\n" + "="*50)
    print("Examples completed!")
    print("="*50)
    print("\nCheck your Metabase instance to see the created resources:")
    print(f"{mb.base_url}")


if __name__ == "__main__":
    main()
