# Adapting Your React TypeScript App to Electron + Python
## Migration Strategy for src/ → AvenStudio Desktop

**What you have:** React + TypeScript SPA with localStorage
**What we're building:** Same UI + functionality, but with Electron + Python + SQLite backend

---

## Your Current Architecture

```
React App (src/)
├── Components (Dashboard, Kanban, Timeline, etc.)
├── State Management (useState, useEffect)
├── Data Storage (localStorage)
└── TypeScript Types (Task, Epic, Sprint, etc.)
```

**Features you've implemented:**
- ✅ Dashboard with stats
- ✅ Multiple views (List, Kanban, Calendar, Timeline)
- ✅ Rich task model (subtasks, comments, attachments, costs)
- ✅ Automation rules
- ✅ Category management
- ✅ Global search
- ✅ Theme switching
- ✅ Settings panel
- ✅ CSV import/export

---

## Target Architecture

```
Electron Shell
    ↓
React App (UI - 95% unchanged)
    ↓ API calls
Preload Bridge (IPC)
    ↓
Python FastAPI (Orchestrator + Modules)
    ↓
SQLite Database
```

---

## Migration Strategy

### Phase 1: Minimal Changes (Keep React, Add Backend)

**Keep:**
- ✅ All React components (Dashboard, Kanban, Timeline, etc.)
- ✅ All TypeScript types
- ✅ All UI logic and interactions
- ✅ Theme system
- ✅ Component structure

**Change:**
- ❌ Remove localStorage persistence
- ✅ Add API client layer
- ✅ Replace useState with API calls
- ✅ Add Electron wrapper

---

## Step-by-Step Adaptation

### 1. Create API Client Layer

**New file:** `src/services/api.ts`

```typescript
// src/services/api.ts

/**
 * API Client for communicating with Python backend
 * Replaces localStorage with real backend calls
 */

import type { Task, NewTaskFormData, AutomationRule } from '../types'

// Define API interface (matches window.api from preload)
interface ElectronAPI {
  tasks: {
    list: (filters?: any) => Promise<Task[]>
    get: (id: string) => Promise<Task>
    create: (data: NewTaskFormData) => Promise<Task>
    update: (id: string, data: Partial<Task>) => Promise<Task>
    delete: (id: string) => Promise<void>
  }
  stats: {
    get: () => Promise<{
      total_tasks: number
      in_progress: number
      completed: number
      blocked: number
      completion_rate: number
    }>
  }
  categories: {
    list: () => Promise<string[]>
    create: (name: string) => Promise<string>
    delete: (name: string) => Promise<void>
  }
  automation: {
    list: () => Promise<AutomationRule[]>
    create: (rule: AutomationRule) => Promise<AutomationRule>
    update: (id: string, rule: Partial<AutomationRule>) => Promise<AutomationRule>
    delete: (id: string) => Promise<void>
    execute: (taskId: string, trigger: string) => Promise<void>
  }
}

// Access Electron API (injected by preload script)
declare global {
  interface Window {
    api: ElectronAPI
  }
}

// Export API client
export const api = window.api

// Helper: Check if running in Electron
export const isElectron = () => {
  return typeof window.api !== 'undefined'
}

// Fallback for development (when not in Electron)
// Uses localStorage as before
export const devAPI = {
  tasks: {
    list: async () => {
      const saved = localStorage.getItem('tasks')
      return saved ? JSON.parse(saved) : []
    },
    create: async (data: NewTaskFormData) => {
      const tasks = await devAPI.tasks.list()
      const newTask: Task = {
        id: crypto.randomUUID(),
        ...data,
        status: 'todo',
        tags: data.tags || [],
        comments: [],
        attachments: [],
        checklist: [],
        subtasks: [],
        customFields: {},
        createdAt: new Date(),
        updatedAt: new Date()
      }
      tasks.push(newTask)
      localStorage.setItem('tasks', JSON.stringify(tasks))
      return newTask
    },
    // ... other methods
  }
}

// Use Electron API if available, fallback to dev API
export default isElectron() ? api : devAPI
```

---

### 2. Update App.tsx to Use API

