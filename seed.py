"""Demo data: python seed.py  ->  login demo@creditassistant.in / Demo@1234"""
from datetime import timedelta
from app import calc
from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import FinancialData, ScoreHistory, User, now

Base.metadata.create_all(engine)
db = SessionLocal()
if db.query(User).filter_by(email="demo@creditassistant.in").first():
    raise SystemExit("Demo user already exists.")
u = User(name="Demo User", email="demo@creditassistant.in", hashed_password=hash_password("Demo@1234"))
db.add(u)
db.flush()
scores, prev = [596, 612, 625, 641, 658, 672, 688], None
for i, s in enumerate(scores):
    db.add(ScoreHistory(user_id=u.id, credit_score=s, recorded_at=now() - timedelta(days=30 * (len(scores) - 1 - i)),
                        improvement_delta=calc.delta(prev, s)))
    prev = s
inc, emi, debt, lim = 85000, 28000, 240000, 300000
db.add(FinancialData(user_id=u.id, credit_score=688, monthly_income=inc, monthly_expenses=52000, monthly_debt_payment=emi,
                     total_debt=debt, credit_limit=lim, credit_utilization=calc.utilization(debt, lim), dti_ratio=calc.dti(emi, inc)))
db.commit()
print("Seeded demo user.")
