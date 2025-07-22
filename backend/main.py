from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import handle_query
from file_loader import load_all_data, search_items, get_item_by_id
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class ItemSearchRequest(BaseModel):
    search_query: str = None
    min_price: float = None
    max_price: float = None
    sort_by: str = None

@app.post("/query")
async def query_agent(request: QueryRequest):
    """Main endpoint for chat interactions with the agent with session tracking"""
    result = handle_query(request.query, session_id=request.session_id)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Items Sales AI Agent is running"}

@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get conversation history for a specific session"""
    from agent import get_conversation_history
    history = get_conversation_history(session_id)
    return {"session_id": session_id, "history": history}

@app.get("/items")
async def get_all_items():
    """Get all items in inventory"""
    items_data = load_all_data()
    return {"items": items_data}

@app.post("/items/search")
async def search_items_endpoint(request: ItemSearchRequest):
    """Search for items with filters"""
    items_data = load_all_data()
    results = search_items(
        items_data,
        search_query=request.search_query,
        min_price=request.min_price,
        max_price=request.max_price,
        sort_by=request.sort_by
    )
    return {"items": results, "count": len(results)}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """Get a specific item by ID"""
    items_data = load_all_data()
    item = get_item_by_id(items_data, item_id)
    if item:
        return {"item": item}
    return {"error": f"Item with ID {item_id} not found"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
