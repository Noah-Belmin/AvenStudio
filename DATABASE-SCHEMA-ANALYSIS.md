# Database Schema: Current vs Needed
**Crossover Analysis**

---

## ✅ Currently Implemented (3 tables)

### 1. tasks
```sql
CREATE TABLE tasks (
    id, title, description, status, priority, category,
    tags, due_date, start_date, assigned_to, created_by,
    estimated_hours, completion_percentage, blocked_by,
    comments, attachments, checklist, subtasks, custom_fields,
    created_at, updated_at
)
```
**Status:** ✅ Implemented, but **missing `project_id` foreign key**

### 2. categories
```sql
CREATE TABLE categories (
    name, created_at
)
```
**Status:** ✅ Implemented (basic version)

### 3. automation_rules
```sql
CREATE TABLE automation_rules (
    id, name, description, enabled, trigger, conditions,
    actions, created_at, updated_at, last_triggered, trigger_count
)
```
**Status:** ✅ Implemented

---

## 🔴 Missing from Design Brief (6 core tables)

### 4. projects ⚠️ CRITICAL - Blocks everything
```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    project_type TEXT CHECK(project_type IN ('self-build', 'custom-build', 'renovation')),
    start_date TEXT,
    target_completion TEXT,
    status TEXT DEFAULT 'planning',
    budget_total REAL,
    created_at TEXT,
    updated_at TEXT
);
```
**Why critical:** Every other table needs `project_id` FK
**Design brief reference:** Section 8, line 517-518

---

### 5. budget_items
```sql
CREATE TABLE budget_items (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    category TEXT,  -- groundworks, structure, M&E, finishes, etc.
    item_name TEXT,
    estimated_cost REAL,
    actual_cost REAL,
    variance REAL,  -- calculated: actual - estimated
    supplier TEXT,
    quote_date TEXT,
    status TEXT,  -- quoted, approved, ordered, paid
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```
**Design brief reference:** Section 8, line 525-527

---

### 6. documents
```sql
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    filename TEXT,
    file_path TEXT,  -- actual file storage location
    document_type TEXT,  -- planning, building_regs, certificate, drawing, etc.
    version INTEGER DEFAULT 1,
    linked_task_id TEXT,
    linked_phase TEXT,
    upload_date TEXT,
    tags TEXT,  -- JSON array
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (linked_task_id) REFERENCES tasks(id)
);
```
**Design brief reference:** Section 8, line 529-532

---

### 7. contacts
```sql
CREATE TABLE contacts (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    role TEXT,  -- architect, builder, engineer, supplier, plumber, etc.
    company TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    notes TEXT,  -- JSON array of timestamped notes
    contracts TEXT,  -- JSON array of contract details
    performance_rating INTEGER CHECK(performance_rating BETWEEN 1 AND 5),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```
**Design brief reference:** Section 8, line 533-535

---

### 8. milestones
```sql
CREATE TABLE milestones (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    phase TEXT,  -- pre-planning, groundworks, structure, first-fix, etc.
    target_date TEXT,
    actual_date TEXT,
    status TEXT DEFAULT 'pending',  -- pending, in-progress, completed, delayed
    dependencies TEXT,  -- JSON array of milestone IDs
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```
**Design brief reference:** Section 8, line 537-538

---

### 9. materials
```sql
CREATE TABLE materials (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    item_name TEXT NOT NULL,
    quantity REAL,
    unit TEXT,  -- m², linear m, tonnes, units, etc.
    supplier_id TEXT,
    cost REAL,
    lead_time_days INTEGER,
    delivery_date TEXT,
    delivery_status TEXT,  -- ordered, in-transit, delivered, overdue
    warranty_info TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (supplier_id) REFERENCES contacts(id)
);
```
**Design brief reference:** Section 8, line 540-542

---

## 🔄 Required Updates to Existing Tables

### tasks table - ADD project_id
```sql
ALTER TABLE tasks ADD COLUMN project_id TEXT;
-- Then add foreign key constraint (requires recreation in SQLite)
```
**Why:** Tasks need to belong to a project
**Impact:** Breaking change - need migration script

### tasks table - ADD phase column
```sql
ALTER TABLE tasks ADD COLUMN phase TEXT;
-- Values: pre-planning, planning, groundworks, structure, first-fix,
--         second-fix, finishes, snagging, etc.
```
**Why:** UK build workflow organizes by phases
**Impact:** Non-breaking, can add gradually

