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
  const table = "โต๊ะ 1";
  const logData = {
    device_id: deviceId,
    table: table,
    timestamp: new Date().toISOString()
  };

  // เปลี่ยน URL ด้านล่างให้ตรงกับ backend ที่จะทำ
  await fetch("http://localhost:5000/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(logData)
  });

  // เปลี่ยนเป็น Wongnai URL จริง
  setTimeout(() => {
    window.location.href = "https://mobile-order.wongnai.com/...";
  }, 2000);
})();