**Before (localStorage):**
```typescript
// App.tsx - OLD

const [tasks, setTasks] = useState<Task[]>([])

// Load from localStorage
useEffect(() => {
  const saved = loadFromLocalStorage()
  if (saved) {
    setTasks(saved.tasks)
  }
}, [])

// Save to localStorage
useEffect(() => {
  saveToLocalStorage({ tasks, categories })
}, [tasks, categories])

// Create task
const createTask = (formData: NewTaskFormData) => {
  const newTask: Task = {
    id: crypto.randomUUID(),
    ...formData,
    // ...
  }
  setTasks([...tasks, newTask])
}
```

**After (API calls):**
```typescript
// App.tsx - NEW

import api from './services/api'

const [tasks, setTasks] = useState<Task[]>([])
const [loading, setLoading] = useState(true)

// Load from API
useEffect(() => {
  loadTasks()
}, [])

const loadTasks = async () => {
  try {
    setLoading(true)
    const data = await api.tasks.list()
    setTasks(data)
  } catch (error) {
    console.error('Failed to load tasks:', error)
  } finally {
    setLoading(false)
  }
}

// Create task
const createTask = async (formData: NewTaskFormData) => {
  try {
    const newTask = await api.tasks.create(formData)
    setTasks([...tasks, newTask])
    return newTask
  } catch (error) {
    console.error('Failed to create task:', error)
    throw error
  }
}

// Update task
const updateTask = async (id: string, updates: Partial<Task>) => {
  try {
    const updated = await api.tasks.update(id, updates)
    setTasks(tasks.map(t => t.id === id ? updated : t))
  } catch (error) {
    console.error('Failed to update task:', error)
    throw error
  }
}

// Delete task
const deleteTask = async (id: string) => {
  try {
    await api.tasks.delete(id)
    setTasks(tasks.filter(t => t.id !== id))
  } catch (error) {
    console.error('Failed to delete task:', error)
    throw error
  }
}
```

---

### 3. Update Components to Use Async Operations

Your components mostly stay the same, just handle async:

**Example: DashboardView.tsx**

```typescript
// Before
const stats = {
  total: tasks.length,
  inProgress: tasks.filter(t => t.status === 'in-progress').length,
  // ...
}

// After (using API)
const [stats, setStats] = useState(null)

useEffect(() => {
  loadStats()
}, [tasks])

const loadStats = async () => {
  try {
    const data = await api.stats.get()
    setStats(data)
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}
```

---

### 4. Electron Setup

**File: `electron/main.js`**

```javascript
const { app, BrowserWindow } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let pythonProcess = null
let mainWindow = null

// Start Python backend
function startPythonBackend() {
  console.log('Starting Python backend...')

  pythonProcess = spawn('python', [
    path.join(__dirname, '../backend/main.py')
  ])

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`)
  })

  return new Promise(resolve => setTimeout(resolve, 2000))
}

// Create window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  // In development: load from Vite dev server
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    // In production: load built React app
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

app.whenReady().then(async () => {
  await startPythonBackend()
  createWindow()
})

app.on('quit', () => {
  if (pythonProcess) pythonProcess.kill()
})
```

**File: `electron/preload.js`**

```javascript
const { contextBridge } = require('electron')

