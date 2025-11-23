# AvenStudio Architecture
## Modular, Migration-Ready Design

**Status:** Foundation Phase
**Date:** November 2025
**Version:** 1.0

---

## Core Philosophy

AvenStudio is designed with **strategic edges** that allow:

1. **Database migration** (SQLite → PostgreSQL) without app rewrites
2. **Modular plugins** that can be added/removed without breaking core
3. **Intelligence layers** (no AI → local LLM → cloud models) as drop-ins
4. **Clean separation** between UI, orchestration, modules, and data

**The app must work perfectly even when modules are missing.**

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  UI Layer (Electron)                 │
│           HTML/CSS/JS + Python Bridge                │
└───────────────────────┬─────────────────────────────┘
                        │ Events / Requests
                        │
┌───────────────────────▼─────────────────────────────┐
│              Core Orchestrator (Python)              │
│                                                      │
│  - Routes all requests                              │
│  - Validates permissions                            │
│  - Manages module lifecycle                         │
│  - Enforces data contracts                          │
│  - NO business logic lives here                     │
└──────┬─────────┬──────────┬──────────┬─────────────┘
       │         │          │          │
       │         │          │          │
   ┌───▼───┐ ┌──▼────┐ ┌───▼────┐ ┌───▼──────────┐
   │Tasks  │ │Budget │ │Timeline│ │Knowledge     │
   │Module │ │Module │ │Module  │ │Engine Module │
   │       │ │       │ │        │ │(OPTIONAL)    │
   └───┬───┘ └──┬────┘ └───┬────┘ └───┬──────────┘
       │        │          │          │
       └────────┴──────────┴──────────┘
                        │
            ┌───────────▼────────────┐
            │  Data Access Layer      │
            │  (Abstract Interface)   │
            └───────────┬────────────┘
                        │
            ┌───────────▼────────────┐
            │    Database Driver      │
            │  SQLite NOW → Postgres  │
            └─────────────────────────┘
```

---

## Layer Responsibilities

### 1. UI Layer (Electron + HTML/CSS/JS)

**Responsibilities:**
- Render views
- Capture user input
- Emit events (never calls DB directly)
- Update based on responses

**Rules:**
- NEVER import database modules
- NEVER call modules directly
- ALL requests go through orchestrator API
- Stateless (orchestrator holds truth)

**Example:**
```javascript
// Good: Event → Orchestrator
window.api.tasks.create({
    title: "Submit building regs",
    priority: "high"
});

// Bad: Direct module call
import { TaskModule } from './modules/tasks';  // ❌ NEVER
```

---

### 2. Core Orchestrator

**Location:** `backend/orchestrator.py`

**Responsibilities:**
- Route requests to correct module
- Validate data contracts
- Manage module registry
- Handle module lifecycle (load/unload)
- Enforce permissions
- Aggregate responses

**DOES NOT:**
- Contain business logic
- Know about module internals
- Touch database directly
- Make decisions (modules do that)

**Contract:**
```python
class Orchestrator:
    def __init__(self, config):
        self.modules = {}
        self.data_layer = DataAccessLayer(config.db_type)
        self._discover_modules()

    def handle_request(self, request: Request) -> Response:
        """
        Routes request to appropriate module.
        If module missing → graceful degradation.
        """
        module_name = request.target_module

        if module_name not in self.modules:
            return Response.module_not_available(module_name)

        module = self.modules[module_name]
        return module.handle(request, self.data_layer)

    def _discover_modules(self):
        """Auto-discover and register modules at startup"""
        pass
```

---

### 3. Modules (Plugins)

**Location:** `backend/modules/{module_name}/`

Each module is **self-contained** and follows this structure:

```
backend/modules/tasks/
├── __init__.py
├── metadata.json          # Name, version, capabilities
├── handlers.py            # Request handlers
├── schemas.py             # Data validation schemas
├── migrations/            # DB schema for this module
│   ├── sqlite/
│   │   └── 001_initial.sql
│   └── postgres/
│       └── 001_initial.sql
└── tests/
```

**Module Contract:**
```python
# backend/modules/tasks/handlers.py

