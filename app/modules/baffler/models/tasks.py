# pylint: disable=E1136
from datetime import datetime

from sqlalchemy.orm import (
    mapped_column
)
from sqlalchemy import String, Integer, Boolean
from database.base import Base

# Base tables
class Tasks(Base):
    __tablename__ = "tasks"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    completed = mapped_column(Boolean, nullable=False, default=False)


    
    
    



    
    
    
    
    
    