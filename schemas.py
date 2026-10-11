from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FinancialIn(BaseModel):
    credit_score: int = Field(ge=300, le=900)
    monthly_income: float = Field(gt=0)
    monthly_expenses: float = Field(ge=0)
    monthly_debt_payment: float = Field(ge=0)
    total_debt: float = Field(ge=0)
    credit_limit: float = Field(ge=0)


class FinancialOut(FinancialIn):
    credit_utilization: float
    dti_ratio: float
    updated_at: datetime
    category: str
    improvement_delta: int
    alerts: List[str]


class HistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    credit_score: int
    recorded_at: datetime
    improvement_delta: int


class AdviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category: str
    analysis: str
    action_plan: List[str]
    source: str
    created_at: datetime