class TaskModule:
    """
    Task management module.
    Can be removed without breaking core app.
    """

    def __init__(self):
        self.name = "tasks"
        self.version = "1.0.0"
        self.dependencies = []  # Other modules this needs

    def handle(self, request: Request, data_layer: DataAccessLayer) -> Response:
        """
        Handle task-related requests.

        RULES:
        - Use data_layer for ALL database access
        - NEVER import database driver directly
        - Return Response object (never raise exceptions)
        - Validate all inputs with schemas
        """
        if request.action == "create":
            return self._create_task(request.data, data_layer)
        elif request.action == "list":
            return self._list_tasks(request.filters, data_layer)
        # ...

    def _create_task(self, data, data_layer):
        # Validate
        schema = TaskCreateSchema()
        validated = schema.validate(data)

        # Use data layer (never raw SQL here)
        task_id = data_layer.insert("tasks", validated)

        return Response.success({"task_id": task_id})
```

**metadata.json:**
```json
{
    "name": "tasks",
    "version": "1.0.0",
    "description": "Task management for self-build projects",
    "author": "AvenStudio",
    "capabilities": [
        "tasks.create",
        "tasks.update",
        "tasks.delete",
        "tasks.list",
        "tasks.search"
    ],
    "dependencies": [],
    "optional_integrations": ["knowledge_engine"],
    "database_tables": ["tasks", "task_dependencies"],
    "hooks": {
        "on_project_created": "initialize_default_tasks",
        "on_timeline_updated": "adjust_task_dates"
    }
}
```

---

### 4. Data Access Layer (Abstract Interface)

**Location:** `backend/data/access_layer.py`

**Purpose:**
- Single interface for all database operations
- Hides SQLite vs PostgreSQL differences
- Makes migration seamless

**Contract:**
```python
from abc import ABC, abstractmethod

class DataAccessLayer(ABC):
    """
    Abstract interface for database operations.
    Implementations: SQLiteDataLayer, PostgresDataLayer
    """

    @abstractmethod
    def insert(self, table: str, data: dict) -> Any:
        """Insert record, return ID"""
        pass

    @abstractmethod
    def update(self, table: str, id: Any, data: dict) -> bool:
        """Update record by ID"""
        pass

    @abstractmethod
    def delete(self, table: str, id: Any) -> bool:
        """Delete record by ID"""
        pass

    @abstractmethod
    def get(self, table: str, id: Any) -> Optional[dict]:
        """Get single record by ID"""
        pass

    @abstractmethod
    def query(self, table: str, filters: dict, order_by: str = None) -> list:
        """Query with filters"""
        pass

    @abstractmethod
    def execute_raw(self, query: str, params: tuple = ()) -> Any:
        """Execute raw SQL (use sparingly)"""
        pass


# Implementation for SQLite
class SQLiteDataLayer(DataAccessLayer):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def insert(self, table: str, data: dict) -> int:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self.conn.execute(query, tuple(data.values()))
        self.conn.commit()
        return cursor.lastrowid

    # ... other methods


# Implementation for PostgreSQL
class PostgresDataLayer(DataAccessLayer):
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)

    def insert(self, table: str, data: dict) -> UUID:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"

        cursor = self.conn.cursor()
        cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        return cursor.fetchone()[0]

    # ... other methods
```

**Modules ONLY interact with this layer, never the database directly.**

---

### 5. Knowledge Engine Module (Optional)

**Location:** `backend/modules/knowledge_engine/`

**The knowledge engine is JUST ANOTHER MODULE.**

It implements the same contract, but provides intelligence services.

**Interface Contract:**
```python
# backend/modules/knowledge_engine/interface.py

