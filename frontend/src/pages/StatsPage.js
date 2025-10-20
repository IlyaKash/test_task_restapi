import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function StatsPage() {
  const navigate = useNavigate();
  const [needReplacement, setNeedReplacement] = useState([]);
  const [lowCapacity, setLowCapacity] = useState([]);
  const [summary, setSummary] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/batteries/alerts/need_replacment")
      .then(res => res.json())
      .then(setNeedReplacement)
      .catch(err => console.error(err));

    fetch("http://127.0.0.1:8000/api/batteries/alerts/low_capacity")
      .then(res => res.json())
      .then(setLowCapacity)
      .catch(err => console.error(err));

    fetch("http://127.0.0.1:8000/api/batteries/stats/summary")
      .then(res => res.json())
      .then(setSummary)
      .catch(err => console.error(err));
  }, []);

  const cardStyle = {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "15px",
    marginBottom: "10px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
  };

  const sectionTitleStyle = {
    marginTop: "30px",
    marginBottom: "15px",
    color: "#333",
    borderBottom: "2px solid #2196F3",
    paddingBottom: "5px"
  };

  return (
    <div style={{ padding: "30px", fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", maxWidth: "1000px", margin: "0 auto" }}>
      <button
        onClick={() => navigate("/")}
        style={{
          padding: "10px 20px",
          marginBottom: "30px",
          borderRadius: "5px",
          border: "none",
          cursor: "pointer",
          backgroundColor: "#2196F3",
          color: "#fff",
          fontWeight: "bold",
          boxShadow: "0 2px 5px rgba(0,0,0,0.2)"
        }}
      >
        Назад к устройствам
      </button>

      <h1 style={{ textAlign: "center", marginBottom: "40px", color: "#333" }}>Статистика батарей</h1>

      <h2 style={sectionTitleStyle}>Общая статистика</h2>
      {Object.keys(summary).length > 0 ? (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "15px" }}>
          {Object.entries(summary).map(([key, value]) => (
            <div key={key} style={{ ...cardStyle, flex: "1 1 200px", textAlign: "center" }}>
              <strong>{key}</strong>
              <p style={{ fontSize: "18px", marginTop: "5px", color: "#555" }}>{value}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>Нет данных</p>
      )}

      <h2 style={sectionTitleStyle}>Батареи с низкой емкостью</h2>
      {lowCapacity.length > 0 ? (
        <div>
          {lowCapacity.map(b => (
            <div key={b.id} style={{ ...cardStyle, borderLeft: "5px solid #FF9800" }}>
              <strong>{b.name}</strong> — Остаток: <span style={{ color: "#FF5722" }}>{b.residual_capacity}%</span>
            </div>
          ))}
        </div>
      ) : (
        <p>Нет батарей с низкой емкостью</p>
      )}

      <h2 style={sectionTitleStyle}>Батареи требующие замены</h2>
      {needReplacement.length > 0 ? (
        <div>
          {needReplacement.map(b => (
            <div key={b.id} style={{ ...cardStyle, borderLeft: "5px solid #f44336", backgroundColor: "#fff0f0" }}>
              <strong>{b.name}</strong> — Остаток: <span style={{ color: "#d32f2f" }}>{b.residual_capacity}%</span> | Срок службы: {b.service_life} дней
            </div>
          ))}
        </div>
      ) : (
        <p>Нет батарей, требующих замены</p>
      )}
    </div>
  );
}
