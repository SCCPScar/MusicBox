const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("farmPlayer", {
  closeWindow: () => ipcRenderer.send("window:close"),
  minimizeWindow: () => ipcRenderer.send("window:minimize"),
});
