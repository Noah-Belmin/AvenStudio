/**
 * Electron Main Process
 * Starts Python backend and creates application window
 */

const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let pythonProcess = null;
let mainWindow = null;

/**
 * Start Python FastAPI backend
 */
function startPythonBackend() {
  console.log('🐍 Starting Python backend...');

  const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
  const backendPath = path.join(__dirname, '../backend/main.py');

  pythonProcess = spawn(pythonPath, [backendPath], {
    cwd: path.join(__dirname, '../backend')
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python] ${data.toString().trim()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    const message = data.toString().trim();
    // Ignore uvicorn startup messages
    if (!message.includes('Started server process') &&
        !message.includes('Waiting for application startup') &&
        !message.includes('Application startup complete') &&
        !message.includes('Uvicorn running on')) {
      console.error(`[Python Error] ${message}`);
    } else {
      console.log(`[Python] ${message}`);
    }
  });

  pythonProcess.on('close', (code) => {
    console.log(`[Python] Process exited with code ${code}`);
  });

  // Give Python time to start (3 seconds)
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('✅ Python backend should be running on http://127.0.0.1:8000');
      resolve();
    }, 3000);
  });
}

/**
 * Create main application window
 */
function createWindow() {
  console.log('🪟 Creating application window...');

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    backgroundColor: '#F7F4F0', // --sand-light from design system
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    icon: path.join(__dirname, '../assets/icon.png'), // TODO: Add icon
    title: 'AvenStudio',
    show: false // Don't show until ready
  });

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    console.log('✅ Application window ready');
  });

  // Load app
  const isDev = process.env.NODE_ENV === 'development';

  if (isDev) {
    // Development: Load from Vite dev server
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
    console.log('📦 Loaded from Vite dev server (http://localhost:5173)');
  } else {
    // Production: Load built files
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
    console.log('📦 Loaded from built files');
  }

  // Handle window close
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * Initialize database (create if doesn't exist)
 */
function initializeDatabase() {
  const dbPath = path.join(__dirname, '../data/aven.db');
  const dataDir = path.dirname(dbPath);

  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
    console.log('📁 Created data directory');
  }

  if (!fs.existsSync(dbPath)) {
    console.log('💾 Database will be created on first run');
  } else {
    console.log('💾 Using existing database:', dbPath);
  }
}

/**
 * App lifecycle - ready
 */
app.whenReady().then(async () => {
  console.log('🚀 AvenStudio Starting...');
  console.log('📍 App Path:', app.getAppPath());
  console.log('📍 User Data:', app.getPath('userData'));

  // Initialize database
  initializeDatabase();

  // Start Python backend
  await startPythonBackend();

  // Create window
  createWindow();

  console.log('✅ AvenStudio Ready!');
});

/**
 * App lifecycle - activate (macOS)
 */
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

/**
 * App lifecycle - all windows closed
 */
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

/**
 * App lifecycle - quit
 */
app.on('quit', () => {
  console.log('👋 Shutting down...');

  // Kill Python process
  if (pythonProcess) {
    console.log('🛑 Stopping Python backend...');
    pythonProcess.kill();
    pythonProcess = null;
  }

  console.log('✅ Goodbye!');
});

/**
 * Handle uncaught exceptions
 */
process.on('uncaughtException', (error) => {
  console.error('💥 Uncaught Exception:', error);
});
