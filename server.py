from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from telethon import TelegramClient
import config
import utils
import uvicorn
from contextlib import asynccontextmanager
from logger import logger

# --- Pydantic Models (Request Bodies) ---
class CreateGroupRequest(BaseModel):
    title: str
    users: List[str]

class UpdateGroupRequest(BaseModel):
    title: str

class AddContactRequest(BaseModel):
    phone: str
    first_name: str
    last_name: Optional[str] = ""

class ScrapeRequest(BaseModel):
    chat_id: str # Can be username or phone or ID
    limit: int = 100

# --- Lifecycle Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the startup and shutdown of the Telegram Client.
    """
    logger.info("Initializing Telegram Client...")
    client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
    await client.start()
    
    # Attach client to app state so endpoints can access it
    app.state.client = client
    
    logger.info("Telegram Client Connected.")
    yield
    
    logger.info("Disconnecting Telegram Client...")
    await client.disconnect()

from fastapi.staticfiles import StaticFiles

# --- FastAPI App ---
app = FastAPI(title="Telegram Agent API", lifespan=lifespan)

# Mount the dashboard directory
app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")

# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "running", "service": "Telegram Agent API"}

@app.post("/groups")
async def create_group(request: CreateGroupRequest):
    client = app.state.client
    result = await utils.create_group(client, request.title, request.users)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create group")
    return {"status": "success", "group_id": result.id, "title": result.title}

@app.put("/groups/{chat_id}")
async def edit_group(chat_id: int, request: UpdateGroupRequest):
    client = app.state.client
    success = await utils.edit_group_title(client, chat_id, request.title)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to edit group title")
    return {"status": "success", "message": "Group title updated"}

@app.delete("/groups/{chat_id}")
async def delete_group(chat_id: int):
    client = app.state.client
    success = await utils.delete_group(client, chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete group")
    return {"status": "success", "message": "Group deleted"}

@app.post("/contacts")
async def add_contact(request: AddContactRequest):
    client = app.state.client
    result = await utils.add_contact(client, request.phone, request.first_name, request.last_name)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to add contact")
    return {"status": "success", "user_id": result.users[0].id if result.users else None}

@app.delete("/contacts/{user_id}")
async def remove_contact(user_id: int):
    client = app.state.client
    success = await utils.remove_contact(client, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove contact")
    return {"status": "success", "message": "Contact removed"}

@app.post("/messages/scrape")
async def scrape_messages(request: ScrapeRequest):
    client = app.state.client
    # Try to convert chat_id to int if it looks like one, otherwise keep as string (username)
    chat_entity = request.chat_id
    if chat_entity.lstrip('-').isdigit():
        chat_entity = int(chat_entity)

    messages = await utils.scrape_messages(client, chat_entity, limit=request.limit)
    return {"status": "success", "count": len(messages), "data": messages}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVER_PORT)
