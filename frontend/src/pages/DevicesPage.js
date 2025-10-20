import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function DevicesPage() {
  const [devices, setDevices] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newDeviceName, setNewDeviceName] = useState("");
  const [newFirmware, setNewFirmware] = useState("");
  const [newIsActive, setNewIsActive] = useState(true);
  const [editDeviceId, setEditDeviceId] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/devices/");
      const data = await res.json();
      setDevices(data.devices || []);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteDevice = async (deviceId) => {
    if (!window.confirm("Are you sure you want to delete this device?")) return;
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/devices/${deviceId}`, {
        method: "DELETE",
      });
      if (res.ok) setDevices(devices.filter((d) => d.id !== deviceId));
      else alert("Failed to delete device");
    } catch (err) {
      console.error(err);
      alert("Error deleting device");
    }
  };

  const addOrUpdateDevice = async () => {
    if (!newDeviceName) return alert("Name is required");
    try {
      let url = "http://127.0.0.1:8000/api/devices/";
      let method = "POST";

      if (editDeviceId) {
        url += `${editDeviceId}`;
        method = "PATCH";
      }

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: newDeviceName,
          firmware_version: newFirmware,
          is_active: newIsActive,
        }),
      });

      if (!res.ok) throw new Error("Failed to save device");

      await fetchDevices();
      setNewDeviceName("");
      setNewFirmware("");
      setNewIsActive(true);
      setShowForm(false);
      setEditDeviceId(null);
    } catch (err) {
      console.error(err);
      alert("Error saving device");
    }
  };

  const handleEditClick = (device) => {
    setEditDeviceId(device.id);
    setNewDeviceName(device.name);
    setNewFirmware(device.firmware_version);
    setNewIsActive(device.is_active);
    setShowForm(true);
  };

  return (
    <div style={{ padding: "30px", fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", maxWidth: "1200px", margin: "0 auto" }}>
    <h1 style={{ textAlign: "center", marginBottom: "20px", color: "#333" }}>Devices Dashboard</h1>

    {/* Блок кнопок сверху */}
    <div style={{ textAlign: "center", marginBottom: "30px", display: "flex", justifyContent: "center", gap: "15px", flexWrap: "wrap" }}>
    {/* Кнопка статистики */}
        <button
            onClick={() => navigate("/statistics")}
            style={{
                background: "linear-gradient(90deg, #673AB7, #512DA8)",
                color: "#fff",
                border: "none",
                padding: "12px 25px",
                borderRadius: "25px",
                cursor: "pointer",
                fontWeight: "bold",
                fontSize: "16px",
                boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
                transition: "all 0.3s ease",
                display: "inline-flex",
                alignItems: "center",
                gap: "8px"
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform = "scale(1.05)";
                e.currentTarget.style.boxShadow = "0 6px 12px rgba(0,0,0,0.3)";
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform = "scale(1)";
                e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
            }}
        >
            📊 Статистика
        </button>

        {/* Кнопка добавления устройства */}
        {!showForm && (
            <button
                onClick={() => setShowForm(true)}
                style={{
                    background: "linear-gradient(90deg, #4CAF50, #388E3C)",
                    color: "#fff",
                    border: "none",
                    padding: "12px 25px",
                    borderRadius: "25px",
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontSize: "16px",
                    boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
                    transition: "all 0.3s ease",
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "scale(1.05)";
                    e.currentTarget.style.boxShadow = "0 6px 12px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "scale(1)";
                    e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
                }}
                >
                ➕ Добавить устройство
            </button>
        )}
    </div>

      {/* Форма добавления/редактирования */}
      <div style={{ marginBottom: "30px", textAlign: "center" }}>
        {showForm && (
          <div
            style={{
              display: "inline-block",
              marginTop: "20px",
              padding: "20px",
              border: "1px solid #ccc",
              borderRadius: "8px",
              boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
              backgroundColor: "#f9f9f9",
              minWidth: "320px",
            }}
          >
            <input
              type="text"
              placeholder="Имя устройства"
              value={newDeviceName}
              onChange={(e) => setNewDeviceName(e.target.value)}
              style={{ display: "block", marginBottom: "10px", width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
            />
            <input
              type="text"
              placeholder="Версия прошивки"
              value={newFirmware}
              onChange={(e) => setNewFirmware(e.target.value)}
              style={{ display: "block", marginBottom: "10px", width: "100%", padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
            />
            <label style={{ display: "block", marginBottom: "10px", fontWeight: "bold" }}>
              Active:
              <input
                type="checkbox"
                checked={newIsActive}
                onChange={(e) => setNewIsActive(e.target.checked)}
                style={{ marginLeft: "10px", transform: "scale(1.2)" }}
              />
            </label>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <button
                onClick={addOrUpdateDevice}
                style={{
                  backgroundColor: "#2196F3",
                  color: "#fff",
                  border: "none",
                  padding: "8px 16px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  fontWeight: "bold",
                }}
              >
                {editDeviceId ? "Обновить" : "Создать"}
              </button>
              <button
                onClick={() => {
                  setShowForm(false);
                  setEditDeviceId(null);
                  setNewDeviceName("");
                  setNewFirmware("");
                  setNewIsActive(true);
                }}
                style={{
                  backgroundColor: "#f44336",
                  color: "#fff",
                  border: "none",
                  padding: "8px 16px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  fontWeight: "bold",
                }}
              >
                Отмена
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Список устройств */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "20px" }}>
        {devices.map((device) => (
          <div
            key={device.id}
            style={{
              border: "1px solid #ddd",
              padding: "15px",
              borderRadius: "10px",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
              backgroundColor: "#fff",
              transition: "transform 0.2s, box-shadow 0.2s",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-4px)";
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
            }}
          >
            <div onClick={() => navigate(`/device/${device.id}`)} style={{ cursor: "pointer" }}>
              <h3 style={{ margin: "0 0 10px 0", color: "#333" }}>{device.name}</h3>
              <p style={{ margin: "5px 0" }}>Версия прошивки: <strong>{device.firmware_version}</strong></p>
              <p style={{ margin: "5px 0" }}>Вкл/Выкл: <strong>{device.is_active ? "Вкл" : "Выкл"}</strong></p>
              <p style={{ margin: "5px 0" }}>АКБ:</p>
              <ul style={{ paddingLeft: "20px", margin: "5px 0" }}>
                {device.batteries?.length ? device.batteries.map((battery) => (
                  <li key={battery.id}>{battery.name}</li>
                )) : <li>Нет АКБ</li>}
              </ul>
            </div>
            <div style={{ marginTop: "10px", display: "flex", justifyContent: "space-between" }}>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleEditClick(device);
                }}
                style={{
                  backgroundColor: "#FFC107",
                  border: "none",
                  padding: "5px 10px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  fontWeight: "bold",
                  color: "#fff"
                }}
              >
                Редактировать
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteDevice(device.id);
                }}
                style={{
                  backgroundColor: "#f44336",
                  border: "none",
                  padding: "5px 10px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  fontWeight: "bold",
                  color: "#fff"
                }}
              >
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DevicesPage;
