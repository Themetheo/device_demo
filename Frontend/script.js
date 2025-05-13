(async () => {
  function getDeviceId() {
    let id = localStorage.getItem("device_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("device_id", id);
    }
    return id;
  }

  const deviceId = getDeviceId();

  // 📌 ดึง table id จาก URL เช่น ?table=3
  const params = new URLSearchParams(window.location.search);
  const tableId = params.get("table") || "13"; // ถ้าไม่มี → โต๊ะ 13
  const tableName = `โต๊ะ ${tableId}`;

  const logData = {
    device_id: deviceId,
    table: tableName,
    timestamp: new Date().toISOString()
  };

  // ✅ ส่ง log ไป backend
  try {
    await fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logData)
    });
  } catch (err) {
    console.warn("❌ ไม่สามารถส่ง log ได้:", err);
  }

  // ✅ ขอ URL redirect จาก backend
  try {
    const res = await fetch(`http://127.0.0.1:5000/get-url/${tableId}`);
    const result = await res.json();

    if (result.url) {
      document.body.innerHTML = `<h2>✅ กำลังพาไปยังเมนูของ ${tableName}...</h2>`;
      setTimeout(() => {
        window.location.href = result.url;
      }, 2000);
    } else {
      document.body.innerHTML = `<h2>❌ ไม่พบ URL สำหรับ ${tableName}</h2>`;
    }
  } catch (err) {
    document.body.innerHTML = `<h2>❌ เกิดข้อผิดพลาดขณะโหลด URL: ${err.message}</h2>`;
  }
})();
let redirected = false;

(async () => {
  function getDeviceId() {
    let id = localStorage.getItem("device_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("device_id", id);
    }
    return id;
  }

  const deviceId = getDeviceId();
  const params = new URLSearchParams(window.location.search);
  const tableId = params.get("table") || "13";
  const tableName = `โต๊ะ ${tableId}`;

  const logData = {
    device_id: deviceId,
    table: tableName,
    timestamp: new Date().toISOString()
  };

  try {
    await fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logData)
    });
  } catch (err) {
    console.warn("❌ ไม่สามารถส่ง log ได้:", err);
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/get-url/${tableId}`);
    const result = await res.json();

    if (result.url && !redirected) {
      redirected = true;
      document.body.innerHTML = `<h2>✅ กำลังพาไปยังเมนูของ ${tableName}...</h2>`;
      setTimeout(() => {
        window.location.href = result.url;
      }, 2000);
    } else {
      document.body.innerHTML = `<h2>❌ ไม่พบ URL สำหรับ ${tableName}</h2>`;
    }
  } catch (err) {
    document.body.innerHTML = `<h2>❌ เกิดข้อผิดพลาดขณะโหลด URL: ${err.message}</h2>`;
  }

  // ✅ Heartbeat
  setInterval(() => {
    fetch("http://127.0.0.1:5000/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        device_id: deviceId,
        table: tableName,
        event: "heartbeat",
        timestamp: new Date().toISOString()
      })
    }).catch((err) => {
      console.warn("❌ ไม่สามารถส่ง heartbeat ได้:", err);
    });
  }, 5 * 60 * 1000);
})();