// Expose API to React app
contextBridge.exposeInMainWorld('api', {
  tasks: {
    list: (filters) =>
      fetch('http://127.0.0.1:8000/api/tasks?' + new URLSearchParams(filters))
        .then(r => r.json()),

    get: (id) =>
      fetch(`http://127.0.0.1:8000/api/tasks/${id}`)
        .then(r => r.json()),

    create: (data) =>
      fetch('http://127.0.0.1:8000/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(r => r.json()),

    update: (id, data) =>
      fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(r => r.json()),

    delete: (id) =>
      fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
        method: 'DELETE'
      }).then(r => r.json())
  },

  stats: {
    get: () =>
      fetch('http://127.0.0.1:8000/api/stats')
        .then(r => r.json())
  },

  categories: {
    list: () =>
      fetch('http://127.0.0.1:8000/api/categories')
        .then(r => r.json()),

    create: (name) =>
      fetch('http://127.0.0.1:8000/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      }).then(r => r.json()),

    delete: (name) =>
      fetch(`http://127.0.0.1:8000/api/categories/${name}`, {
        method: 'DELETE'
      }).then(r => r.json())
  },

  automation: {
    list: () =>
      fetch('http://127.0.0.1:8000/api/automation/rules')
        .then(r => r.json()),

    create: (rule) =>
      fetch('http://127.0.0.1:8000/api/automation/rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rule)
      }).then(r => r.json()),

    execute: (taskId, trigger) =>
      fetch('http://127.0.0.1:8000/api/automation/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ taskId, trigger })
      }).then(r => r.json())
  }
})
```

---

### 5. Python Backend (Matches Your Types)

**File: `backend/main.py`**

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn

from orchestrator import Orchestrator

app = FastAPI(title="AvenStudio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = Orchestrator({
    'db_type': 'sqlite',
    'db_path': 'data/aven.db'
})

# Pydantic models (match your TypeScript types)
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    category: str
    tags: List[str] = []
    dueDate: Optional[datetime] = None
    startDate: Optional[datetime] = None
    assignedTo: Optional[str] = None
    estimatedHours: Optional[float] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    dueDate: Optional[datetime] = None
    completionPercentage: Optional[int] = None

# Endpoints
@app.get("/api/tasks")
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
):
    """List all tasks with optional filters"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'list',
        'filters': {
            'status': status,
            'priority': priority,
            'category': category
        }
    })

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """Get single task by ID"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'get',
        'id': task_id
    })

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    """Create new task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'create',
        'data': task.dict()
    })

@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    """Update existing task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'update',
        'id': task_id,
        'data': task.dict(exclude_unset=True)
    })

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete task"""
    return orchestrator.handle_request({
        'module': 'tasks',
        'action': 'delete',
        'id': task_id
    })

@app.get("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    return orchestrator.handle_request({
        'module': 'stats',
        'action': 'get_dashboard_stats'
    })

@app.get("/api/categories")
def list_categories():
    """List all categories"""
    return orchestrator.handle_request({
        'module': 'categories',
        'action': 'list'
    })

# Automation rules endpoints
@app.get("/api/automation/rules")
def list_automation_rules():
    """List all automation rules"""
    return orchestrator.handle_request({
        'module': 'automation',
        'action': 'list_rules'
    })

@app.post("/api/automation/rules")
def create_automation_rule(rule: Dict[str, Any]):
    """Create automation rule"""
    return orchestrator.handle_request({
        'module': 'automation',
        'action': 'create_rule',
        'data': rule
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

### 6. SQLite Schema (Based on Your Types)

**File: `backend/modules/tasks/migrations/sqlite/001_initial.sql`**

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,

    -- Basic info
    title TEXT NOT NULL,
    description TEXT,

    -- Status & Priority
    status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in-progress', 'review', 'blocked', 'done')),
    priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),

    -- Categorization
    category TEXT,
    tags TEXT,  -- JSON array

    -- Relationships
    epic_id TEXT,
    sprint_id TEXT,
    job_site_id TEXT,
    parent_task_id TEXT,
    related_task_ids TEXT,  -- JSON array

    -- Assignment
    assigned_to TEXT,
    created_by TEXT,
    reviewers TEXT,  -- JSON array

    -- Dates (ISO 8601 strings)
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    due_date TEXT,
    start_date TEXT,
    completed_at TEXT,

    -- Collaboration (stored as JSON)
    comments TEXT DEFAULT '[]',
    attachments TEXT DEFAULT '[]',
    checklist TEXT DEFAULT '[]',
    subtasks TEXT DEFAULT '[]',

    -- Custom fields
    custom_fields TEXT DEFAULT '{}',

    -- Metadata
    estimated_hours REAL,
    completion_percentage INTEGER DEFAULT 0 CHECK(completion_percentage BETWEEN 0 AND 100),
    blocked_by TEXT,  -- JSON array
    is_locked BOOLEAN DEFAULT 0,
    is_favorite BOOLEAN DEFAULT 0,

    -- Cost tracking
    estimated_cost REAL,
    actual_cost REAL,
    cost_breakdown TEXT DEFAULT '[]',  -- JSON array
    billable BOOLEAN DEFAULT 0
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_category ON tasks(category);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    name TEXT PRIMARY KEY,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Insert default categories
INSERT OR IGNORE INTO categories (name) VALUES
    ('work'),
    ('personal'),
    ('health'),
    ('learning'),
    ('construction'),
    ('other');

-- Automation rules table
CREATE TABLE IF NOT EXISTS automation_rules (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    enabled BOOLEAN DEFAULT 1,
    trigger TEXT NOT NULL,
    conditions TEXT NOT NULL,  -- JSON
    actions TEXT NOT NULL,  -- JSON
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    last_triggered TEXT,
    trigger_count INTEGER DEFAULT 0
);
```

