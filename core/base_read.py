from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Response
from .session import Speack, ConnectionManager
from rest_framework.authtoken.models import Token
from account.models import ChatSystem, Message
from asgiref.sync import sync_to_async
import google.generativeai as genai
import json
from decouple import config

config_file_path = "../.env"

api_key = config("ModelApiKey")

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


genai.configure(api_key=api_key)
gemini = genai.GenerativeModel("gemini-1.5-flash")


@router.websocket("/ws/chat")
async def chat_system(websocket: WebSocket, token: str):
    if token is None:
        await websocket.close(code=4001)

    # Get and check user from given token
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=4003)

    await manager.connect(websocket, user)
    # receives and broadcast message on websocket connection
    try:
        while True:
            chat = gemini.start_chat(history=None)
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You said: {data}", websocket, user)
            try:
                stream.feed(data)
                stream.play_async()
            except Exception as e:
                await manager.broadcast(f"Error occured when reading data", user)
                continue

            try:
                response = chat.send_message(data)
                try:
                    stream.feed(response.text)
                    await manager.broadcast(f"Client model says: {response.text}", user)
                    stream.play_async()
                except Exception as e:
                    await manager.broadcast(f"Error occured when reading data", user)
                    continue
            except Exception as e:
                await manager.broadcast(f"Error generating response from model", user)
                continue

    except WebSocketDisconnect:
        manager.disconnect(websocket, user)
        await manager.broadcast(f"Client #{user} has left the chat", user)
