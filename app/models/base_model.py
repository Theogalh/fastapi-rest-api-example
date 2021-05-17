from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.models import PyObjectId


class BasicModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    creation_datetime: datetime = None
    modification_datetime: datetime = None

    @validator("creation_datetime", pre=True, always=True)
    def default_creation_datetime(cls, v, values, **kwargs) -> datetime:
        return v or datetime.now()

    @validator("modification_datetime", pre=True, always=True)
    def default_modification_datetime(cls, v, values, **kwargs) -> datetime:
        return v or datetime.now()
