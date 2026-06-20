from pydantic import BaseModel, EmailStr, Field
from typing import List

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