---

## File Structure After Migration

```
AvenStudio/
├── electron/
│   ├── main.js              # Starts Python, creates window
│   └── preload.js           # Bridges React → Python
│
├── src/                     # Your React app (mostly unchanged!)
│   ├── App.tsx              # Updated: API calls instead of localStorage
│   ├── components/          # No changes needed
│   │   ├── DashboardView.tsx
│   │   ├── KanbanView.tsx
│   │   ├── TimelineView.tsx
│   │   └── ...
│   ├── services/
│   │   └── api.ts           # NEW: API client layer
│   ├── types.ts             # No changes
│   ├── utils.ts             # Remove localStorage functions
│   └── ...
│
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── orchestrator.py      # Routes to modules
│   └── modules/
│       ├── tasks/
│       │   ├── handlers.py
│       │   └── migrations/sqlite/001_initial.sql
│       ├── automation/
│       └── stats/
│
├── data/
│   └── aven.db              # SQLite database
│
├── package.json             # Add Electron dependencies
├── vite.config.ts           # Configure for Electron
└── tsconfig.json            # No changes
```

---

## Development Workflow

### 1. Run React Dev Server (for UI development)
```bash
npm run dev  # Vite dev server on http://localhost:5173
```

### 2. Run Python Backend (separate terminal)
```bash
cd backend
python main.py  # API on http://127.0.0.1:8000
```

### 3. Run in Electron (for testing)
```bash
npm run electron:dev  # Starts both Vite + Python + Electron
```

### 4. Build for Production
```bash
npm run build  # Build React app
npm run electron:build  # Package Electron + Python into .exe/.app
```

---

## What Stays the Same

✅ **100% of your React components** (Dashboard, Kanban, Timeline, etc.)
✅ **100% of your TypeScript types**
✅ **100% of your UI logic**
✅ **Theme system**
✅ **Automation rules logic** (just stored in SQLite instead of localStorage)
✅ **All views and interactions**

---

## What Changes

❌ Remove `localStorage` calls
✅ Add `api` service layer
✅ Make component methods `async`
✅ Add loading states
✅ Add error handling

**Example change in a component:**

```typescript
// Before
const handleCreateTask = (formData) => {
  createTask(formData)
  setNewTaskModalOpen(false)
}

// After
const handleCreateTask = async (formData) => {
  try {
    await createTask(formData)
    setNewTaskModalOpen(false)
  } catch (error) {
    // Show error toast
    console.error('Failed to create task:', error)
  }
}
```

---

## Key Benefits

1. **Minimal code changes** - React app mostly stays the same
2. **Keep all your features** - automation, views, cost tracking, etc.
3. **Real database** - SQLite instead of localStorage
4. **Desktop app** - Packaged .exe/.app
5. **Python backend** - Clean business logic separation
6. **Scalable** - Can migrate to PostgreSQL later

---

## Next Steps

Want me to:
1. **Create the API service layer** (`src/services/api.ts`)?
2. **Update App.tsx** to use API calls?
3. **Generate SQLite schema** from your TypeScript types?
4. **Set up Electron configuration** (package.json, main.js, preload.js)?
5. **Create Python backend** with all your endpoints?

Your React app is **excellent** - we're just swapping localStorage for a real backend. The UI and logic you built stays intact!
