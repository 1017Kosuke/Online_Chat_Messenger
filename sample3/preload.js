const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  sendToServer: (protocol, packet) => {
    return ipcRenderer.invoke("send-to-server", protocol, packet);
  },
});