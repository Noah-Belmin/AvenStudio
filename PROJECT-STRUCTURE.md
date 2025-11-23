# AvenStudio Project Structure
## Electron + Python + Your HTML Mockups

This structure integrates your existing HTML mockups with the Electron + Python architecture.

---

## File Organization

```
AvenStudio/
├── electron/
│   ├── main.js              # Electron main process (starts Python, creates window)
│   └── preload.js           # Bridge between UI and Python (IPC)
│
├── ui/                      # Your HTML mockups go here
│   ├── index.html           # Landing/router page
│   ├── dashboard.html       # Your dashboard mockup (adapted)
│   ├── timeline.html        # Your timeline mockup (adapted)
│   ├── styles/
│   │   ├── tokens.css       # Design system variables (extracted from mockups)
│   │   └── components.css   # Shared component styles
│   └── scripts/
│       ├── api.js           # API client (talks to Python backend)
│       ├── dashboard.js     # Dashboard-specific logic
│       └── timeline.js      # Timeline-specific logic
│
├── backend/
│   ├── main.py              # FastAPI server entry point
│   ├── orchestrator.py      # Core orchestrator
│   ├── data/
│   │   ├── access_layer.py  # Data access abstraction
│   │   └── sqlite_layer.py  # SQLite implementation
│   └── modules/
│       ├── tasks/
│       │   ├── handlers.py
│       │   ├── schemas.py
│       │   └── migrations/
│       │       └── sqlite/
│       │           └── 001_initial.sql
│       ├── budget/
│       └── timeline/
│
├── data/
│   └── aven.db              # SQLite database (created on first run)
│
├── package.json             # Electron + Node dependencies
├── requirements.txt         # Python dependencies
└── config.yaml              # App configuration
```

---

## How It Works

### 1. **Electron Starts Everything**

`electron/main.js` is the entry point:

```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pythonProcess = null;
let mainWindow = null;

// Start Python backend
function startPythonBackend() {
    console.log('Starting Python backend...');

    pythonProcess = spawn('python', [
        path.join(__dirname, '../backend/main.py')
    ]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    // Give Python time to start (2 seconds)
    return new Promise(resolve => setTimeout(resolve, 2000));
}

// Create Electron window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        backgroundColor: '#F7F4F0',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    // Load your UI
    mainWindow.loadFile('ui/index.html');

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
}

// App lifecycle
app.whenReady().then(async () => {
    // Start Python backend first
    await startPythonBackend();

    // Then create window
    createWindow();
});

// Cleanup on quit
app.on('quit', () => {
    if (pythonProcess) {
        pythonProcess.kill();
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
```

---

### 2. **Preload Script (The Bridge)**

`electron/preload.js` exposes safe API methods to your UI:

```javascript
const { contextBridge } = require('electron');

// Expose API to UI (accessible via window.api)
contextBridge.exposeInMainWorld('api', {
    // Tasks API
    tasks: {
        list: (filters) => fetch('http://127.0.0.1:8000/api/tasks', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        }).then(r => r.json()),

        create: (data) => fetch('http://127.0.0.1:8000/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json()),

        update: (id, data) => fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json()),

        delete: (id) => fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
            method: 'DELETE'
        }).then(r => r.json())
    },

    // Stats API
    stats: {
        get: () => fetch('http://127.0.0.1:8000/api/stats')
            .then(r => r.json())
    },

    // Budget API
    budget: {
        list: () => fetch('http://127.0.0.1:8000/api/budget')
            .then(r => r.json()),

        create: (data) => fetch('http://127.0.0.1:8000/api/budget', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(r => r.json())
    },

    // Timeline API
    timeline: {
        get: (projectId) => fetch(`http://127.0.0.1:8000/api/timeline/${projectId}`)
            .then(r => r.json())
    }
});
```

---

### 3. **Python Backend**

`backend/main.py` runs as FastAPI server:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from orchestrator import Orchestrator
from data.sqlite_layer import SQLiteDataLayer

app = FastAPI(title="AvenStudio API")

# Allow Electron UI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
config = {
    'db_type': 'sqlite',
    'db_path': 'data/aven.db'
}
orchestrator = Orchestrator(config)

# Health check
@app.get("/")
def root():
    return {"status": "AvenStudio API running", "version": "0.1.0"}

# Stats endpoint (for dashboard)
@app.get("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    return orchestrator.handle_request({
        'module': 'stats',
        'action': 'get_dashboard_stats'
    })

# Tasks endpoints
@app.get("/api/tasks")
def list_tasks(status: str = None, priority: str = None):
    """List all tasks with optional filters"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'list',
        'filters': {'status': status, 'priority': priority}
    })

@app.post("/api/tasks")
def create_task(task_data: dict):
    """Create new task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'create',
        'data': task_data
    })

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task_data: dict):
    """Update existing task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'update',
        'id': task_id,
        'data': task_data
    })

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'delete',
        'id': task_id
    })

# Start server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
```

---

### 4. **Adapting Your HTML Mockups**

Your mockups stay **95% the same**. Only JavaScript changes.

