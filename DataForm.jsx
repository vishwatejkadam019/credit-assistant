import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { errMsg } from "../api";

const FIELDS = [
  ["credit_score", "Credit score (300–900)", 300, 900],
  ["monthly_income", "Monthly income (₹)", 1],
  ["monthly_expenses", "Monthly expenses (₹)", 0],
  ["monthly_debt_payment", "Monthly EMIs and card payments (₹)", 0],
  ["total_debt", "Total outstanding debt (₹)", 0],
  ["credit_limit", "Total credit limit (₹)", 0],
];

export default function DataForm() {
  const nav = useNavigate();
  const [v, setV] = useState(Object.fromEntries(FIELDS.map(([k]) => [k, ""])));
  const [exists, setExists] = useState(false);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.get("/financial-data").then(({ data }) => {
      setExists(true);
      setV(Object.fromEntries(FIELDS.map(([k]) => [k, data[k]])));
    }).catch(() => {});
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setErr(""); setBusy(true);
    const body = Object.fromEntries(FIELDS.map(([k]) => [k, Number(v[k])]));
    try {
      await (exists ? api.put : api.post)("/financial-data", body);
      nav("/"); // dashboard reloads charts on mount
    } catch (x) { setErr(errMsg(x)); } finally { setBusy(false); }
  };

  return (
    <form className="card form" onSubmit={submit}>
      <h1>{exists ? "Update your details" : "Your financial details"}</h1>
      <p className="muted">We calculate your debt-to-income ratio and credit utilisation from these.</p>
      {FIELDS.map(([k, label, min, max]) => (
        <label key={k}>{label}
          <input required type="number" inputMode="decimal" step="any" min={min} max={max}
            value={v[k]} onChange={(e) => setV({ ...v, [k]: e.target.value })} />
        </label>
      ))}
      {err && <p className="error" role="alert">{err}</p>}
      <button className="btn" disabled={busy}>{busy ? "Saving…" : "Save details"}</button>
    </form>
  );
}
