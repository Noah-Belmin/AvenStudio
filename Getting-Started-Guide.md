# AvenStudio - Getting Started Guide
## From Design Brief to Working App

This guide walks you through setting up your development environment and building the first working version of AvenStudio.

---

## Prerequisites

Before you start coding, you need:

### 1. Install Node.js
**Why:** Electron runs on Node.js

**How:**
- Visit: https://nodejs.org/
- Download: LTS version (Long Term Support)
- Install: Follow installer instructions
- Verify: Open terminal, type `node --version`

### 2. Install Python
**Why:** Your backend logic runs in Python

**How:**
- Visit: https://www.python.org/downloads/
- Download: Python 3.11 or newer
- Install: Check "Add Python to PATH" during installation
- Verify: Open terminal, type `python --version`

### 3. Install Git
**Why:** Version control for your code

**How:**
- Visit: https://git-scm.com/downloads
- Install: Default settings are fine
- Verify: Open terminal, type `git --version`

### 4. Install a Code Editor
**Recommended:** VS Code (free, excellent Python support)

**How:**
- Visit: https://code.visualstudio.com/
- Download and install
- Install extensions: Python, Pylance, SQLite Viewer

---

## Project Setup (Step by Step)

### Step 1: Create Project Folder

```bash
# Create main project folder
mkdir aven-studio
cd aven-studio

# Create subfolders
mkdir electron
mkdir ui
mkdir backend
mkdir data
```

**What you just created:**
```
aven-studio/
├── electron/    # Electron app shell
├── ui/          # HTML/CSS/JS interface
├── backend/     # Python FastAPI code
└── data/        # SQLite database will live here
```

---

### Step 2: Initialize Electron

```bash
# Initialize npm project
npm init -y

# Install Electron
npm install electron --save-dev

# Install Electron Forge (makes development easier)
npm install @electron-forge/cli --save-dev
```

**Create `electron/main.js`:**

```javascript
// This is the main entry point for your Electron app
const { app, BrowserWindow } = require('electron');
const path = require('path');

// Create the main window
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    backgroundColor: '#F7F4F0' // Sand-light from design system
  });

  // Load your UI
  mainWindow.loadFile('ui/index.html');

  // Open DevTools in development
  if (!app.isPackaged) {
    mainWindow.webContents.openDevTools();
  }
}

// App lifecycle
app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
```

**Create `electron/preload.js`:**

```javascript
// This file runs before the renderer and sets up safe communication
const { contextBridge } = require('electron');

// Expose safe methods to the UI
contextBridge.exposeInMainWorld('api', {
  // We'll add API methods here later
});
```

**Update `package.json`:**

```json
{
  "name": "aven-studio",
  "version": "0.1.0",
  "main": "electron/main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^27.0.0"
  }
}
```

---

### Step 3: Create Basic UI

**Create `ui/index.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AvenStudio</title>
  <link rel="stylesheet" href="styles/tokens.css">
  <link rel="stylesheet" href="styles/main.css">
</head>
<body>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">AvenStudio</div>
        <div class="logo-subtitle">Self-Build Navigator</div>
      </div>
      <nav class="sidebar-nav">
        <a href="#" class="nav-item active">Dashboard</a>
        <a href="#" class="nav-item">Tasks</a>
        <a href="#" class="nav-item">Budget</a>
        <a href="#" class="nav-item">Timeline</a>
      </nav>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <h1 class="page-title">Dashboard</h1>
      </header>

      <div class="dashboard">
        <h2>Welcome to AvenStudio</h2>
        <p>Your self-build project management platform</p>
      </div>
    </main>
  </div>

  <script src="scripts/app.js"></script>
</body>
</html>
```

**Create `ui/styles/tokens.css`:**

```css
/* Design System Tokens */
:root {
  /* Colors */
  --navy: #304F5D;
  --navy-dark: #243a45;
  --navy-light: #3d6275;
  --bronze: #A57F62;
  --bronze-light: #c9a485;
  --mint: #98D0D3;
  --mint-light: #c5e5e7;
  --sand: #EEE5DC;
  --sand-light: #F7F4F0;
  --sand-dark: #e0d4c8;
  --plum: #823755;
  --tangerine: #F37045;
  --white: #FFFFFF;
  
  /* Semantic */
  --success: #4a7c59;
  --success-light: #e8f0ea;
  --warning: #c17f24;
  --warning-light: #fef3e2;
  --danger: #9e3b3b;
  --danger-light: #fae8e8;
  
  /* Typography */
  --font-body: 'DM Sans', -apple-system, sans-serif;
  
  /* Layout */
  --sidebar-width: 260px;
}
```

