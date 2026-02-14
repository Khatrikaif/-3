from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Local Minimal Chat")

MAX_MESSAGES_PER_ROOM = 200
rooms: Dict[str, List[dict]] = defaultdict(list)


class JoinPayload(BaseModel):
    room: str = Field(min_length=1, max_length=32)
    username: str = Field(min_length=1, max_length=32)


class MessagePayload(BaseModel):
    room: str = Field(min_length=1, max_length=32)
    username: str = Field(min_length=1, max_length=32)
    text: str = Field(min_length=1, max_length=500)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def add_message(room: str, username: str, text: str, system: bool = False) -> None:
    item = {
        "id": len(rooms[room]) + 1,
        "username": username,
        "text": text,
        "time": now_iso(),
        "system": system,
    }
    rooms[room].append(item)
    if len(rooms[room]) > MAX_MESSAGES_PER_ROOM:
        rooms[room] = rooms[room][-MAX_MESSAGES_PER_ROOM:]


@app.get("/")
def home() -> FileResponse:
    return FileResponse("index.html")


@app.post("/api/join")
def join(payload: JoinPayload):
    room = payload.room.strip().lower()
    username = payload.username.strip()
    add_message(room, "system", f"{username} joined the room", system=True)
    return {"ok": True, "room": room, "username": username}


@app.get("/api/messages")
def get_messages(room: str, after: int = 0):
    room_key = room.strip().lower()
    if not room_key:
        raise HTTPException(status_code=400, detail="room is required")
    msgs = [m for m in rooms[room_key] if m["id"] > after]
    return {"messages": msgs}


@app.post("/api/messages")
def post_message(payload: MessagePayload):
    room = payload.room.strip().lower()
    username = payload.username.strip()
    text = payload.text.strip()
    add_message(room, username, text)
    return {"ok": True}
