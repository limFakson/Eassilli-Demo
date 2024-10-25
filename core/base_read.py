from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response
from .session import Speack, ConnectionManager
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async
import json

router = APIRouter()

engine = SystemEngine()
stream = TextToAudioStream(engine)


# Test on TTS library
@router.post("/speak")
async def speak(text: Speack):
    stream.feed(text)
    await stream.play_async()
    return True


manager = ConnectionManager()


async def get_user_from_token(token: str):
    try:
        # Fetch token from Django's Token model
        auth_token = await sync_to_async(Token.objects.get)(key=token)
        name = await sync_to_async(lambda: auth_token.user.username)()
        return name
    except Token.DoesNotExist:
        return None


@router.websocket("/ws/chat")
async def ChatSystem(websocket: WebSocket, token: str):
    if token is None:
        await websocket.close(code=4001)

    # Get and check user from given token
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=4003)

    await manager.connect(websocket)
    # receives and broadcast message on websocket connection
    try:
        while True:
            data = await websocket.receive_text()
            stream.feed(data)
            stream.play_async()
            await manager.broadcast(f"Client #{user} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user} has left the chat")
