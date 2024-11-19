'use strict'

const { ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');
import { app, protocol, BrowserWindow } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
      preload: path.join(__dirname, 'preload.js')  // Ensure this path is correct
    }
  });

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol('app');
    win.loadURL('app://./index.html');
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}

ipcMain.on('toMain', (event, args) => {
  console.log(args);
  switch(args['command']){
  case 'sign-in':
    console.log('sign-in api call for subjectId:', args['subjectId']);
    break;

  case 'set-ecg-device':
    console.log('make api call');
    break;

  case 'start-signal-quality-check':
    console.log('starting signal quality check using', args['device'], 'ecg device...');
    break;

  case 'start-baseline':
    console.log('starting baseline script for subjectId "' + args['subjectId'] + '" using', args['device'], 'ecg device...');
    startBaselineScript(args.subjectId, args.device);
    break;

  case 'stop-baseline':
    console.log('stop baseline script');
    break;

  default:
    console.log('no command given')
  }
  

  // optionally send a response back to the renderer process
  event.reply('fromMain', 'Data received and processed in main process');
});

ipcMain.on('survey', (event, args) => {
  console.log('survey responses received: ', args);
  // do something with the survey responses

  // optionally send a response back to the renderer process
  event.reply('fromMain', 'Data received and processed in main process');
});

function startBaselineScript(subjectId, device) {

  // note - likely need to update script path for dev vs build differences. trying to do this below

  let scriptPath;

  if (isDevelopment) {
    // during development, use the relative path to the scripts folder
    scriptPath = path.join(__dirname, '..', 'public', 'scripts');
  } else {
    // in production, use the path from resources
    scriptPath = path.join(process.resourcesPath, 'scripts');
  }

  const filename = (device === 'old' ? 'old_' : '') + 'run_baseline.bat';
  const fullPath = path.join(scriptPath, filename);
  console.log(fullPath);

  exec(`start cmd.exe /K ${fullPath} ${subjectId}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error starting baseline script: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error in baseline script: ${stderr}`);
      return;
    }
    console.log(`Baseline script output: ${stdout}`);
  });
}

