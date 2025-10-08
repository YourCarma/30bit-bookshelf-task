from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class Kind(Enum):
    BOOK = "book"
    ARTICLE = "article"
    
class Status(Enum):
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"
    
class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    