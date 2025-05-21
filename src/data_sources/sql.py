import pandas as pd
from fastapi import UploadFile
from sqlalchemy import select
from src.core.repositories import CarsDBRepository
from src.core.entities import Car

class SQLCarsRepo(CarsDBRepository):
    def __init__(self, db):
        self.db = db

    def initialize_stock(self, data):
        self.db.init_db()
        with self.db.get_db() as db:
            db.bulk_insert_mappings(Car, data)
            db.commit()

    def get_cars_by_filter(self, filters: list):
        with self.db.get_db() as db:
            stmt = select(Car).where(*filters).distinct().order_by(Car.year.desc())
            result = db.execute(stmt).scalars().all()
            return result