### categories table - ADD project_id
```sql
ALTER TABLE categories ADD COLUMN project_id TEXT;
-- Make categories project-specific, not global
```
**Why:** Different projects may have different categories
**Impact:** Breaking change - need to decide if categories are global or per-project

---

## 📊 Complete Schema Map

| Table | Exists? | Missing Fields | Design Brief Section | Priority |
|-------|---------|----------------|---------------------|----------|
| **tasks** | ✅ Yes | `project_id`, `phase` | Line 520-523 | 🔴 Critical |
| **categories** | ✅ Yes | `project_id` (optional) | Implied | 🟡 Medium |
| **automation_rules** | ✅ Yes | None | Implied | ✅ Complete |
| **projects** | ❌ No | Entire table | Line 517-518 | 🔴 **BLOCKING** |
| **budget_items** | ❌ No | Entire table | Line 525-527 | 🔴 Critical |
| **documents** | ❌ No | Entire table | Line 529-532 | 🔴 Critical |
| **contacts** | ❌ No | Entire table | Line 533-535 | 🔴 Critical |
| **milestones** | ❌ No | Entire table | Line 537-538 | 🟡 High |
| **materials** | ❌ No | Entire table | Line 540-542 | 🟡 High |

**Summary:**
- ✅ **3 tables implemented** (tasks, categories, automation_rules)
- ❌ **6 tables missing** (projects, budget_items, documents, contacts, milestones, materials)
- 🔄 **2 tables need updates** (tasks, categories - add project_id)

---

## 🎯 No Duplication - They're Complementary

**Answer to your question: No crossover, they're all needed.**

The existing 3 tables are **generic task management**:
- tasks
- categories
- automation_rules

The missing 6 tables are **UK self-build specific**:
- projects (multi-project support)
- budget_items (financial tracking)
- documents (planning docs, building regs, certificates)
- contacts (architects, builders, suppliers)
- milestones (planning permission, building control, completion)
- materials (bricks, timber, windows, etc.)

**They work together:**
```
projects
  └── tasks (linked via project_id, organized by phase)
  └── budget_items (linked via project_id)
  └── documents (linked via project_id, can link to tasks)
  └── contacts (linked via project_id, assignees for tasks)
  └── milestones (linked via project_id, mark key dates)
  └── materials (linked via project_id, linked to suppliers)
```

---

## 🚨 Critical Issue: Missing project_id

**Current tasks table has NO project_id!**

This means:
- ❌ Can't have multiple projects
- ❌ All tasks mix together
- ❌ Can't filter by project
- ❌ Can't archive a project
- ❌ Single-project limitation

**This blocks the entire design brief vision.**

---

## 🔧 Migration Path

### Phase 1: Add projects table (1 day)
```sql
CREATE TABLE projects (...);

-- Create default project for existing data
INSERT INTO projects (id, name, status)
VALUES ('default-project', 'My Self-Build', 'active');
```

### Phase 2: Update tasks table (1 day)
```sql
-- Create new tasks table with project_id
CREATE TABLE tasks_new (..., project_id TEXT, ...);

-- Migrate existing data
INSERT INTO tasks_new
SELECT *, 'default-project' as project_id FROM tasks;

-- Swap tables
DROP TABLE tasks;
ALTER TABLE tasks_new RENAME TO tasks;
```

### Phase 3: Add remaining tables (1-2 days)
```sql
CREATE TABLE budget_items (...);
CREATE TABLE documents (...);
CREATE TABLE contacts (...);
CREATE TABLE milestones (...);
CREATE TABLE materials (...);
```

**Total migration time: 3-4 days**

---

## 📋 Recommendation

**Step 1:** Add `projects` table immediately (highest priority)
**Step 2:** Update `tasks` table to include `project_id` and `phase`
**Step 3:** Add remaining 6 tables based on feature priority:
  - High: budget_items, documents, contacts
  - Medium: milestones, materials

All 9 tables are needed for the full vision. **No duplication, all complementary.**

---

## 🎯 Design Brief Schemas Were Examples

You mentioned the design brief schemas were "examples" - that's partially true:

**What was exemplary:**
- The specific categories (groundworks, structure, etc.)
- The exact phases listed
- The number of milestones

**What's NOT exemplary (must have):**
- The table structure (projects, tasks, budget, documents, etc.)
- The relationships (project_id foreign keys)
- The data model (how everything links together)

**You can't build AvenStudio without these 9 tables** - they're the foundation, not examples.

---

**Generated:** November 23, 2025
**Status:** 3 of 9 tables complete, 6 tables + migrations needed
