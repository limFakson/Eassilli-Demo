import os
import django
from django.conf import settings
from pydantic import BaseModel
from fastapi import WebSocket

# Django settings environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

# Initialise django
django.setup()


class UserModel(BaseModel):
    identifier: str
    password: str


class RegisterUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    userName: str
    isStudent: bool
    field: str
    password: str


class Speack(BaseModel):
    text: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, name):
        await websocket.accept()
        if name not in self.active_connections:
            self.active_connections[name] = []
        self.active_connections[name].append(websocket)

    def disconnect(self, websocket: WebSocket, name):
        self.active_connections[name].remove(websocket)
        if not self.active_connections[name]:
            del self.active_connections[name]

    async def broadcast(self, message: str, name):
        for connection in self.active_connections[name]:
            await connection.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket, name: str):
        if name in self.active_connections:
            for websocket in self.active_connections[name]:
                await websocket.send_text(message)