**Create `ui/styles/main.css`:**

```css
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap');

/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  background-color: var(--sand-light);
  color: var(--navy);
  line-height: 1.6;
}

/* Layout */
.app-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background: var(--white);
  border-right: 1px solid var(--sand-dark);
  padding: 1.5rem;
}

.logo {
  font-size: 1.375rem;
  font-weight: 500;
  color: var(--navy);
  margin-bottom: 0.25rem;
}

.logo-subtitle {
  font-size: 0.75rem;
  color: var(--navy);
  opacity: 0.5;
}

.sidebar-nav {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  padding: 0.75rem 1rem;
  color: var(--navy);
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.15s ease;
}

.nav-item:hover {
  background: var(--sand-light);
}

.nav-item.active {
  background: var(--sand);
  border-left: 3px solid var(--bronze);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  background: var(--white);
  border-bottom: 1px solid var(--sand-dark);
  padding: 1rem 2rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--navy);
}

.dashboard {
  padding: 2rem;
}
```

**Create `ui/scripts/app.js`:**

```javascript
// Main application JavaScript
console.log('AvenStudio is running!');

// We'll add functionality here as we build features
```

---

### Step 4: Set Up Python Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install FastAPI and dependencies
pip install fastapi uvicorn sqlalchemy sqlite
```

**Create `backend/main.py`:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AvenStudio API")

# Allow Electron to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AvenStudio API is running"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# We'll add more endpoints here as we build features
```

**Create `backend/database.py`:**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'aven.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Create `backend/models.py`:**

```python
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    start_date = Column(DateTime)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")  # todo, in_progress, review, blocked, done
    priority = Column(String, default="medium")  # urgent, high, medium, low
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
```

**Create `backend/run.py`:**

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

---

### Step 5: Test Everything Works

**Terminal 1 - Start Backend:**
```bash
cd backend
python run.py
```

You should see: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Start Electron:**
```bash
# From project root
npm start
```

You should see: AvenStudio window opens with your UI!

**Test the connection:**
- Open browser to `http://127.0.0.1:8000/docs`
- You should see FastAPI's automatic documentation

---

## What You've Built

✅ Electron desktop app shell  
✅ Basic UI with design system colors  
✅ Python FastAPI backend  
✅ SQLite database setup  
✅ Communication between layers  

**This is your foundation.** Everything else builds on this.

---

## Next Steps

### 1. Build Your First Feature: Create Task

**Backend (backend/main.py):**

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Task
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    project_id: int = 1  # Default project for now

@app.post("/api/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
```

**Frontend (ui/scripts/app.js):**

```javascript
async function createTask(title, description) {
  const response = await fetch('http://127.0.0.1:8000/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, description, project_id: 1 })
  });
  
  const task = await response.json();
  console.log('Task created:', task);
  return task;
}
```

---

## Troubleshooting

### Python backend won't start
- Check Python is installed: `python --version`
- Check virtual environment is activated
- Check all dependencies installed: `pip list`

### Electron won't start
- Check Node.js is installed: `node --version`
- Check Electron is installed: `npm list electron`
- Check main.js path in package.json

### Can't connect to backend from frontend
- Check backend is running (Terminal 1)
- Check URL is correct (http://127.0.0.1:8000)
- Check CORS middleware is enabled
- Check browser console for errors

---

## Resources

**When you get stuck:**
- Electron docs: https://www.electronjs.org/docs/latest
- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy docs: https://docs.sqlalchemy.org/

**Community help:**
- Stack Overflow (tag: electron, fastapi, python)
- FastAPI Discord: https://discord.gg/VQjSZaeJmf
- Electron Discord: https://discord.gg/electron

---

**You now have everything you need to start building AvenStudio. Take it one feature at a time, test frequently, and you'll have a working app before you know it!**
