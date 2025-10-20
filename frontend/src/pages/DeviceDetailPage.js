import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function DeviceDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState(null);
  

  const [newBattery, setNewBattery] = useState({
    name: "",
    nominal_voltage: "",
    residual_capacity: "",
    service_life: ""
  });

  const [editBatteryId, setEditBatteryId] = useState(null);

  useEffect(() => {
    fetchDevice();
  }, []);

  const fetchDevice = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/devices/${id}`);
      const data = await res.json();
      setDevice(data.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddOrUpdateBattery = async (e) => {
    e.preventDefault();
    try {
        let url = `http://127.0.0.1:8000/api/devices/${id}/batteries`;
        let method = "POST";

        if (editBatteryId) {
            url = `http://127.0.0.1:8000/api/batteries/${editBatteryId}`;
            method = "PATCH";
        }

        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newBattery)
        });

        if (!res.ok) throw new Error("Сохранить АКБ не удалось");

        setNewBattery({ name: "", nominal_voltage: "", residual_capacity: "", service_life: "" });
        setEditBatteryId(null);
        fetchDevice();
    } catch (err) {
        console.error(err);
        alert("Ошибка сохранения АКБ");
    }
};


  const handleDeleteBattery = async (batteryId) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/devices/${id}/batteries/${batteryId}`, {
        method: "DELETE"
      });

      if (!res.ok) throw new Error("Удаление АКБ не удалось");

      fetchDevice();
    } catch (err) {
      console.error(err);
      alert("Ошибка удаления АКБ");
    }
  };

  const handleEditBatteryClick = (battery) => {
    setEditBatteryId(battery.id);
    setNewBattery({
      name: battery.name,
      nominal_voltage: battery.nominal_voltage,
      residual_capacity: battery.residual_capacity,
      service_life: battery.service_life
    });
  };

  if (!device) return <div>Loading...</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "800px", margin: "0 auto" }}>
      <button
        onClick={() => navigate(-1)}
        style={{
          padding: "5px 10px",
          marginBottom: "20px",
          cursor: "pointer",
          borderRadius: "5px",
          border: "1px solid #888"
        }}
      >
        Назад
      </button>

      <h1>Имя АКБ: {device.name}</h1>
      <p><strong>Версия прошивки:</strong> {device.firmware_version}</p>
      <p><strong>Вкл/Выкл:</strong> {device.is_active ? "Вкл" : "Выкл"}</p>

      <h2>АКБ</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {device.batteries?.length > 0 ? (
          device.batteries.map((battery) => (
            <li
              key={battery.id}
              style={{
                border: "1px solid #ccc",
                padding: "10px",
                marginBottom: "10px",
                borderRadius: "5px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                backgroundColor: "#fafafa"
              }}
            >
              <span>
                {battery.name} - {battery.residual_capacity}% - {battery.nominal_voltage}V - {battery.service_life}d
              </span>
              <div>
                <button
                  onClick={() => handleEditBatteryClick(battery)}
                  style={{
                    padding: "5px 10px",
                    marginRight: "5px",
                    cursor: "pointer",
                    borderRadius: "5px",
                    border: "none",
                    backgroundColor: "#FFC107",
                    color: "#fff",
                  }}
                >
                  Редактировать
                </button>
                <button
                  onClick={() => handleDeleteBattery(battery.id)}
                  style={{
                    padding: "5px 10px",
                    cursor: "pointer",
                    borderRadius: "5px",
                    border: "none",
                    backgroundColor: "#f44336",
                    color: "#fff",
                  }}
                >
                  Уадлить
                </button>
              </div>
            </li>
          ))
        ) : (
          <li>АКБ остуствуют</li>
        )}
      </ul>

      <h3>{editBatteryId ? "Изменить АКБ" : "Добавить новую АКБ"}</h3>
      <form onSubmit={handleAddOrUpdateBattery} style={{ display: "flex", flexDirection: "column", gap: "10px", marginTop: "10px" }}>
        <input
          type="text"
          placeholder="Имя"
          value={newBattery.name}
          onChange={(e) => setNewBattery({ ...newBattery, name: e.target.value })}
          required
          style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
        />
        <input
          type="number"
          placeholder="Номинальное напряжение"
          value={newBattery.nominal_voltage}
          onChange={(e) => setNewBattery({ ...newBattery, nominal_voltage: parseFloat(e.target.value) })}
          required
          style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
        />
        <input
          type="number"
          placeholder="Остаточная емкость"
          value={newBattery.residual_capacity}
          onChange={(e) => setNewBattery({ ...newBattery, residual_capacity: parseFloat(e.target.value) })}
          required
          style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
        />
        <input
          type="number"
          placeholder="Срок службы (в днях)"
          value={newBattery.service_life}
          onChange={(e) => setNewBattery({ ...newBattery, service_life: parseInt(e.target.value) })}
          required
          style={{ padding: "8px", borderRadius: "5px", border: "1px solid #ccc" }}
        />
        <div style={{ display: "flex", gap: "10px" }}>
          <button
            type="submit"
            style={{ padding: "10px", cursor: "pointer", borderRadius: "5px", border: "1px solid #888", backgroundColor: "#4CAF50", color: "#fff" }}
          >
            {editBatteryId ? "Обновить АКБ" : "Добавить АКБ"}
          </button>
          {editBatteryId && (
            <button
              type="button"
              onClick={() => {
                setEditBatteryId(null);
                setNewBattery({ name: "", nominal_voltage: "", residual_capacity: "", service_life: "" });
              }}
              style={{ padding: "10px", cursor: "pointer", borderRadius: "5px", border: "1px solid #888", backgroundColor: "#f44336", color: "#fff" }}
            >
              Отмена
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default DeviceDetailPage;
