from sqlalchemy import Column, Integer, String, Boolean
from src.infrastructure.data_handlers.database import db

class Car(db.Base):
    __tablename__ = "cars"

    stock_id = Column(Integer, primary_key=True, index=True)
    km = Column(Integer, index=True, nullable=True)
    price = Column(Integer, index=True, nullable=True)
    make = Column(String, index=True, nullable=True)
    model = Column(String, index=True, nullable=True)
    year = Column(Integer, index=True, nullable=True)
    version = Column(String, index=True, nullable=True)
    bluetooth = Column(Boolean, index=True, nullable=True)
    length = Column(Integer, index=True, nullable=True)
    width = Column(Integer, index=True, nullable=True)
    height = Column(Integer, index=True, nullable=True)
    car_play = Column(Boolean, index=True, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}