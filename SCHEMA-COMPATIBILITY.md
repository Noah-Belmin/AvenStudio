# PostgreSQL → SQLite Schema Compatibility Guide
## Adapting Existing Schemas for Migration-Ready Development

**Purpose:** Convert your existing PostgreSQL schemas to SQLite-compatible versions while maintaining **identical data structures** for seamless migration later.

---

## The Strategy

Your PostgreSQL schemas are well-designed and should be preserved. The goal is:

1. **SQLite version NOW** (for local development/testing)
2. **PostgreSQL version LATER** (when scaling)
3. **Zero application changes** when migrating (data layer handles it)

---

## Conversion Rules

### 1. UUID → TEXT

**PostgreSQL:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_user_id UUID NOT NULL REFERENCES users(user_id)
);
```

**SQLite Compatible:**
```sql
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,  -- Store UUID as TEXT
    owner_user_id TEXT NOT NULL,
    FOREIGN KEY (owner_user_id) REFERENCES users(user_id)
);
```

**Application Layer (Python):**
```python
import uuid

# Generate UUIDs in application code, not database
def create_project(owner_id, data):
    project_id = str(uuid.uuid4())  # Generate in Python
    data_layer.insert('projects', {
        'project_id': project_id,
        'owner_user_id': owner_id,
        **data
    })
```

---

### 2. ENUM → TEXT with CHECK Constraint

**PostgreSQL:**
```sql
CREATE TYPE project_stage AS ENUM (
    'pre_planning',
    'planning',
    'design',
    'pre_construction',
    'construction',
    'completion',
    'post_occupancy'
);

CREATE TABLE projects (
    current_stage project_stage DEFAULT 'pre_planning'
);
```

**SQLite Compatible:**
```sql
CREATE TABLE projects (
    current_stage TEXT DEFAULT 'pre_planning'
        CHECK(current_stage IN (
            'pre_planning',
            'planning',
            'design',
            'pre_construction',
            'construction',
            'completion',
            'post_occupancy'
        ))
);
```

**Tip:** Extract enums to Python for consistency:

```python
# backend/shared/enums.py

from enum import Enum

class ProjectStage(str, Enum):
    PRE_PLANNING = 'pre_planning'
    PLANNING = 'planning'
    DESIGN = 'design'
    PRE_CONSTRUCTION = 'pre_construction'
    CONSTRUCTION = 'construction'
    COMPLETION = 'completion'
    POST_OCCUPANCY = 'post_occupancy'

# Use in both SQLite schema generation AND validation
VALID_STAGES = [s.value for s in ProjectStage]
```

---

### 3. JSONB → JSON (TEXT)

**PostgreSQL:**
```sql
CREATE TABLE projects (
    project_metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_projects_metadata ON projects USING GIN(project_metadata);
```

**SQLite Compatible:**
```sql
CREATE TABLE projects (
    project_metadata TEXT DEFAULT '{}'  -- JSON as TEXT
);

-- SQLite 3.38+ supports JSON functions
CREATE INDEX idx_projects_metadata ON projects(
    json_extract(project_metadata, '$.key')  -- Index specific JSON path
);
```

**Differences:**
- PostgreSQL `JSONB` is binary, more efficient
- SQLite `JSON` (stored as TEXT) is parsed each query
- **Both work identically from application perspective**

**Application Usage (identical for both):**
```python
# Works with both SQLite and Postgres
data_layer.insert('projects', {
    'project_metadata': json.dumps({
        'custom_field': 'value',
        'tags': ['residential', 'eco-build']
    })
})

# Query JSON (data layer handles syntax differences)
results = data_layer.query_json('projects', 'metadata.tags', contains='eco-build')
```

---

### 4. TIMESTAMPTZ → TEXT (ISO 8601)

**PostgreSQL:**
```sql
CREATE TABLE tasks (
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**SQLite Compatible:**
```sql
CREATE TABLE tasks (
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

**Application Layer (uniform handling):**
```python
from datetime import datetime, timezone

def now_utc():
    """Returns current UTC time as ISO string"""
    return datetime.now(timezone.utc).isoformat()

# Data layer normalizes timestamps automatically
data_layer.insert('tasks', {
    'created_at': now_utc(),  # 2025-11-23T14:32:01+00:00
    'title': 'Task name'
})
```

---

### 5. ARRAY → JSON Array

**PostgreSQL:**
```sql
CREATE TABLE sites (
    boundary_treatments TEXT[] DEFAULT ARRAY[]::text[]
);
```

**SQLite Compatible:**
```sql
CREATE TABLE sites (
    boundary_treatments TEXT DEFAULT '[]'  -- JSON array as TEXT
);
```

**Application Usage:**
```python
# Store arrays as JSON
data_layer.insert('sites', {
    'boundary_treatments': json.dumps(['fence', 'hedge', 'wall'])
})

# Query (data layer handles differences)
sites = data_layer.query('sites')
for site in sites:
    treatments = json.loads(site['boundary_treatments'])
```

---

### 6. SERIAL/BIGSERIAL → INTEGER AUTOINCREMENT

**PostgreSQL:**
```sql
CREATE TABLE simple_items (
    id SERIAL PRIMARY KEY,
    name TEXT
);
```

**SQLite Compatible:**
```sql
CREATE TABLE simple_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
```

**Note:** For complex schemas, prefer **UUID as TEXT** (consistent across DBs):

```sql
-- Better for distributed systems and migration
CREATE TABLE items (
    id TEXT PRIMARY KEY,  -- UUID
    name TEXT
);
```

---

### 7. RETURNING Clause

**PostgreSQL:**
```sql
INSERT INTO tasks (title, status)
VALUES ('Task name', 'todo')
RETURNING task_id;
```

**SQLite:**
```sql
INSERT INTO tasks (task_id, title, status)
VALUES ('uuid-here', 'Task name', 'todo');

-- Get last inserted ID
SELECT last_insert_rowid();  -- For INTEGER PRIMARY KEY
```

**Data Layer Abstraction:**
```python
# Data layer handles this internally

class PostgresDataLayer:
    def insert(self, table, data):
        # Use RETURNING
        query = f"INSERT INTO {table} ... RETURNING id"
        return cursor.fetchone()[0]

class SQLiteDataLayer:
    def insert(self, table, data):
        # Use lastrowid or return provided UUID
        cursor.execute(f"INSERT INTO {table} ...")
        return data.get('id') or cursor.lastrowid
```

---

### 8. Indexes and Full-Text Search

**PostgreSQL:**
```sql
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE TABLE projects (
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english',
            coalesce(project_name, '') || ' ' ||
            coalesce(site_address, '')
        )
    ) STORED
);

