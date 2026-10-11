import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api, { errMsg, inr } from "../api";
import AdvicePanel from "../components/AdvicePanel";
import ScoreGauge from "../components/ScoreGauge";

export default function Dashboard() {
  const [d, setD] = useState(null);
  const [state, setState] = useState("loading"); // loading | empty | error | ready
  const [err, setErr] = useState("");

  useEffect(() => {
    Promise.all([api.get("/financial-data"), api.get("/history"), api.get("/utilization")])
      .then(([fd, h, u]) => { setD({ fd: fd.data, h: h.data, u: u.data }); setState("ready"); })
      .catch((e) => { if (e.response?.status === 404) setState("empty"); else { setErr(errMsg(e)); setState("error"); } });
  }, []);

  if (state === "loading") return <p className="muted">Loading your dashboard…</p>;
  if (state === "error") return <p className="error" role="alert">{err}</p>;
  if (state === "empty") return (
    <section className="card">
      <h1>Add your financial details</h1>
      <p className="muted">Enter your score, income and debts to see your dashboard.</p>
      <Link className="btn" to="/data">Enter details</Link>
    </section>
  );

  const { fd, h, u } = d;
  const pts = h.map((x) => ({
    date: new Date(x.recorded_at + "Z").toLocaleDateString("en-IN", { day: "numeric", month: "short" }),
    score: x.credit_score,
  }));
  const pie = [{ name: "Debt used", value: u.used, c: u.utilization_pct > 30 ? "#B3261E" : "#0F7C86" },
               { name: "Limit available", value: u.available, c: "#D5DBE5" }];

  return (
    <>
      <section className="card"><ScoreGauge score={fd.credit_score} category={fd.category} delta={fd.improvement_delta} /></section>
      <section className="card">
        <h2>What is holding your score back</h2>
        {fd.alerts.length === 0 ? <p className="ok">No bottlenecks flagged. Keep paying on time.</p>
          : <ul className="alerts">{fd.alerts.map((a) => <li key={a}>{a}</li>)}</ul>}
        <p className="muted">Utilisation {fd.credit_utilization}% · Debt-to-income {fd.dti_ratio}%</p>
      </section>
      <div className="grid">
        <section className="card">
          <h2>Score over time</h2>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={pts}>
              <CartesianGrid stroke="#E3E8F0" vertical={false} />
              <XAxis dataKey="date" fontSize={12} />
              <YAxis domain={[300, 900]} fontSize={12} width={36} />
              <Tooltip />
              <Line type="monotone" dataKey="score" name="Score" stroke="#0F7C86" strokeWidth={3} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </section>
        <section className="card">
          <h2>Credit utilisation</h2>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={pie} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={2}>
                {pie.map((s) => <Cell key={s.name} fill={s.c} />)}
              </Pie>
              <Tooltip formatter={(x) => inr(x)} />
            </PieChart>
          </ResponsiveContainer>
          <p className="muted center">{inr(u.used)} used of {inr(u.used + u.available)}</p>
        </section>
      </div>
      <AdvicePanel />
    </>
  );
}
