#!/usr/bin/env python3
"""
Quick test of Gemini API with correct model
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def quick_gemini_test():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No GEMINI_API_KEY found")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        import google.generativeai as genai
        print("✅ Gemini package imported")
        
        # Configure and test
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Model created with gemini-2.0-flash-exp")
        
        # Simple test
        response = model.generate_content("Say 'Hello from Gemini!' briefly")
        print(f"✅ API Response: {response.text}")
        
        # Test code generation
        code_prompt = """Write Python code to calculate average temperature. Use this format:
result = {
    "query": "test",
    "response": "Average calculated",
    "value": 23.5
}
Only return the code."""
        
        code_response = model.generate_content(code_prompt)
        print(f"✅ Code generation: {code_response.text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Quick Gemini Test")
    print("=" * 30)
    quick_gemini_test()