CREATE INDEX idx_projects_search ON projects USING GIN(search_vector);
```

**SQLite Compatible:**
```sql
-- Use FTS5 virtual table (separate table)
CREATE VIRTUAL TABLE projects_fts USING fts5(
    project_id UNINDEXED,
    project_name,
    site_address,
    content='projects',  -- Mirror of projects table
    content_rowid='rowid'
);

-- Keep in sync with triggers
CREATE TRIGGER projects_fts_insert AFTER INSERT ON projects BEGIN
    INSERT INTO projects_fts(rowid, project_id, project_name, site_address)
    VALUES (new.rowid, new.project_id, new.project_name, new.site_address);
END;

CREATE TRIGGER projects_fts_update AFTER UPDATE ON projects BEGIN
    UPDATE projects_fts
    SET project_name = new.project_name, site_address = new.site_address
    WHERE rowid = new.rowid;
END;

CREATE TRIGGER projects_fts_delete AFTER DELETE ON projects BEGIN
    DELETE FROM projects_fts WHERE rowid = old.rowid;
END;
```

**Data Layer Search Abstraction:**
```python
class DataAccessLayer:
    def search(self, table: str, query: str) -> list:
        """Full-text search (DB-agnostic)"""
        pass

class PostgresDataLayer:
    def search(self, table, query):
        return self.execute_raw(
            f"SELECT * FROM {table} WHERE search_vector @@ to_tsquery(%s)",
            (query,)
        )

class SQLiteDataLayer:
    def search(self, table, query):
        return self.execute_raw(
            f"SELECT * FROM {table}_fts WHERE {table}_fts MATCH ?",
            (query,)
        )
```

---

### 9. Triggers and Auto-Update

**PostgreSQL:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**SQLite Compatible:**
```sql
CREATE TRIGGER update_projects_updated_at
    AFTER UPDATE ON projects
    FOR EACH ROW
BEGIN
    UPDATE projects
    SET updated_at = datetime('now')
    WHERE rowid = NEW.rowid;
END;
```

**Alternative:** Handle in application layer for consistency:

```python
class DataAccessLayer:
    def update(self, table, id, data):
        # Automatically add updated_at
        data['updated_at'] = now_utc()
        # ... execute update
```

---

## Converting Your Existing Schemas

### Example: Phase 1 - Core Foundation Tables

**Your Postgres Version:**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**SQLite Equivalent:**
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    preferences TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),

    CONSTRAINT valid_email CHECK (
        email LIKE '%_@__%.__%'  -- Basic email validation
    )
);

CREATE INDEX idx_users_email ON users(email);
```

---

### Example: Projects Table

