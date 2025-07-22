import google.generativeai as genai
import os
from file_loader import load_all_data, search_items, get_item_by_id
import pandas as pd
import json
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Set up Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None

# We're no longer using this function as we've integrated its logic into handle_query
# and all responses now go through the AI model
def handle_direct_item_query(query, items_data):
    """
    This function is deprecated. All queries now go through the AI model.
    """
    return None

def handle_query(query):
    """
    Main function to handle user queries about items
    """
    # Load items data
    items_data = load_all_data()
    
    # Get potential matching items to provide context to the AI
    matching_items = []
    query_lower = query.lower().strip()
    
    # Check for specific item names or keywords in the query
    for item in items_data:
        if query_lower in item['item_name'].lower() or item['item_name'].lower() in query_lower:
            matching_items.append(item)
    
    # If no direct name matches, look for category keywords
    if not matching_items:
        categories = {
            "electronics": ["laptop", "tablet", "computer", "phone", "headphones", "earbuds", "speaker"],
            "office supplies": ["stapler", "paper", "pen", "pencil", "notebook", "binder"],
            "clothing": ["shirt", "pants", "jacket", "hoodie", "sweater", "yoga"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in query_lower:
                    results = search_items(items_data, search_query=keyword)
                    if results:
                        matching_items.extend(results[:5])
                        break
            if matching_items:
                break
    
    # Check for price ranges in query
    price_range_pattern = r'under\s+\$?(\d+)|less\s+than\s+\$?(\d+)|cheaper\s+than\s+\$?(\d+)'
    match = re.search(price_range_pattern, query_lower)
    if match:
        max_price = int(next(filter(None, match.groups())))
        price_results = search_items(items_data, max_price=max_price, sort_by='price')
        if price_results:
            matching_items.extend(price_results[:5])
    
    # Use AI to handle all queries
    if model:
        try:
            # Prepare items for AI context - prioritize matching items first
            relevant_items = []
            
            # Make sure we don't have duplicate items
            seen_items = set()
            
            # First add matching items (if any)
            for item in matching_items:
                if item['item_id'] not in seen_items:
                    relevant_items.append(item)
                    seen_items.add(item['item_id'])
            
            # Then add some general items for context
            general_items = []
            for item in items_data:
                if item['item_id'] not in seen_items and len(relevant_items) + len(general_items) < 20:
                    general_items.append(item)
                    seen_items.add(item['item_id'])
            
            # Combine relevant and general items
            items_to_include = relevant_items + general_items
            
            # Convert items to a string format for the AI
            items_info = ""
            
            # Format matching items (mark them as relevant)
            for i, item in enumerate(relevant_items):
                items_info += (f"[RELEVANT TO QUERY] Item: ID={item['item_id']}, Name={item['item_name']}, "
                             f"Price=${item['price']:.2f}, Quantity={item['item_quantity']}, "
                             f"Description={item['item_description']}, "
                             f"Discount={item['maximum_discount']*100:.0f}%\n")
            
            # Format general items
            for i, item in enumerate(general_items):
                items_info += (f"Item: ID={item['item_id']}, Name={item['item_name']}, "
                              f"Price=${item['price']:.2f}, Quantity={item['item_quantity']}, "
                              f"Description={item['item_description']}, "
                              f"Discount={item['maximum_discount']*100:.0f}%\n")
            
            # Create prompt for the AI
            prompt = f"""
You are a helpful sales assistant for an e-commerce store. Based on the query, help the customer 
find products they're looking for or answer questions about our inventory.

Customer query: {query}

Here's information about our items:
{items_info}

INSTRUCTIONS:
1. Respond in a natural, conversational way as a sales assistant.
2. If the query is about a specific item, provide details about that item.
3. If the query is about price range or categories, suggest appropriate items.
4. If they ask about discounts or offers, mention the available discount percentage.
5. Always include the price in your response.
6. Be concise but informative.
"""
            response = model.generate_content(prompt)
            
            # Extract the AI's response
            ai_response = response.text.strip()
            
            # Create a JSON response
            result = {
                "response": ai_response,
                "query": query,
                "format": "text"
            }
            
            # Include matched items in the response
            if relevant_items:
                result["items"] = relevant_items[:5]  # Include up to 5 most relevant items
            
            return result
            
        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try again with a more specific query.",
                "query": query,
                "format": "text"
            }
    else:
        # Even in fallback mode, provide item details instead of a generic message
        items_list = items_data[:5]  # Just show the first 5 items
        items_text = ""
        for item in items_list:
            items_text += f"{item['item_name']} - ${item['price']:.2f}\n"
        
        return {
            "response": f"Here are some items from our inventory:\n\n{items_text}\n\nYou can ask for more specific products or categories.",
            "items": items_list,
            "query": query,
            "format": "text"
        }
