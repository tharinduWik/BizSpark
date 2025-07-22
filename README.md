# AI Air Quality Agent - Gemini Edition 🧠✨

An intelligent air quality data analysis system powered by Google Gemini API. This system allows users to query air quality data from multiple rooms using natural language and get AI-generated analysis with visualizations.

## 🔍 Pure AI Processing Architecture

This system now uses a pure AI-driven approach, where **all** data analysis is performed by the Gemini API:

- Every user query is processed directly by the Gemini API without predefined handlers
- The AI generates Python code that runs directly against your data
- Multiple fallback mechanisms ensure reliable results even with complex queries
- Progressive retry system with simplified prompts for error recovery
- Real-time data analysis without mock replies or canned responses

## ✅ Latest Improvements

- Complete transition to AI-driven processing without predefined query handlers
- Enhanced error handling with multi-layer AI retry mechanisms
- Improved syntax error recovery for malformed queries
- Gemini model updated to use `gemini-2.0-flash-exp` version
- Comprehensive test suite to verify AI processing capabilities

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Backend dependencies
cd backend
pip install google-generativeai fastapi uvicorn pandas python-dotenv

# Frontend dependencies  
cd ../frontend
npm install
```

### 2. Configure Gemini API

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `backend/.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=True
PORT=8000
```

### 3. Start the System

**Option 1: Automatic startup (Recommended)**
```bash
python start_with_gemini.py
```

**Option 2: Manual startup**
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

### 4. Access the System

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs

## Troubleshooting

### Backend Issues

1. **"Module not found" errors**: Install dependencies
   ```bash
   pip install fastapi uvicorn python-dotenv pandas openai
   ```

2. **"Port already in use"**: Kill the process using port 8000
   ```bash
   netstat -ano | findstr :8000
   taskkill /PID <PID_NUMBER> /F
   ```

3. **OpenAI API errors**: The app will work with mock data if no API key is set

### Frontend Issues

1. **"axios not found"**: Install dependencies
   ```bash
   cd frontend
   npm install axios
   ```

2. **"Connection refused"**: Make sure the backend is running on port 8000

## API Endpoints

- `POST /query` - Send queries to the AI agent
- `GET /health` - Check server status
- `GET /docs` - Interactive API documentation

## Sample Queries

Try these queries with your AI agent:

- "What's the average CO2 level in Room 1?"
- "Show me temperature trends across all rooms"
- "Which room has the highest humidity?"
- "Compare air quality between rooms"
- "What are the recent measurements for Room 2?"

## Project Structure

```
ai-air-quality-agent/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── agent.py             # AI agent logic
│   ├── file_loader.py       # Data loading utilities
│   ├── requirements.txt     # Python dependencies
│   ├── start_backend.bat    # Windows batch starter
│   ├── start_backend.ps1    # PowerShell starter
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styling
│   │   └── api.js          # API communication
│   └── package.json        # Node.js dependencies
└── data/
    ├── sensor_data_Room 1.ndjson
    ├── sensor_data_Room 2.ndjson
    ├── sensor_data_Room 3.ndjson
    └── sensor_data_Room 4.ndjson
```

## Environment Variables

Add your OpenAI API key to `backend/.env`:
```
OPENAI_API_KEY=your_actual_api_key_here
```

The app works without an API key using mock responses.