**Postgres:**
```sql
CREATE TYPE project_stage AS ENUM (...);
CREATE TYPE build_method AS ENUM (...);

CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    current_stage project_stage DEFAULT 'pre_planning',
    build_method build_method,
    project_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**SQLite:**
```sql
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    owner_user_id TEXT NOT NULL,
    current_stage TEXT DEFAULT 'pre_planning'
        CHECK(current_stage IN (
            'pre_planning', 'planning', 'design',
            'pre_construction', 'construction',
            'completion', 'post_occupancy'
        )),
    build_method TEXT
        CHECK(build_method IN (
            'traditional_masonry', 'timber_frame', 'sips',
            'icf', 'modular', 'hybrid', 'other'
        )),
    project_metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (owner_user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_projects_owner ON projects(owner_user_id);
CREATE INDEX idx_projects_stage ON projects(current_stage);
```

---

## Schema Generation Tool

Create a tool to generate both versions from a single source:

```python
# backend/tools/schema_generator.py

class SchemaGenerator:
    """
    Generates both SQLite and PostgreSQL schemas
    from a unified definition.
    """

    def __init__(self, definitions_path: str):
        self.definitions = self._load_definitions(definitions_path)

    def generate_sqlite(self, module_name: str) -> str:
        """Generate SQLite schema for module"""
        tables = self.definitions[module_name]['tables']
        sql = []

        for table_name, table_def in tables.items():
            sql.append(self._sqlite_table(table_name, table_def))

        return '\n\n'.join(sql)

    def generate_postgres(self, module_name: str) -> str:
        """Generate PostgreSQL schema for module"""
        tables = self.definitions[module_name]['tables']
        sql = []

        # ENUMs first
        for enum in self._extract_enums(tables):
            sql.append(self._postgres_enum(enum))

        for table_name, table_def in tables.items():
            sql.append(self._postgres_table(table_name, table_def))

        return '\n\n'.join(sql)

    def _sqlite_table(self, name, definition):
        # Generate SQLite CREATE TABLE
        pass

    def _postgres_table(self, name, definition):
        # Generate Postgres CREATE TABLE
        pass
```

**Schema Definition (YAML):**
```yaml
# backend/modules/tasks/schema.yaml

tasks:
  tables:
    tasks:
      columns:
        task_id:
          type: uuid
          primary_key: true
        project_id:
          type: uuid
          references: projects.project_id
          on_delete: cascade
        title:
          type: text
          nullable: false
        status:
          type: enum
          values: [todo, in_progress, review, blocked, done]
          default: todo
        priority:
          type: enum
          values: [urgent, high, medium, low]
          default: medium
        metadata:
          type: jsonb
          default: {}
        created_at:
          type: timestamp
          default: now
      indexes:
        - columns: [project_id]
        - columns: [status]
        - columns: [due_date]
```

Then generate:
```bash
python schema_generator.py tasks --output sqlite > tasks_sqlite.sql
python schema_generator.py tasks --output postgres > tasks_postgres.sql
```

---

## Testing Strategy

### Dual Schema Tests

```python
# tests/test_schemas.py
import pytest

@pytest.mark.parametrize("db_type", ["sqlite", "postgres"])
def test_task_creation(db_type):
    """Test task creation works identically in both DBs"""

    # Setup
    if db_type == "sqlite":
        data_layer = SQLiteDataLayer(":memory:")
    else:
        data_layer = PostgresDataLayer(test_connection_string)

    # Apply schema
    schema_manager = SchemaManager(data_layer, db_type)
    schema_manager.apply_module_migrations("tasks")

    # Test (same code for both)
    task_id = data_layer.insert('tasks', {
        'task_id': str(uuid.uuid4()),
        'project_id': str(uuid.uuid4()),
        'title': 'Test task',
        'status': 'todo',
        'priority': 'high'
    })

    # Verify
    task = data_layer.get('tasks', task_id)
    assert task['title'] == 'Test task'
    assert task['status'] == 'todo'
```

---

## Migration Path

When ready to move from SQLite → PostgreSQL:

1. **Export data from SQLite**
   ```python
   exporter = DataExporter(sqlite_layer)
   data = exporter.export_all()  # JSON format
   ```

2. **Apply PostgreSQL schemas**
   ```python
   schema_manager = SchemaManager(postgres_layer, "postgres")
   schema_manager.apply_all_migrations()
   ```

3. **Import data to PostgreSQL**
   ```python
   importer = DataImporter(postgres_layer)
   importer.import_all(data)  # Handles type conversions
   ```

4. **Update config.yaml**
   ```yaml
   database:
     type: "postgres"  # Changed from "sqlite"
   ```

5. **Restart app** - everything works identically

---

## Recommendation for Your Project

### For Existing Postgres Schemas:

1. **Keep them as the source of truth** - they're well-designed
2. **Generate SQLite versions** using conversion rules above
3. **Test both versions** with identical application code
4. **Use data layer abstraction** - app never knows which DB

### File Structure:

```
backend/modules/
├── tasks/
│   ├── migrations/
│   │   ├── sqlite/
│   │   │   └── 001_initial.sql  (converted)
│   │   └── postgres/
│   │       └── 001_initial.sql  (original)
│   └── schema.yaml  (optional: unified definition)
```

### Start Simple:

Convert **7 core tables first**:
1. users
2. projects
3. tasks
4. budget_items
5. documents
6. contacts
7. milestones

Add complex schemas (risk assessments, standards tracking, etc.) **as modules later**.

---

## Key Takeaways

✅ **Your PostgreSQL schemas are excellent** - don't abandon them
✅ **SQLite versions are straightforward** - use conversion rules above
✅ **Data layer makes migration seamless** - app code doesn't change
✅ **Test both versions regularly** - catch incompatibilities early
✅ **UUIDs as TEXT** - consistent across both databases
✅ **Enums as TEXT + CHECK** - validation in both DB and Python
✅ **JSON instead of JSONB** - same API, different storage

**You can develop locally with SQLite confidence, knowing PostgreSQL migration will be painless.**
