# AvenStudio Mockup - Working Prototype

**A fully functional desktop prototype demonstrating Electron + React + Python + SQLite architecture**

This is a working implementation showing how your React TypeScript app integrates with a Python backend and SQLite database, packaged as a desktop application with Electron.

---

## What This Is

This prototype demonstrates:
- ✅ **React TypeScript UI** - Your existing components working with real data
- ✅ **Electron Desktop App** - Packaged as native .exe/.app
- ✅ **Python FastAPI Backend** - Business logic and database operations
- ✅ **SQLite Database** - Offline-first data persistence
- ✅ **Modular Architecture** - Orchestrator + pluggable modules
- ✅ **API Service Layer** - Clean separation between UI and backend

---

## Architecture

```
┌─────────────────────────────────────┐
│    Electron Window (Chromium)       │
│    React UI (Your Components)       │
└─────────────┬───────────────────────┘
              │
              │ window.api (IPC Bridge)
              │
┌─────────────▼───────────────────────┐
│        Electron Preload.js          │
│   (Bridges UI ↔ Python via fetch)   │
└─────────────┬───────────────────────┘
              │
              │ HTTP (localhost:8000)
              │
┌─────────────▼───────────────────────┐
│      Python FastAPI Backend         │
│                                     │
│  ┌─────────────────────────────┐   │
│  │    Core Orchestrator        │   │
│  └────┬──────────┬─────────────┘   │
│       │          │                  │
│  ┌────▼────┐ ┌───▼────┐            │
│  │ Tasks   │ │ Stats  │            │
│  │ Module  │ │ Module │            │
│  └────┬────┘ └───┬────┘            │
│       │          │                  │
│  ┌────▼──────────▼────┐            │
│  │  SQLite Data Layer  │            │
│  └─────────────────────┘            │
└─────────────┬───────────────────────┘
              │
              │
    ┌─────────▼──────────┐
    │  SQLite Database    │
    │  (data/aven.db)     │
    └────────────────────┘
```

---

## Project Structure

```
MockUp/
├── electron/
│   ├── main.js              # Electron main process (starts Python, creates window)
│   └── preload.js           # IPC bridge (exposes window.api to React)
│
├── src/                     # React TypeScript App
│   ├── App.tsx              # Main app (adapted for API)
│   ├── components/          # All your React components
│   ├── services/
│   │   └── api.ts           # API client layer (replaces localStorage)
│   ├── types.ts             # TypeScript types
│   └── ...
│
├── backend/
│   ├── main.py              # FastAPI application
│   ├── orchestrator.py      # Core orchestrator (routes requests)
│   ├── data/
│   │   └── sqlite_layer.py  # SQLite data access layer
│   └── modules/
│       ├── tasks/
│       │   └── handlers.py  # Task CRUD operations
│       ├── stats/
│       │   └── handlers.py  # Dashboard statistics
│       ├── categories/
│       │   └── handlers.py  # Category management
│       └── automation/
│           └── handlers.py  # Automation rules
│
├── data/
│   └── aven.db              # SQLite database (created on first run)
│
├── package.json             # Node dependencies + Electron config
├── vite.config.ts           # Vite build configuration
├── tsconfig.json            # TypeScript configuration
└── README.md                # This file
```

---

## Quick Start

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/downloads/))
- **npm** or **yarn**

### 1. Install Dependencies

```bash
# Navigate to MockUp directory
cd MockUp

# Install Node dependencies
npm install

# Install Python dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Run in Development Mode

**Option A: Run everything automatically**
```bash
npm run electron:dev
```

This will:
1. Start Vite dev server (React UI on http://localhost:5173)
2. Wait for Vite to be ready
3. Start Python backend automatically
4. Open Electron window

**Option B: Run components separately** (for debugging)

Terminal 1 - React UI:
```bash
npm run dev
```

Terminal 2 - Python Backend:
```bash
cd backend
python main.py
```

Terminal 3 - Electron:
```bash
electron .
```

### 3. Build for Production

```bash
# Build React app + Package Electron
npm run electron:build
```

This creates a distributable app in `dist-electron/`:
- **Windows**: `AvenStudio Setup.exe`
- **macOS**: `AvenStudio.dmg`
- **Linux**: `AvenStudio.AppImage`

---

## How It Works

### Data Flow Example: Creating a Task

1. **User clicks "New Task" button** in React UI
2. **React calls:** `await api.tasks.create(taskData)`
3. **API service** (`src/services/api.ts`) calls: `window.api.tasks.create()`
4. **Preload bridge** (`electron/preload.js`) makes HTTP request to Python
5. **Python receives** POST request at `/api/tasks`
6. **FastAPI routes** to orchestrator
7. **Orchestrator** forwards to Tasks module
8. **Tasks module** validates data and calls data layer
9. **Data layer** inserts into SQLite database
10. **Response flows back** through all layers
11. **React updates** UI with new task

**All of this happens in milliseconds, completely offline!**

---

## API Endpoints

The Python backend exposes these endpoints:

### Tasks
- `GET /api/tasks` - List tasks (with filters)
- `GET /api/tasks/{id}` - Get single task
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Stats
- `GET /api/stats` - Dashboard statistics

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category
- `PUT /api/categories/{name}` - Update category
- `DELETE /api/categories/{name}` - Delete category

### Automation
- `GET /api/automation/rules` - List automation rules
- `POST /api/automation/rules` - Create rule
- `POST /api/automation/execute` - Execute automation

### System
- `GET /` - Health check

**API Documentation:** http://127.0.0.1:8000/docs (when backend is running)

---

## Database Schema

### tasks
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('todo', 'in-progress', 'review', 'blocked', 'done')),
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
    category TEXT,
    tags TEXT (JSON array),
    due_date TEXT (ISO 8601),
    start_date TEXT,
    assigned_to TEXT,
    estimated_hours REAL,
    completion_percentage INTEGER (0-100),
    blocked_by TEXT (JSON array),
    comments TEXT (JSON array),
    attachments TEXT (JSON array),
    checklist TEXT (JSON array),
    subtasks TEXT (JSON array),
    custom_fields TEXT (JSON object),
    created_at TEXT,
    updated_at TEXT
)
```

