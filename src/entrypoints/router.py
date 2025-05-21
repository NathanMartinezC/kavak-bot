from fastapi import APIRouter, UploadFile, Request, Form
from fastapi.responses import PlainTextResponse

from src.infrastructure.dependencies import chatbot_dependencies


router = APIRouter()

car_services = chatbot_dependencies.get_car_services()
chat_services = chatbot_dependencies.get_chat_services()

@router.post("/chat")
async def root(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
) -> PlainTextResponse:
    try:
        chat_services.process_chat_request(Body, From)
    except Exception as e:
        return PlainTextResponse(
            content="Lo siento, no pude procesar tu solicitud.",
            media_type="text/plain"
        )

@router.post("/init-db")
async def init(file: UploadFile):
    return await car_services.initialize_stock(file)