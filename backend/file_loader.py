import os
import json
import pandas as pd

def load_items_data():
    """
    Load items data from Excel file
    """
    try:
        # Load the Excel file with items
        items_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Items.xlsx')
        items_df = pd.read_excel(items_file)
        
        # Clean column names in case there are any whitespace issues
        items_df.columns = [col.strip() for col in items_df.columns]
        
        # Convert to dictionary format for easier access
        items_data = items_df.to_dict(orient='records')
        
        print(f"Loaded {len(items_data)} items from {items_file}")
        return items_data
    except Exception as e:
        print(f"Error loading items data: {e}")
        return []

def search_items(items_data, search_query=None, min_price=None, max_price=None, sort_by=None):
    """
    Search for items based on search criteria
    
    Parameters:
    - items_data: List of item dictionaries
    - search_query: String to search in item name and description
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - sort_by: Field to sort by (e.g., 'price', 'item_name')
    
    Returns:
    - List of matching items
    """
    if not items_data:
        return []
    
    # Start with all items
    results = items_data.copy()
    
    # Apply search query filter
    if search_query:
        search_query = search_query.lower()
        results = [
            item for item in results 
            if (search_query in str(item.get('item_name', '')).lower() or 
                search_query in str(item.get('item_description', '')).lower())
        ]
    
    # Apply price filters
    if min_price is not None:
        results = [item for item in results if item.get('price', 0) >= min_price]
    
    if max_price is not None:
        results = [item for item in results if item.get('price', 0) <= max_price]
    
    # Sort results if needed
    if sort_by and sort_by in ['price', 'item_name', 'item_quantity']:
        reverse = sort_by == 'price'  # Sort price high to low by default
        results.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    
    return results

def get_item_by_id(items_data, item_id):
    """
    Get a specific item by its ID
    
    Parameters:
    - items_data: List of item dictionaries
    - item_id: The ID of the item to find
    
    Returns:
    - Item dictionary or None if not found
    """
    for item in items_data:
        if str(item.get('item_id', '')).strip() == str(item_id).strip():
            return item
    return None

def load_all_data():
    """
    Main function to load all items data
    """
    return load_items_data()
