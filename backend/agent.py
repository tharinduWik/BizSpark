import google.generativeai as genai
import os
from file_loader import load_all_data, search_items, get_item_by_id
import pandas as pd
import json
from dotenv import load_dotenv
import re
from datetime import datetime
from typing import Dict, List, Any

# Load environment variables from .env file
load_dotenv()

# Set up Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None

# Conversation memory storage (session_id -> conversation history)
conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

def find_relevant_items(query, items_data):
    """
    Find items relevant to the query, but don't generate any responses.
    Just return the relevant items for context.
    
    Parameters:
    - query: User's query text
    - items_data: List of item dictionaries
    
    Returns:
    - Dictionary with item_data or items key containing relevant items
    """
    query_lower = query.lower().strip()
    result = {}
    
    # Handle direct ID queries
    if "sku" in query_lower:
        sku_pattern = r'SKU\d{7}'
        match = re.search(sku_pattern, query, re.IGNORECASE)
        if match:
            item_id = match.group(0)
            item = get_item_by_id(items_data, item_id)
            if item:
                result["item_data"] = item
                return result
    
    # Handle price range queries
    price_range_pattern = r'under\s+\$?(\d+)|less\s+than\s+\$?(\d+)|cheaper\s+than\s+\$?(\d+)'
    match = re.search(price_range_pattern, query_lower)
    if match:
        max_price = int(next(filter(None, match.groups())))
        results = search_items(items_data, max_price=max_price, sort_by='price')
        if results:
            result["items"] = results[:5]
            return result
    
    # Handle product category searches
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
                    result["items"] = results[:5]
                    return result
    
    # Check for specific item names in the query
    for item in items_data:
        item_name_lower = item['item_name'].lower()
        if item_name_lower in query_lower:
            result["item_data"] = item
            return result
    
    # No specific matches found
    return None

