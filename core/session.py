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
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
