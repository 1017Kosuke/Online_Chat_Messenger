const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const net = require("net");
const dgram = require("dgram");

const TCP_PORT = 9000;
const UDP_PORT = 9001;
const HOST = "127.0.0.1";

function createWindow() {
  const win = new BrowserWindow({
    width: 900,
    height: 750,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadFile(path.join(__dirname, "./src/index.html"));
}

function sendByTcp(packet) {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    const message = JSON.stringify(packet);

    client.connect(TCP_PORT, HOST, () => {
      client.write(message);
    });

    client.on("data", (data) => {
      resolve(data.toString());
      client.destroy();
    });

    client.on("error", (err) => {
      reject(err.message);
    });

    client.on("close", () => {
      client.destroy();
    });
  });
}

function sendByUdp(packet) {
  return new Promise((resolve, reject) => {
    const client = dgram.createSocket("udp4");

    const message = Buffer.from(
      JSON.stringify(packet)
    );

    const timeout = setTimeout(() => {
      client.close();
      reject("UDP server response timeout");
    }, 3000);

    client.send(message, UDP_PORT, HOST, (err) => {
      if (err) {
        clearTimeout(timeout);

        client.close();
        reject(err.message);
      }
    });

    client.on("message", (msg) => {
      clearTimeout(timeout);

      resolve(msg.toString());

      client.close();
    });

    client.on("error", (err) => {
      clearTimeout(timeout);

      client.close();

      reject(err.message);
    });
  });
}

ipcMain.handle("send-to-server", async (event, protocol, packet) => {
  if (protocol === "tcp") {
    return await sendByTcp(packet);
  }

  if (protocol === "udp") {
    return await sendByUdp(packet);
  }

  throw new Error("Invalid protocol");
});

app.whenReady().then(createWindow);