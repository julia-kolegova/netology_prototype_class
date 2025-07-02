from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Literal
from datetime import datetime, date
import json
import os

app = FastAPI()

DATA_FILE = "abonents_data.json"

# ------------------ Pydantic Model ------------------
class AbonentRequest(BaseModel):
    last_name: str = Field(..., description="Фамилия")
    first_name: str = Field(..., description="Имя")
    birth_date: date
    phone_number: str
    email: EmailStr
    issue_reason: List[Literal['нет доступа к сети', 'не работает телефон', 'не приходят письма']] = []
    issue_datetime: datetime = None

    @validator('last_name', 'first_name')
    def validate_name(cls, value):
        if not value.istitle():
            raise ValueError('Имя и фамилия должны начинаться с заглавной буквы')
        if not value.isalpha():
            raise ValueError('Имя и фамилия должны содержать только буквы кириллицы')
        if not all('А' <= ch <= 'я' or ch == 'ё' or ch == 'Ё' for ch in value):
            raise ValueError('Имя и фамилия должны быть написаны на кириллице')
        return value

    @validator('phone_number')
    def validate_phone(cls, value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) != 11:
            raise ValueError('Номер телефона должен содержать 11 цифр')
        return value

@app.post("/submit")
async def submit_abonent(data: AbonentRequest):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
    else:
        saved_data = []

    saved_data.append(data.dict())

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(saved_data, f, ensure_ascii=False, indent=4)

    return {"status": "успешно", "data": data.dict()}
