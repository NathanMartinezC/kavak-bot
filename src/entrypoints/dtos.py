from typing import Optional
from pydantic import BaseModel

class ChatResponse(BaseModel):
    message: str

class CarPreferences(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[int] = None
    km: Optional[int] = None
    bluetooth: Optional[bool] = None
    car_play: Optional[bool] = None
    initial_payment: Optional[int] = None

class IntentData(BaseModel):
    intent: str
    preferences: Optional[CarPreferences] = None


class ResponseHandler:
    def recommendation_response(self, data: list) -> str:
        if not data:
            return "Lo siento, no encontré autos que coincidan con tus preferencias."
        
        message = "Aquí tienes algunas recomendaciones de autos según tus preferencias:"
        for car in data:
            message += f"\n\n{car['make']} {car['model']} {car['year']} {car['version']}"
            message += f"\nStock ID: {car['stock_id']}"
            message += f"\nPrecio: {car['price']}"
            message += f"\nKilometraje: {car['km']}"
            message += f"\nBluetooth: {'Sí' if car['bluetooth'] else 'No'}"
            message += f"\nCarPlay: {'Sí' if car['car_play'] else 'No'}"
        return message
    
    def financing_response(self, car: dict, options: list) -> str:
        message = f"Aquí tienes opciones de financiamiento para un {car['make']} {car['model']} {car['year']} {car['version']}:"
        for option in options:
            message += f"\n\nAños: {option['años']}"
            message += f"\nPago inicial: {option['pago_inicial']}"
            message += f"\nTotal pagado: {option['total_pagado']}"
            message += f"\nTotal interés: {option['total_interes']}"
        return message
    
    
    
    