def get_conversation_history(session_id: str, max_entries: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve conversation history for a specific session
    
    Parameters:
    - session_id: Unique identifier for the user session
    - max_entries: Maximum number of conversation entries to include
    
    Returns:
    - List of conversation entries
    """
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    
    # Return the most recent entries (limited by max_entries)
    return conversation_memory[session_id][-max_entries:]


def add_to_conversation_history(session_id: str, role: str, content: Any, context: Dict[str, Any] = None):
    """
    Add a new entry to the conversation history
    
    Parameters:
    - session_id: Unique identifier for the user session
    - role: 'user' or 'assistant'
    - content: The message content
    - context: Optional context data (like item details)
    """
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    
    # Create the conversation entry
    entry = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    # Add context if provided
    if context:
        entry["context"] = context
    
    # Add to memory
    conversation_memory[session_id].append(entry)
    
    # Limit the size of conversation history (keep last 10 entries)
    if len(conversation_memory[session_id]) > 10:
        conversation_memory[session_id] = conversation_memory[session_id][-10:]


def extract_item_context(result):
    """
    Extract item context from query result
    """
    context = {}
    
    # Extract item data if available
    if "item_data" in result and result["item_data"]:
        context["current_item"] = result["item_data"]
    
    # Extract multiple items if available
    if "items" in result and result["items"]:
        context["item_list"] = result["items"]
    
    return context if context else None


def handle_query(query, session_id="default"):
    """
    Main function to handle user queries about items with conversation memory
    All queries now go through the API for natural responses
    
    Parameters:
    - query: User's query text
    - session_id: Unique identifier for the user session
    """
    # Load items data
    items_data = load_all_data()
    
    # Get conversation history
    conversation_history = get_conversation_history(session_id)
    
    # Add user query to conversation history
    add_to_conversation_history(session_id, "user", query)
    
    # Find relevant items for context (but don't use them for direct responses)
    relevant_items_result = find_relevant_items(query, items_data)
    context = extract_item_context(relevant_items_result) if relevant_items_result else None
    
    # Use AI to handle all queries with context
    if model:
        try:
            # Extract context from recent conversation
            current_context = {}
            recent_items = []
            
            # Look for recent items in conversation history
            for entry in reversed(conversation_history):
                if "context" in entry and entry["context"]:
                    if "current_item" in entry["context"] and not current_context.get("current_item"):
                        current_context["current_item"] = entry["context"]["current_item"]
                    
                    if "item_list" in entry["context"] and not current_context.get("item_list"):
                        current_context["item_list"] = entry["context"]["item_list"]
                
                # Stop once we have enough context
                if "current_item" in current_context and "item_list" in current_context:
                    break
            
            # If we have new context from this query, update current_context
            if context:
                if "current_item" in context and not current_context.get("current_item"):
                    current_context["current_item"] = context["current_item"]
                if "item_list" in context and not current_context.get("item_list"):
                    current_context["item_list"] = context["item_list"]
            
            # Convert conversation history to string format
            conversation_text = ""
            for entry in conversation_history:
                if entry["role"] == "user":
                    conversation_text += f"Customer: {entry['content']}\n"
                else:
                    # Truncate long responses
                    response = entry['content']
                    if len(response) > 200:
                        response = response[:197] + "..."
                    conversation_text += f"Assistant: {response}\n"
            
            # Prepare items information for the AI
            items_info = ""
            
            # Include current item from context first if available
            if current_context.get("current_item"):
                item = current_context["current_item"]
                items_info += (f"[CURRENTLY DISCUSSING] Item: ID={item['item_id']}, Name={item['item_name']}, "
                             f"Price=${item['price']:.2f}, Quantity={item['item_quantity']}, "
                             f"Description={item.get('item_description', 'No description available')}, "
                             f"Discount={item['maximum_discount']*100:.0f}%\n")
            
            # Include recently discussed items if available
            if current_context.get("item_list"):
                for i, item in enumerate(current_context["item_list"]):
                    items_info += (f"Recent Item {i+1}: ID={item['item_id']}, Name={item['item_name']}, "
                                 f"Price=${item['price']:.2f}, "
                                 f"Description={item.get('item_description', 'No description available')}, "
                                 f"Discount={item.get('maximum_discount', 0)*100:.0f}%\n")
            
            # Include general items as well (avoiding duplicates)
            already_included_ids = set()
            if current_context.get("current_item"):
                already_included_ids.add(current_context["current_item"]["item_id"])
            if current_context.get("item_list"):
                for item in current_context["item_list"]:
                    already_included_ids.add(item["item_id"])
            
            # Add additional items for context
            for i, item in enumerate(items_data[:15]):  # Limit to 15 additional items
                if item["item_id"] not in already_included_ids:
                    items_info += (f"Item: ID={item['item_id']}, Name={item['item_name']}, "
                                  f"Price=${item['price']:.2f}, Quantity={item['item_quantity']}, "
                                  f"Description={item.get('item_description', 'No description available')}, "
                                  f"Discount={item.get('maximum_discount', 0)*100:.0f}%\n")
            
            # Create prompt for the AI with conversation context
            prompt = f"""
You are a helpful sales assistant for an e-commerce store. Based on the query and conversation history,
help the customer find products they're looking for or answer questions about our inventory.

CONVERSATION HISTORY:
{conversation_text}

CURRENT CUSTOMER QUERY: {query}

ITEMS INFORMATION:
{items_info}

INSTRUCTIONS:
1. If the customer is asking about an item already mentioned in the conversation, use that context.
2. If the query refers to "it", "this item", "that product", etc., assume they are talking about the item marked [CURRENTLY DISCUSSING].
3. If the customer is asking about price, features, availability, or discounts, look for the relevant item in the context.
4. Be concise, helpful, and specific in your recommendations.
5. ALWAYS mention the exact discount percentage when discussing an item that has a discount.
6. ALWAYS include the item description in your response when focusing on a specific item.
7. If answering a follow-up question about a specific item, always mention the item name for clarity.
8. When discussing prices, always format them as $XX.XX with two decimal places.
"""
            response = model.generate_content(prompt)
            
            # Extract the AI's response
            ai_response = response.text.strip()
            
            # Add assistant response to conversation history
            add_to_conversation_history(session_id, "assistant", ai_response, context)
            
            # Create a JSON response with both AI text AND relevant items
            result = {
                "response": ai_response,
                "query": query,
                "format": "text"
            }
            
            # Include item data if available
            if context:
                if "current_item" in context:
                    result["item_data"] = context["current_item"]
                if "item_list" in context:
                    result["items"] = context["item_list"]
            
            return result
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again with a more specific query."
            
            # Add error response to conversation history
            add_to_conversation_history(session_id, "assistant", error_response)
            
            return {
                "response": error_response,
                "query": query,
                "format": "text"
            }
    else:
        # Even without an AI model, we can provide useful information about items
        featured_items = items_data[:5]  # Get 5 items to feature
        items_text = "\n".join([
            f"- {item['item_name']} (${item['price']:.2f})" +
            (f" - {item['maximum_discount']*100:.0f}% discount available!" if item.get('maximum_discount', 0) > 0 else "") 
            for item in featured_items
        ])
        
        fallback_response = f"I can help you find items in our inventory. Here are some featured products:\n\n{items_text}\n\nHow can I assist you today?"
        
        # Add fallback response to conversation history
        add_to_conversation_history(session_id, "assistant", fallback_response, {"item_list": featured_items})
        
        return {
            "response": fallback_response,
            "query": query,
            "items": featured_items,
            "format": "text"
        }
