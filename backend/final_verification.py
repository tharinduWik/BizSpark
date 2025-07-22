#!/usr/bin/env python3
"""
Final verification that the system works with Gemini
"""

def test_imports():
    """Test that all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported")
    except ImportError:
        print("❌ google.generativeai not found - run: pip install google-generativeai")
        return False
    
    try:
        import fastapi
        print("✅ fastapi imported")
    except ImportError:
        print("❌ fastapi not found")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported")
    except ImportError:
        print("❌ pandas not found")
        return False
        
    return True

def test_env():
    """Test environment variables"""
    print("\n🔍 Testing environment...")
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        print(f"✅ GEMINI_API_KEY found: {api_key[:20]}...")
        return True
    else:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False

def test_gemini_quick():
    """Quick test of Gemini API"""
    print("\n🔍 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content("Respond with just the word 'SUCCESS'")
        
        if response.text and "SUCCESS" in response.text.upper():
            print("✅ Gemini API working correctly")
            return True
        else:
            print(f"⚠️ Unexpected response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def test_agent():
    """Test the agent module"""
    print("\n🔍 Testing agent module...")
    
    try:
        from agent import handle_query
        
        result = handle_query("Hello")
        
        if "error" in result:
            print(f"❌ Agent error: {result['error']}")
            return False
        else:
            print("✅ Agent working correctly")
            return True
            
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def main():
    print("🧪 Final System Verification - Gemini Edition")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Setup", test_env),
        ("Gemini API", test_gemini_quick),
        ("Agent Module", test_agent)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {name} failed")
    
    print(f"\n{'='*60}")
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the system:")
        print("1. Backend: python -m uvicorn main:app --reload --port 8000")
        print("2. Frontend: cd ../frontend && npm start")
        print("3. Open: http://localhost:3000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
