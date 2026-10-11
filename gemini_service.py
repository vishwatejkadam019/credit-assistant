"""Gemini advice with a rule-based fallback so the app still works offline."""
import json
import logging
import os
from . import calc

log = logging.getLogger("gemini")
PROMPT = """You are a credit advisor for the Indian financial system (CIBIL scale 300-900, RBI guidelines).
User metrics (INR): {m}
Reply with ONLY JSON: {{"analysis": "3-4 sentence assessment of their credit health", "action_plan": [exactly 5 short, specific steps]}}
Make the steps specific to Indian banking: CIBIL report checks and disputes, RBI norms, on-time EMI and UPI Autopay habits,
secured credit cards against a fixed deposit, keeping utilisation under 30%, avoiding many loan enquiries. No guarantees."""


def _fallback(m: dict) -> dict:
    u, d, s = m["credit_utilization"], m["dti_ratio"], m["credit_score"]
    plan = [
        f"Cut credit utilisation from {u:.0f}% to under 30%: pay down balances before the statement date." if u > 30
        else "Keep utilisation under 30% of your limit; ask for a limit increase rather than spending more.",
        "Pay every EMI and card bill by the due date. Turn on UPI Autopay or bank auto-debit so nothing slips.",
        f"Your EMIs take {d:.0f}% of income. Prepay the costliest loan or consolidate to get under 40%." if d > 40
        else "Your EMI burden is healthy. Avoid taking new loans until your score improves.",
        "If your score is low or history is thin, take a secured card against a fixed deposit and repay it in full monthly."
        if s < 700 else "Keep your oldest cards open: a long credit history supports a score above 750.",
        "Download your free annual CIBIL report, dispute any errors, and avoid applying to several lenders within a few months.",
    ]
    return {"analysis": f"Your score of {s} is rated {calc.category(s)}. Utilisation is {u:.0f}% and EMIs take {d:.0f}% of income. "
                        "Steady on-time payments and lower utilisation are the fastest levers.",
            "action_plan": plan, "source": "fallback"}


def get_advice(m: dict) -> dict:
    out = {"category": calc.category(m["credit_score"])}
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return {**out, **_fallback(m)}
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
                                      generation_config={"response_mime_type": "application/json", "temperature": 0.4})
        data = json.loads(model.generate_content(PROMPT.format(m=json.dumps(m))).text)
        plan = [str(x) for x in data["action_plan"]]
        if len(plan) != 5:
            raise ValueError("expected 5 steps")
        return {**out, "analysis": str(data["analysis"]), "action_plan": plan, "source": "gemini"}
    except Exception:
        log.exception("Gemini call failed; using fallback advice")
        return {**out, **_fallback(m)}
