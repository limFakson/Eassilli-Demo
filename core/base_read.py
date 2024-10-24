from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine
from fastapi import APIRouter
from .session import Speack

router = APIRouter()

engine = SystemEngine()
stream = TextToAudioStream(engine)


@router.post("/speak")
async def speak(text: Speack):
    stream.feed(text)
    await stream.play_async()
    return True
