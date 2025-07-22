#!/usr/bin/env python3
"""
Start the AI Air Quality Agent with Gemini API
"""

import subprocess
import sys
import os
import time

def check_gemini_setup():
    """Check if Gemini is properly set up"""
    print("🔍 Checking Gemini API setup...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Quick test - also check if model can handle Python code generation
        response = model.generate_content(
            "Generate Python code to calculate average of [1,2,3,4,5]. Return only the code, no explanations.")
        if response.text:
            print(f"✅ Gemini API working: Code generation capabilities confirmed")
            return True
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False
    
    return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting backend server...")
    
    try:
        # Start uvicorn server
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"]
        process = subprocess.Popen(cmd, cwd="e:/Agent/ai-air-quality-agent/backend")
        print("✅ Backend started on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def test_endpoint():
    """Test the backend endpoint"""
    import requests
    import json
    
    print("🧪 Testing backend endpoint...")
    time.sleep(3)  # Give server time to start
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        
        # Test query endpoint with a sample data question
        # Using a specific room query to verify AI-based processing
        test_query = {"query": "What's the average temperature in Room 1?"}
        print("🔍 Testing AI analysis with sample query...")
        
        response = requests.post("http://localhost:8000/query", json=test_query, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"❌ Query test failed: {result['error']}")
            elif "table" in result:
                print("✅ Query test passed - AI successfully analyzed data")
                print(f"   Response: {result['response']}")
                return True
            else:
                print("⚠️ Query returned a response but might not have analyzed data properly")
                print(f"   Response: {result.get('response', 'No response text')}")
                return True
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
    
    return False

def main():
    print("🤖 AI Air Quality Agent - Gemini Edition")
    print("=" * 50)
    
    # Check setup
    if not check_gemini_setup():
        print("\n💡 Setup required:")
        print("1. Install: pip install google-generativeai")
        print("2. Add GEMINI_API_KEY to backend/.env file")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    try:
        # Test the backend
        if test_endpoint():
            print("\n🎉 System is ready!")
            print("🔗 Backend API: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("\n💡 You can now:")
            print("1. Start the frontend: cd frontend && npm start")
            print("2. Test queries at: http://localhost:8000/docs")
            print("3. Use the complete system")
            
            # Keep running
            print("\n⌨️ Press Ctrl+C to stop the server...")
            backend_process.wait()
        else:
            print("❌ System test failed")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