### categories
```sql
CREATE TABLE categories (
    name TEXT PRIMARY KEY,
    created_at TEXT
)
```

### automation_rules
```sql
CREATE TABLE automation_rules (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    enabled INTEGER (0 or 1),
    trigger TEXT,
    conditions TEXT (JSON array),
    actions TEXT (JSON array),
    created_at TEXT,
    updated_at TEXT,
    last_triggered TEXT,
    trigger_count INTEGER
)
```

**Database Location:** `MockUp/data/aven.db`

---

## Making Changes

### Adding a New Feature to UI

1. Edit React components in `src/components/`
2. Hot reload updates automatically (Vite)
3. Call backend via `api` service if needed

### Adding a New Endpoint

1. Add route in `backend/main.py`
2. Add handler in appropriate module
3. Add method to `electron/preload.js`
4. Add to `src/services/api.ts`

### Adding a New Module

1. Create `backend/modules/yourmodule/handlers.py`
2. Register in `backend/orchestrator.py`
3. Add endpoints in `backend/main.py`

---

## Adapting App.tsx

The original `App.tsx` uses `localStorage`. To use the API:

### Key Changes Needed

1. **Import API instead of utils:**
   ```typescript
   // Remove
   import { saveToLocalStorage, loadFromLocalStorage } from './utils'

   // Add
   import api from './services/api'
   ```

2. **Load data from API on mount:**
   ```typescript
   useEffect(() => {
     loadAllData()
   }, [])

   const loadAllData = async () => {
     const tasks = await api.tasks.list()
     setTasks(tasks)
     // etc...
   }
   ```

3. **Make CRUD operations async:**
   ```typescript
   const createTask = async (formData) => {
     const newTask = await api.tasks.create(formData)
     setTasks([...tasks, newTask])
   }
   ```

4. **Add error handling:**
   ```typescript
   try {
     await api.tasks.create(formData)
   } catch (error) {
     console.error('Failed:', error)
     // Show error to user
   }
   ```

**See `APP_MIGRATION_CHANGES.md` for complete diff.**

---

## Development Tips

### Debugging

- **Electron DevTools:** Opens automatically in dev mode
- **Python logs:** Visible in terminal running Electron
- **Network requests:** Check DevTools Network tab
- **Database:** Use [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect `data/aven.db`

### Common Issues

**"Port 8000 already in use"**
- Kill existing Python process: `pkill -f "python main.py"`

**"window.api is undefined"**
- Make sure Electron's preload script is loading
- Check `webPreferences` in `electron/main.js`

**"Failed to connect to backend"**
- Ensure Python backend started successfully
- Check terminal for Python errors
- Try accessing http://127.0.0.1:8000 in browser

---

## Next Steps

1. **Adapt App.tsx** - Apply changes from `APP_MIGRATION_CHANGES.md`
2. **Test all views** - Dashboard, Kanban, Timeline, etc.
3. **Add features** - Extend modules as needed
4. **Polish UI** - Connect remaining components to API
5. **Package** - Build distributable app

---

## What's Next?

This prototype demonstrates the **foundation**. From here you can:

- ✅ Add more modules (Budget, Documents, Timeline)
- ✅ Implement knowledge engine module (local LLM)
- ✅ Migrate from SQLite to PostgreSQL (just swap data layer)
- ✅ Add cloud sync module (optional)
- ✅ Expand automation rules engine

**All architecture patterns are in place - just build on this foundation!**

---

## Technical Notes

### Why This Stack?

- **Electron**: Cross-platform desktop app packaging
- **React + TypeScript**: Modern UI with type safety
- **Python**: Perfect for AI/ML integration later
- **FastAPI**: Modern, fast, auto-documented APIs
- **SQLite**: Zero-config, offline-first database

### Migration Path

This is designed for easy PostgreSQL migration:
- SQLite now (development, single-user)
- PostgreSQL later (production, multi-user, cloud)
- Just swap data layer implementation - no app code changes!

---

## License

MIT

---

## Questions?

Check the documentation:
- `ARCHITECTURE.md` - Overall system design
- `SCHEMA-COMPATIBILITY.md` - Database migration guide
- `REACT-MIGRATION-GUIDE.md` - Full React adaptation guide
- `PROJECT-STRUCTURE.md` - Detailed structure explanation

---

**🎉 You now have a fully functional AvenStudio prototype!**
