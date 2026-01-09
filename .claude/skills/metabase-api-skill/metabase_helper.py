#!/usr/bin/env python3
"""
Metabase API Helper
A comprehensive client for interacting with Metabase REST API
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class MetabaseError(Exception):
    """Custom exception for Metabase API errors"""
    pass


class MetabaseClient:
    """Client for interacting with Metabase REST API"""
    
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        session_token: Optional[str] = None
    ):
        """
        Initialize Metabase client
        
        Args:
            base_url: Metabase instance URL (e.g., 'https://metabase.example.com')
            username: Username for authentication
            password: Password for authentication
            api_key: API key for authentication (preferred over username/password)
            session_token: Existing session token (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session_token = session_token
        self.session = requests.Session()
        
        # Authenticate if credentials provided
        if not api_key and not session_token and username and password:
            self._authenticate()
    
    def _authenticate(self) -> str:
        """
        Authenticate with Metabase and get session token
        
        Returns:
            Session token
        """
        url = f"{self.base_url}/api/session"
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.session_token = data.get('id')
            return self.session_token
        except requests.exceptions.RequestException as e:
            raise MetabaseError(f"Authentication failed: {str(e)}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        elif self.session_token:
            headers["X-Metabase-Session"] = self.session_token
        else:
            raise MetabaseError("No authentication method available")
        
        return headers
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Any:
        """
        Make HTTP request to Metabase API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/api/card/')
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            
            # Return parsed JSON if available
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {response.status_code}: {str(e)}"
            try:
                error_detail = response.json()
                error_msg += f" - {json.dumps(error_detail)}"
            except:
                pass
            raise MetabaseError(error_msg)
        except requests.exceptions.RequestException as e:
            raise MetabaseError(f"Request failed: {str(e)}")
    
    def create_card(
        self,
        name: str,
        sql_query: str,
        database_id: int,
        collection_id: Optional[int] = None,
        description: Optional[str] = None,
        display: str = "table",
        visualization_settings: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new SQL card (question) in Metabase
        
        Args:
            name: Card name
            sql_query: SQL query string
            database_id: Database ID in Metabase
            collection_id: Collection ID (None for root)
            description: Card description
            display: Visualization type (table, bar, line, pie, etc.)
            visualization_settings: Custom visualization settings
            
        Returns:
            Created card data including card ID
        """
        payload = {
            "name": name,
            "display": display,
            "dataset_query": {
                "database": database_id,
                "type": "native",
                "native": {
                    "query": sql_query
                }
            },
            "visualization_settings": visualization_settings or {},
            "collection_id": collection_id
        }
        
        if description:
            payload["description"] = description
        
        result = self._make_request("POST", "/api/card/", data=payload)
        print(f"✓ Created card '{name}' with ID: {result['id']}")
        return result
    
    def execute_query(
        self,
        sql_query: str,
        database_id: int
    ) -> Dict:
        """
        Execute an ad-hoc SQL query without saving
        
        Args:
            sql_query: SQL query string
            database_id: Database ID in Metabase
            
        Returns:
            Query results
        """
        payload = {
            "database": database_id,
            "type": "native",
            "native": {
                "query": sql_query
            }
        }
        
        result = self._make_request("POST", "/api/dataset/", data=payload)
        return result
    
    def get_card(self, card_id: int) -> Dict:
        """
        Get card details by ID
        
        Args:
            card_id: Card ID
            
        Returns:
            Card data
        """
        return self._make_request("GET", f"/api/card/{card_id}")
    
    def update_card(
        self,
        card_id: int,
        name: Optional[str] = None,
        sql_query: Optional[str] = None,
        description: Optional[str] = None,
        collection_id: Optional[int] = None
    ) -> Dict:
        """
        Update an existing card
        
        Args:
            card_id: Card ID to update
            name: New name (optional)
            sql_query: New SQL query (optional)
            description: New description (optional)
            collection_id: New collection ID (optional)
            
        Returns:
            Updated card data
        """
        # Get current card data
        current_card = self.get_card(card_id)
        
        # Update only provided fields
        if name:
            current_card["name"] = name
        if description is not None:
            current_card["description"] = description
        if sql_query:
            current_card["dataset_query"]["native"]["query"] = sql_query
        if collection_id is not None:
            current_card["collection_id"] = collection_id
        
        result = self._make_request("PUT", f"/api/card/{card_id}", data=current_card)
        print(f"✓ Updated card ID: {card_id}")
        return result
    
    def delete_card(self, card_id: int) -> None:
        """
        Delete a card
        
        Args:
            card_id: Card ID to delete
        """
        self._make_request("DELETE", f"/api/card/{card_id}")
        print(f"✓ Deleted card ID: {card_id}")
    
    def list_cards(self) -> List[Dict]:
        """
        List all cards accessible to the user
        
        Returns:
            List of cards
        """
        return self._make_request("GET", "/api/card/")
    
    def run_card_query(self, card_id: int, export_format: str = "json") -> Any:
        """
        Execute a saved card's query
        
        Args:
            card_id: Card ID
            export_format: Export format (json, csv, xlsx)
            
        Returns:
            Query results
        """
        if export_format == "json":
            return self._make_request("POST", f"/api/card/{card_id}/query")
        else:
            endpoint = f"/api/card/{card_id}/query/{export_format}"
            return self._make_request("GET", endpoint)
    
    def list_databases(self) -> List[Dict]:
        """
        List all databases
        
        Returns:
            List of databases
        """
        return self._make_request("GET", "/api/database/")
    
    def get_database_metadata(self, database_id: int) -> Dict:
        """
        Get database metadata including tables and fields
        
        Args:
            database_id: Database ID
            
        Returns:
            Database metadata
        """
        return self._make_request("GET", f"/api/database/{database_id}/metadata")
    
    def list_collections(self) -> List[Dict]:
        """
        List all collections
        
        Returns:
            List of collections
        """
        return self._make_request("GET", "/api/collection/")
    
    def create_collection(
        self,
        name: str,
        parent_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> Dict:
        """
        Create a new collection
        
        Args:
            name: Collection name
            parent_id: Parent collection ID (None for root)
            description: Collection description
            
        Returns:
            Created collection data
        """
        payload = {
            "name": name,
            "parent_id": parent_id
        }
        
        if description:
            payload["description"] = description
        
        result = self._make_request("POST", "/api/collection/", data=payload)
        print(f"✓ Created collection '{name}' with ID: {result['id']}")
        return result
    
    def get_collection_items(self, collection_id: int) -> List[Dict]:
        """
        Get items in a collection
        
        Args:
            collection_id: Collection ID
            
        Returns:
            List of items in collection
        """
        return self._make_request("GET", f"/api/collection/{collection_id}/items")
    
    def bulk_create_cards(
        self,
        cards: List[Dict],
        database_id: int,
        collection_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Create multiple cards from a list
        
        Args:
            cards: List of dicts with 'name', 'query', and optional 'description'
            database_id: Database ID
            collection_id: Target collection ID
            
        Returns:
            List of created card data
        """
        results = []
        for card_spec in cards:
            try:
                result = self.create_card(
                    name=card_spec['name'],
                    sql_query=card_spec['query'],
                    database_id=database_id,
                    collection_id=collection_id,
                    description=card_spec.get('description')
                )
                results.append(result)
            except MetabaseError as e:
                print(f"✗ Failed to create card '{card_spec['name']}': {str(e)}")
        
        return results


def main():
    """Example usage"""
    # Initialize from environment variables
    mb = MetabaseClient(
        base_url=os.getenv('METABASE_URL', 'http://localhost:3000'),
        username=os.getenv('METABASE_USERNAME'),
        password=os.getenv('METABASE_PASSWORD'),
        api_key=os.getenv('METABASE_API_KEY')
    )
    
    # Example: List databases
    print("\n📊 Available Databases:")
    databases = mb.list_databases()
    for db in databases:
        print(f"  - {db['name']} (ID: {db['id']})")
    
    # Example: Create a card
    if databases:
        db_id = databases[0]['id']
        card = mb.create_card(
            name="Example Query",
            sql_query="SELECT 1 as test",
            database_id=db_id,
            description="Created by API"
        )
        print(f"\n✓ Card URL: {mb.base_url}/question/{card['id']}")


if __name__ == "__main__":
    main()
