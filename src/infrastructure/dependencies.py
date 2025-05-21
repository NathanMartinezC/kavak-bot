import logging
from src.infrastructure.data_handlers.database import db
from src.infrastructure.data_handlers.llm import LLMHandler
from src.infrastructure.data_handlers.twilio import TwilioClient
from src.data_sources.sql import SQLCarsRepo
from src.core.services import CarServices
from src.core.services import ChatServices
from src.entrypoints.dtos import ResponseHandler

logger = logging.getLogger(__name__)

class GlobalDependencies:
    def __init__(self):
        self.logger = logger
        self.db = db


class ChatBotDependencies(GlobalDependencies):
    def __init__(self):
        super().__init__()
        self.cars_repo = SQLCarsRepo(self.db)
        self.car_services = CarServices(self.cars_repo)
        self.llm_handler = LLMHandler()
        self.chat_handler = TwilioClient()
        self.response_handler = ResponseHandler()
        self.chat_services = ChatServices(
            self.llm_handler,
            self.car_services,
            self.chat_handler,
            self.response_handler,
            self.logger
        )

    def get_car_services(self):
        return self.car_services
    
    def get_chat_services(self):
        return self.chat_services
    


chatbot_dependencies = ChatBotDependencies()


