"""Pure credit calculations (no DB), so they are easy to test."""
from typing import Optional


def dti(monthly_debt_payment: float, monthly_income: float) -> float:
    """Debt-to-income % = monthly debt payments / monthly income x 100."""
    return round(monthly_debt_payment / monthly_income * 100, 2) if monthly_income > 0 else 0.0


def utilization(total_debt: float, credit_limit: float) -> float:
    """Utilisation % = total debt / credit limit x 100."""
    if credit_limit <= 0:
        return 0.0 if total_debt <= 0 else 100.0
    return round(total_debt / credit_limit * 100, 2)


def category(score: int) -> str:
    """CIBIL-style bands (assumption): <600 Poor, 600-699 Fair, 700-749 Good, 750+ Excellent."""
    return "Poor" if score < 600 else "Fair" if score < 700 else "Good" if score < 750 else "Excellent"


def delta(previous: Optional[int], current: int) -> int:
    """Change versus the previous recorded score (0 for the first record)."""
    return 0 if previous is None else current - previous
