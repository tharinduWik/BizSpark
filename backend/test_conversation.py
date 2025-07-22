import sys
import os

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agent import handle_query

# Test conversation memory with follow-up questions
def test_conversation_memory():
    session_id = "test_session"
    
    print("\n=== Testing Conversation Memory ===\n")
    
    # First query about a specific item
    print("First query: 'Do you have any binders?'")
    result1 = handle_query("Do you have any binders?", session_id=session_id)
    print(f"Response: {result1['response']}\n")
    
    # Follow-up question about the same item
    print("Follow-up query: 'What is the price of that binder?'")
    result2 = handle_query("What is the price of that binder?", session_id=session_id)
    print(f"Response: {result2['response']}\n")
    
    # Another follow-up
    print("Second follow-up: 'What is the maximum discount available?'")
    result3 = handle_query("What is the maximum discount available?", session_id=session_id)
    print(f"Response: {result3['response']}\n")
    
    # New topic
    print("New topic: 'Tell me about laptops under $500'")
    result4 = handle_query("Tell me about laptops under $500", session_id=session_id)
    print(f"Response: {result4['response']}\n")
    
    # Follow-up on new topic
    print("Follow-up on new topic: 'Which one has the best specs?'")
    result5 = handle_query("Which one has the best specs?", session_id=session_id)
    print(f"Response: {result5['response']}\n")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_conversation_memory()
