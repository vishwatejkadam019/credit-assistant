from datetime import datetime, timezone
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from .database import Base


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=now)


class FinancialData(Base):
    __tablename__ = "financial_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    credit_score = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    monthly_debt_payment = Column(Float, nullable=False)  # added: needed for DTI
    total_debt = Column(Float, nullable=False)
    credit_limit = Column(Float, nullable=False)
    credit_utilization = Column(Float, nullable=False)
    dti_ratio = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now)


class ScoreHistory(Base):
    __tablename__ = "score_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    credit_score = Column(Integer, nullable=False)
    recorded_at = Column(DateTime, default=now)
    improvement_delta = Column(Integer, default=0)


class AIAdvice(Base):
    __tablename__ = "ai_advice"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    category = Column(String(20))
    analysis = Column(Text, nullable=False)
    action_plan = Column(JSON, nullable=False)
    source = Column(String(20), default="gemini")
    created_at = Column(DateTime, default=now)
