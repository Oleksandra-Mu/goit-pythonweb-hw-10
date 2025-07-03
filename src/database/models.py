from sqlalchemy import Column, Integer, String, DateTime
from src.database.db import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    date_of_birth = Column(DateTime, nullable=False)
    additional_info = Column(String(500), nullable=True)
