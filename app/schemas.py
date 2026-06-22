from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List, Literal, Optional
from datetime import datetime

class UserInfo(BaseModel):
    name: str = Field(..., description="ФИО пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    phone: str = Field(..., description="Телефон пользователя", min_length=10)

class SubmitDataIn(BaseModel):
    name: str = Field(..., description="Название перевала")
    latitude: float = Field(..., description="Широта (координата)")
    longitude: float = Field(..., description="Долгота (координата)")
    altitude_m: int = Field(..., description="Высота в метрах", ge=0)
    photos: List[str] = Field(default_factory=list, description="Список ссылок на фотографии")
    user_info: UserInfo

class SubmitDataOut(BaseModel):
    status: int = 200
    message: str = "Отправлено успешно"
    id: int | None = None

class ErrorResponse(BaseModel):
    status: int
    message: str

class PassOut(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    altitude_m: int
    photos: List[str]
    user_info: UserInfo
    status: Literal["new", "pending", "accepted", "rejected"]
    created_at: datetime

class PatchResult(BaseModel):
    state: Literal[0, 1]
    message: Optional[str] = None

class PartialSubmitDataIn(SubmitDataIn):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    altitude_m: int | None = None
    photos: List[str] | None = None
    user_info: UserInfo | None = None

    @model_validator(mode='before')
    def clean_none(cls, values):
        return {k: v for k, v in values.items() if v is not None}