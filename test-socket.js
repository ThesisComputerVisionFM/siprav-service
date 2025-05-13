// test-socket.js
const io = require("socket.io-client");

const socket = io("http://localhost:8000");

socket.on("connect", () => {
  console.log("✅ Conectado al backend");
});

socket.on("alerts", (data) => {
  console.log("🚨 Alertas recibidas:", data);
});

socket.on("cameras", (data) => {
  console.log("📷 Cámaras recibidas:", data);
});

socket.on("disconnect", () => {
  console.log("❌ Desconectado");
});