class KnowledgeEngineInterface(ABC):
    """
    Contract for AI/intelligence services.
    Can be implemented by:
    - NoOpKnowledgeEngine (does nothing)
    - LocalLLMEngine (small local model)
    - CloudLLMEngine (remote API)
    - HybridEngine (mix of both)
    """

    @abstractmethod
    def suggest_next_tasks(self, project_id: str, context: dict) -> list:
        """Suggest tasks based on project state"""
        pass

    @abstractmethod
    def explain_concept(self, term: str, user_level: str) -> str:
        """Explain construction terms at user's level"""
        pass

    @abstractmethod
    def check_decision_impacts(self, decision: dict) -> list:
        """Analyze decision impacts (cost, schedule, quality)"""
        pass

    @abstractmethod
    def generate_risk_warnings(self, project_state: dict) -> list:
        """Identify potential risks"""
        pass


# No-op implementation (default)
class NoOpKnowledgeEngine(KnowledgeEngineInterface):
    """Used when knowledge engine is disabled"""

    def suggest_next_tasks(self, project_id, context):
        return []  # No suggestions

    def explain_concept(self, term, user_level):
        return f"Information about '{term}' is not available."

    # ... returns empty/default for all methods


# Local LLM implementation
class LocalLLMEngine(KnowledgeEngineInterface):
    def __init__(self, model_path: str):
        self.model = load_local_model(model_path)

    def suggest_next_tasks(self, project_id, context):
        prompt = self._build_prompt(context)
        response = self.model.generate(prompt)
        return self._parse_suggestions(response)

    # ... actual AI logic
```

**The orchestrator doesn't care which implementation is active:**

```python
# backend/orchestrator.py

class Orchestrator:
    def __init__(self, config):
        self.modules = {}

        # Knowledge engine selection
        if config.knowledge_engine == "local":
            self.knowledge = LocalLLMEngine(config.model_path)
        elif config.knowledge_engine == "cloud":
            self.knowledge = CloudLLMEngine(config.api_key)
        else:
            self.knowledge = NoOpKnowledgeEngine()

        # Register as optional service
        self.services = {
            "knowledge": self.knowledge
        }
```

---

## Database Migration Strategy

### SQLite → PostgreSQL Schema Compatibility

Your existing Postgres schemas need **adaptation** for SQLite. Here's the strategy:

#### Write Dual Schemas

Each module maintains **both** SQLite and PostgreSQL versions:

```
backend/modules/tasks/migrations/
├── sqlite/
│   └── 001_initial.sql
└── postgres/
    └── 001_initial.sql
```

#### Key Adaptations Needed

| PostgreSQL Feature | SQLite Equivalent |
|---|---|
| `UUID` type | `TEXT` (store as string) |
| `ENUM` types | `TEXT` with `CHECK` constraint |
| `JSONB` | `JSON` (no binary format) |
| `ARRAY` | JSON array as `TEXT` |
| `TIMESTAMPTZ` | `TEXT` (ISO 8601 format) |
| `SERIAL` / `BIGSERIAL` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `RETURNING` clause | Use `cursor.lastrowid` |
| Extensions (`uuid-ossp`, `pg_trgm`) | Application-level UUIDs, FTS5 |

#### Example Dual Schema

**PostgreSQL version:**
```sql
-- backend/modules/tasks/migrations/postgres/001_initial.sql

CREATE TYPE task_status AS ENUM ('todo', 'in_progress', 'review', 'blocked', 'done');
CREATE TYPE task_priority AS ENUM ('urgent', 'high', 'medium', 'low');

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    status task_status DEFAULT 'todo',
    priority task_priority DEFAULT 'medium',
    due_date TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

**SQLite version (compatible):**
```sql
-- backend/modules/tasks/migrations/sqlite/001_initial.sql

CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,  -- UUID stored as TEXT
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'review', 'blocked', 'done')),
    priority TEXT DEFAULT 'medium' CHECK(priority IN ('urgent', 'high', 'medium', 'low')),
    due_date TEXT,  -- ISO 8601 datetime string
    metadata TEXT DEFAULT '{}',  -- JSON as TEXT
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

#### Migration Tool

```python
# backend/data/migrator.py

