#!/usr/bin/env python3
"""
Quick OpenAI API test
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def quick_test():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    client = openai.OpenAI(api_key=api_key)
    
    try:
        print("🔄 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say hello briefly"}
            ],
            max_tokens=10
        )
        
        print("✅ API works!")
        print(f"Response: {response.choices[0].message.content}")
        
        # Test function calling
        print("\n🔄 Testing function calling...")
        func_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Write code to add 2+2"}
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "execute_code",
                        "description": "Execute Python code",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string"},
                            },
                            "required": ["code"]
                        }
                    }
                }
            ],
            tool_choice="auto"
        )
        
        if func_response.choices[0].message.tool_calls:
            print("✅ Function calling works!")
        else:
            print("⚠️ No function call made")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()
