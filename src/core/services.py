import logging
import pandas as pd
from io import BytesIO
from sqlalchemy import or_
from fastapi import UploadFile
from typing import Union

from src.core.entities import Car
from src.core.prompts import company_info_prompt, identify_intent_prompt
from src.entrypoints.dtos import IntentData, ResponseHandler, ChatResponse
from src.infrastructure.data_handlers.llm import LLMHandler
from src.infrastructure.data_handlers.twilio import TwilioClient
from src.core.repositories import CarsDBRepository


class CarServices:
    def __init__(
        self,
        db_repo: CarsDBRepository
    ):
        self.db_repo = db_repo

    async def initialize_stock(self, file: UploadFile) -> None:
        if not file.filename.endswith(".csv"):
            raise Exception("File must be a CSV")
        
        contents = await file.read()
        df = self._process_file(contents)
        cars_data = df.to_dict(orient="records")
        
        try:
            self.db_repo.initialize_stock(cars_data)
        except Exception as e:
            raise e
        
        return {"message": "Cars added successfully"}
    
    def _process_file(self, contents: bytes) -> pd.DataFrame:
        df = pd.read_csv(BytesIO(contents))
        df = df.rename(
            columns={
                "largo": "length",
                "ancho": "width",
                "altura": "height",
            }
        )
        df["bluetooth"] = df["bluetooth"] == "Sí"
        df["car_play"] = df["car_play"] == "Sí"
        return df

    def get_cars_by_filter(self, intent_data: IntentData) -> Union[list, ChatResponse]:
        filter_exp = self.build_car_filter_exp(intent_data)
        cars = self.db_repo.get_cars_by_filter(filter_exp)
        if not cars:
            return ChatResponse(
                message="Lo siento, no encontré autos que coincidan con tus preferencias."
            )
        cars_data = [car.as_dict() for car in cars]
        return cars_data

    def build_car_filter_exp(self, intent_data: IntentData) -> list:
        filters = []
        preferences = intent_data.preferences.model_dump()
        for key, value in preferences.items():
            if value is not None:
                if key == "initial_payment":
                    continue
                if key == "price":
                    filters.append(getattr(Car, key) <= value)
                elif key == "km":
                    filters.append(getattr(Car, key) <= value)
                else:
                    filters.append(getattr(Car, key).ilike(value))

        if len(filters) > 1:
            return or_(*filters)
        return filters
    
    def calculate_financing(self, car: dict, initial_payment: int, years: list) -> list:
        financing_options = []
        price = car.get("price")
        financing_amount = max(0, price - initial_payment)
        monthly_interest_rate = 10 / 100 / 12

        for year in years:
            months = year * 12
            monthly_payment = (financing_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -months)
            
            total_payment = round(monthly_payment * months + initial_payment, 2)
            total_interest = round((monthly_payment * months) - financing_amount, 2)

            financing_options.append(
                {
                    "años": year,
                    "pago_inicial": initial_payment,
                    "total_pagado": total_payment,
                    "total_interes": total_interest 
                }
            )
        
        return [
            {
                "options": financing_options
            }
        ]
        

class ChatServices:
    def __init__(
        self,
        llm_handler: LLMHandler,
        car_services: CarServices,
        chat_handler: TwilioClient,
        response_handler: ResponseHandler,
        logger: logging.Logger
    ):
        self.llm_handler = llm_handler
        self.car_services = car_services
        self.chat_handler = chat_handler
        self.response_handler = response_handler
        self.logger = logger

    def identify_intent(self, message: str) -> dict:
        prompt = identify_intent_prompt(message)
        data = self.llm_handler.make_request(prompt=prompt)
        return IntentData(**data)
    
    def get_recommendations(self, intent_data: IntentData):
        cars_data = self.car_services.get_cars_by_filter(intent_data)

        if isinstance(cars_data, ChatResponse):
            return cars_data
        
        message = self.response_handler.recommendation_response(cars_data)
        return ChatResponse(
            message=message
        )

    def get_company_info(self, message: str) -> ChatResponse:
        prompt = company_info_prompt(message)
        data = self.llm_handler.make_request(prompt=prompt)

        return ChatResponse(
            message=data.get("response")
        )     
    
    def get_financing_info(self, intent_data: IntentData) -> ChatResponse:
        if not intent_data.preferences.initial_payment:
            return ChatResponse(
                message="Lo siento, no tengo información sobre financiamiento sin un pago inicial."
            )
        
        cars_data = self.car_services.get_cars_by_filter(intent_data)
        if isinstance(cars_data, ChatResponse):
            return cars_data
        
        financing_data = self.car_services.calculate_financing(
            cars_data[0],
            intent_data.preferences.initial_payment,
            [3,6]
        )

        message = self.response_handler.financing_response(
            car=cars_data[0],
            options=financing_data[0]["options"]
        )
        return ChatResponse(
            message=message
        )

    def process_intent(self, intent_data: IntentData, message: str) -> ChatResponse:
        if intent_data.intent == "recommendation":
            return self.get_recommendations(intent_data)
        if intent_data.intent == "financing":
            return self.get_financing_info(intent_data)
        if intent_data.intent == "company_info":
            return self.get_company_info(message)
        
        return "Lo siento, no entendí tu solicitud. Por favor, intenta de nuevo."
    
    def process_chat_request(self, message: str, to: str) -> str:
        intent_data = self.identify_intent(message)
        processed_message = self.process_intent(intent_data, message)
        
        self.chat_handler.send_message(
            to=to,
            body=processed_message.message
        )
        return processed_message.message
    