#### Before (Static Mockup):
```html
<!-- selfbuild-dashboard.html -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-card-value">24</div>
        <div class="stat-card-label">Total Tasks</div>
    </div>
</div>
```

#### After (Dynamic with Python Backend):
```html
<!-- ui/dashboard.html -->
<div class="stats-grid" id="statsGrid">
    <!-- Will be populated by JavaScript -->
</div>

<script src="scripts/dashboard.js"></script>
```

**ui/scripts/dashboard.js:**
```javascript
// Load dashboard stats on page load
async function loadDashboardStats() {
    try {
        // Call Python backend via API
        const stats = await window.api.stats.get();

        // Update UI with real data
        document.getElementById('statsGrid').innerHTML = `
            <div class="stat-card">
                <div class="stat-card-header">
                    <span class="stat-card-title">Total Tasks</span>
                    <div class="stat-card-icon navy">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                        </svg>
                    </div>
                </div>
                <div class="stat-card-value">${stats.total_tasks}</div>
                <div class="stat-card-label">Across all phases</div>
            </div>

            <div class="stat-card">
                <div class="stat-card-header">
                    <span class="stat-card-title">In Progress</span>
                    <div class="stat-card-icon mint">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                    </div>
                </div>
                <div class="stat-card-value">${stats.in_progress}</div>
                <div class="stat-card-label">Currently active</div>
            </div>

            <div class="stat-card">
                <div class="stat-card-header">
                    <span class="stat-card-title">Completed</span>
                    <div class="stat-card-icon success">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                            <path d="M22 4L12 14.01l-3-3"/>
                        </svg>
                    </div>
                </div>
                <div class="stat-card-value">${stats.completed}</div>
                <div class="stat-card-label">${stats.completion_rate}% completion rate</div>
            </div>

            <div class="stat-card">
                <div class="stat-card-header">
                    <span class="stat-card-title">Blocked</span>
                    <div class="stat-card-icon danger">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 8v4M12 16h.01"/>
                        </svg>
                    </div>
                </div>
                <div class="stat-card-value">${stats.blocked}</div>
                <div class="stat-card-label">Needs attention</div>
            </div>
        `;
    } catch (error) {
        console.error('Failed to load stats:', error);
        // Show error state to user
    }
}

// Load tasks list
async function loadTasks() {
    try {
        const tasks = await window.api.tasks.list({ priority: 'high' });

        const taskList = document.getElementById('highPriorityTasks');
        taskList.innerHTML = tasks.map(task => `
            <div class="task-item" onclick="openTask('${task.id}')">
                <div class="task-item-content">
                    <div class="task-item-title">${task.title}</div>
                    <div class="task-tags">
                        <span class="tag tag-${task.priority}">${task.priority}</span>
                        <span class="tag tag-${task.status}">${task.status}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

