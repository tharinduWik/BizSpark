#!/usr/bin/env python3
"""
End-to-end test of the AI Air Quality Agent with real OpenAI API
"""

import requests
import json
import time

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔬 Testing Backend API...")
    print("=" * 40)
    
    # Test queries
    test_queries = [
        "Hello!",
        "Show me average temperature in each room",
        "How does temperature vary by hour of the day?",
        "Which room has the highest CO2 levels?",
        "Compare humidity levels across all rooms"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: '{query}'")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{base_url}/query",
                json={"query": query},
                timeout=30  # Increase timeout for OpenAI API calls
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                    if "details" in result:
                        print(f"   Details: {result['details']}")
                else:
                    print("✅ Success!")
                    if "response" in result:
                        print(f"   Response: {result['response'][:100]}...")
                    if "table" in result:
                        print(f"   Table rows: {len(result['table'])}")
                    if "suggestions" in result:
                        print(f"   Suggestions: {len(result['suggestions'])}")
                        
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏱️ Request timed out (this may happen with OpenAI API calls)")
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - is the backend running on port 8000?")
        except Exception as e:
            print(f"❌ Exception: {e}")
            
        time.sleep(1)  # Brief pause between requests

def check_health():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except:
        print("❌ Backend is not running. Please start it first.")
        return False

if __name__ == "__main__":
    print("🧪 AI Air Quality Agent - End-to-End Test")
    print("=" * 50)
    
    if check_health():
        test_backend()
    else:
        print("\n💡 To start the backend:")
        print("   cd e:\\Agent\\ai-air-quality-agent\\backend")
        print("   python -m uvicorn main:app --reload --port 8000")
        
    print("\n🔗 After testing, you can access:")
    print("   Backend API: http://localhost:8000")
    print("   Frontend: http://localhost:3000")
    print("   API Docs: http://localhost:8000/docs")