class SchemaManager:
    """Manages schema migrations for current database type"""

    def __init__(self, data_layer: DataAccessLayer, db_type: str):
        self.data_layer = data_layer
        self.db_type = db_type  # "sqlite" or "postgres"

    def apply_module_migrations(self, module_name: str):
        """Apply migrations for a module"""
        migration_path = f"backend/modules/{module_name}/migrations/{self.db_type}"

        # Read migration files in order
        migrations = sorted(Path(migration_path).glob("*.sql"))

        for migration_file in migrations:
            with open(migration_file) as f:
                sql = f.read()
                self.data_layer.execute_raw(sql)
```

---

## Configuration-Driven Behavior

**Config file:** `config.yaml`

```yaml
app:
  name: "AvenStudio"
  version: "0.1.0"
  environment: "development"  # development, production

database:
  type: "sqlite"  # sqlite | postgres
  sqlite:
    path: "data/aven.db"
  postgres:
    host: "localhost"
    port: 5432
    database: "avenstudio"
    user: "postgres"
    password: "password"

modules:
  enabled:
    - tasks
    - budget
    - timeline
    - documents
    - contacts
  # Optional modules
  optional:
    - knowledge_engine
    - ai_assistant

knowledge_engine:
  enabled: false  # Can disable entirely
  mode: "none"    # none | local | cloud | hybrid
  local:
    model_path: "models/llama-3-8b"
    max_tokens: 2048
  cloud:
    provider: "anthropic"
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-haiku"

features:
  offline_mode: true
  auto_backup: true
  backup_interval_hours: 24
```

---

## Module Hot-Swapping

Modules can be added/removed at **runtime** without restarting:

```python
# Example: Adding knowledge engine mid-session

orchestrator = Orchestrator.get_instance()

# Check if knowledge engine available
if orchestrator.has_module("knowledge_engine"):
    # Use it
    suggestions = orchestrator.call("knowledge_engine.suggest_tasks", {...})
else:
    # Graceful degradation
    suggestions = []  # Manual task creation
```

---

## Development Phases

### Phase 1: Core + SQLite (Current)
- Build orchestrator
- Implement 3-5 core modules (tasks, budget, timeline)
- SQLite data layer
- Basic UI with static data
- **No knowledge engine yet**

### Phase 2: Module Expansion
- Add documents, contacts, materials modules
- Refine module contracts
- Test hot-swapping
- UI connects to orchestrator

### Phase 3: Intelligence Layer
- Add NoOpKnowledgeEngine
- Implement local LLM option
- Test with/without engine
- UI remains unchanged

### Phase 4: PostgreSQL Migration
- Implement PostgresDataLayer
- Test dual-schema migrations
- Config toggle: SQLite ↔ Postgres
- Zero UI changes

### Phase 5: Cloud Features
- Cloud sync module (optional)
- Remote knowledge engine option
- Multi-user collaboration module
- Still works offline

---

## Key Principles

1. **UI never knows about database type** (SQLite vs Postgres)
2. **Modules never know about other modules** (orchestrator mediates)
3. **Knowledge engine is optional** (app works without it)
4. **Data layer is abstract** (swap implementations)
5. **Configuration drives behavior** (no hardcoded assumptions)

---

## Next Steps

1. ✅ Define orchestrator API contract
2. ⬜ Build SQLite data access layer
3. ⬜ Create first module (tasks) with dual schemas
4. ⬜ Connect UI to orchestrator (not direct DB)
5. ⬜ Test module hot-swapping
6. ⬜ Add knowledge engine interface (no-op first)

---

**This architecture ensures AvenStudio can:**
- Start simple (SQLite, no AI)
- Scale intelligently (Postgres, local/cloud LLM)
- Remain modular (add/remove features)
- Never collapse under its own complexity