// Create new task
async function createTask() {
    const title = document.getElementById('taskTitle').value;
    const priority = document.getElementById('taskPriority').value;

    try {
        await window.api.tasks.create({
            title: title,
            priority: priority,
            status: 'todo'
        });

        // Reload task list
        await loadTasks();

        // Close modal
        closeModal();
    } catch (error) {
        console.error('Failed to create task:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardStats();
    loadTasks();
});
```

---

### 5. **CSS Extraction**

Extract your mockup styles into reusable files:

**ui/styles/tokens.css** (from your mockups):
```css
:root {
    /* Colors */
    --navy: #304F5D;
    --navy-dark: #243a45;
    --bronze: #A57F62;
    --bronze-light: #c9a485;
    --mint: #98D0D3;
    --sand: #EEE5DC;
    --sand-light: #F7F4F0;
    --white: #FFFFFF;

    /* Semantic */
    --success: #4a7c59;
    --warning: #c17f24;
    --danger: #9e3b3b;

    /* Typography */
    --font-display: 'DM Sans', -apple-system, sans-serif;
    --font-body: 'DM Sans', -apple-system, sans-serif;

    /* Layout */
    --sidebar-width: 260px;
}
```

**ui/styles/components.css** (extracted from mockups):
```css
/* Stats Cards */
.stats-grid { /* ... */ }
.stat-card { /* ... */ }

/* Task Cards */
.task-item { /* ... */ }
.task-tags { /* ... */ }

/* Tags */
.tag { /* ... */ }
.tag-urgent { /* ... */ }
.tag-high { /* ... */ }

/* Timeline */
.gantt-bar { /* ... */ }
```

Then each page imports them:
```html
<link rel="stylesheet" href="styles/tokens.css">
<link rel="stylesheet" href="styles/components.css">
<link rel="stylesheet" href="styles/dashboard.css">
```

---

## Step-by-Step: Converting Your Mockups

### Phase 1: Setup (Week 1)

1. **Initialize Electron project**
   ```bash
   npm init
   npm install electron electron-builder --save-dev
   ```

2. **Create basic structure**
   ```bash
   mkdir -p electron ui/scripts ui/styles backend/modules
   ```

3. **Copy mockups to ui/**
   ```bash
   cp selfbuild-dashboard.html ui/dashboard.html
   cp selfbuild-timeline.html ui/timeline.html
   ```

4. **Extract CSS to shared files**
   - Create `ui/styles/tokens.css` with design system
   - Create `ui/styles/components.css` with reusable components

5. **Create Electron main and preload**
   - `electron/main.js` (starts Python, creates window)
   - `electron/preload.js` (API bridge)

6. **Test Electron loads mockups**
   ```bash
   npm start  # Should show your mockups in Electron window
   ```

---

### Phase 2: Python Backend (Week 1-2)

1. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install fastapi uvicorn
   ```

2. **Create basic FastAPI server**
   - `backend/main.py` with health check endpoint

3. **Test Python starts from Electron**
   - Should see "Python backend started" in console

4. **Create first endpoint** (`/api/stats`)
   - Return hardcoded stats for now

5. **Test UI can call Python**
   - `window.api.stats.get()` should return data

---

### Phase 3: Connect Dashboard (Week 2-3)

1. **Create `ui/scripts/dashboard.js`**
   - `loadDashboardStats()` function
   - `loadTasks()` function

2. **Replace static HTML with dynamic**
   - Stats cards populated from API
   - Task lists populated from API

3. **Implement orchestrator**
   - `backend/orchestrator.py`
   - Route requests to modules

4. **Create tasks module**
   - `backend/modules/tasks/handlers.py`
   - SQLite schema
   - CRUD operations

5. **Test end-to-end**
   - Create task in UI → saves to SQLite → shows in list

---

### Phase 4: Timeline & Other Views (Week 3-4)

1. **Adapt timeline mockup**
   - `ui/scripts/timeline.js`
   - Load tasks from API
   - Render Gantt bars dynamically

2. **Add budget module**
   - Backend endpoints
   - UI integration

3. **Navigation between views**
   - Router logic in `ui/index.html`
   - Load views dynamically

---

## Key Differences from TypeScript Approach

| Your TypeScript Attempt | Electron + Python Approach |
|---|---|
| Framework-heavy (React/Vue?) | Pure HTML/CSS (your mockups!) |
| Complex build process | Simple: HTML loads directly |
| All logic in JS/TS | Business logic in Python (cleaner) |
| May need bundling | No bundling needed |
| TypeScript compilation | Optional (can use vanilla JS) |

**Your mockups are already perfect for Electron.** You just:
1. Keep the HTML/CSS as-is
2. Add JavaScript to call Python API
3. Python handles all business logic
4. SQLite stores data

---

## What You Can Reuse from Mockups

✅ **100% of HTML structure** (keep layouts exactly)
✅ **100% of CSS styling** (all your design work)
✅ **SVG icons** (all navigation, stat icons)
✅ **Color system** (Navy, Bronze, Mint, Sand)
✅ **Typography** (DM Sans everywhere)
✅ **Component patterns** (cards, tags, buttons)

❌ **Static data** (replace with API calls)
❌ **Hardcoded values** (fetch from Python)

---

## Example: Complete Flow

**User clicks "New Task" button:**

1. **UI** (dashboard.html):
   ```javascript
   async function createTask() {
       const data = {
           title: document.getElementById('taskTitle').value,
           priority: document.getElementById('taskPriority').value
       };

       await window.api.tasks.create(data);
       await loadTasks();  // Refresh list
   }
   ```

2. **Preload** (electron/preload.js):
   ```javascript
   tasks: {
       create: (data) => fetch('http://127.0.0.1:8000/api/tasks', {
           method: 'POST',
           body: JSON.stringify(data)
       })
   }
   ```

3. **Python** (backend/main.py):
   ```python
   @app.post("/api/tasks")
   def create_task(task_data: dict):
       return orchestrator.handle_request({
           'module': 'tasks',
           'action': 'create',
           'data': task_data
       })
   ```

4. **Orchestrator**:
   ```python
   def handle_request(self, request):
       module = self.modules['tasks']
       return module.handle(request, self.data_layer)
   ```

5. **Tasks Module**:
   ```python
   def handle(self, request, data_layer):
       if request['action'] == 'create':
           task_id = data_layer.insert('tasks', request['data'])
           return {'success': True, 'id': task_id}
   ```

6. **SQLite**: Task saved to database

7. **Response** flows back up to UI, list refreshes

---

## Why This Is Better Than TypeScript SPA

1. **Simpler**: No build process, no bundling
2. **Faster**: HTML loads instantly
3. **Cleaner**: Business logic in Python (not JS)
4. **Offline**: Everything local, no server needed
5. **Maintainable**: Clear separation (UI ↔ Python)
6. **Your mockups work**: 95% already done

---

## Next Step: Quick Prototype

Want me to create:
- [ ] Complete Electron setup (main.js + preload.js)?
- [ ] Adapted dashboard.html with API integration?
- [ ] Basic Python backend with first endpoints?
- [ ] Example module (tasks) with SQLite?

**I can give you a working prototype that shows your dashboard mockup connected to real Python + SQLite backend in about 30 minutes of coding.**

Your TypeScript approach would have required rebuilding everything. With Electron, your mockups **ARE** the app - they just need connection to the Python brain.
