"""
SQLite Data Access Layer
Provides database operations for SQLite
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class SQLiteDataLayer:
    """SQLite implementation of data access layer"""

    def __init__(self, db_path: str):
        """Initialize SQLite connection"""
        self.db_path = db_path

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Connect to database
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dicts
        print(f"✅ Connected to SQLite: {db_path}")

    def initialize_schema(self):
        """Create tables if they don't exist"""
        cursor = self.conn.cursor()

        # ==================== PROJECTS TABLE ====================
        # Core table - all other tables link to projects
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT,
            project_type TEXT DEFAULT 'self-build' CHECK(project_type IN ('self-build', 'custom-build', 'renovation')),
            start_date TEXT,
            target_completion TEXT,
            status TEXT DEFAULT 'planning' CHECK(status IN ('planning', 'in-progress', 'on-hold', 'completed', 'archived')),
            budget_total REAL,
            description TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
        ''')

        # Create default project if none exists
        cursor.execute('SELECT COUNT(*) FROM projects')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO projects (id, name, status)
            VALUES ('default-project', 'My Self-Build Project', 'planning')
            ''')
            print("📁 Created default project")

        # ==================== TASKS TABLE ====================
        # Enhanced with project_id and phase for UK self-build workflow
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL DEFAULT 'default-project',
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in-progress', 'review', 'blocked', 'done')),
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
            category TEXT NOT NULL,
            phase TEXT,
            tags TEXT DEFAULT '[]',
            due_date TEXT,
            start_date TEXT,
            assigned_to TEXT,
            created_by TEXT,
            estimated_hours REAL,
            completion_percentage INTEGER DEFAULT 0 CHECK(completion_percentage BETWEEN 0 AND 100),
            blocked_by TEXT DEFAULT '[]',
            comments TEXT DEFAULT '[]',
            attachments TEXT DEFAULT '[]',
            checklist TEXT DEFAULT '[]',
            subtasks TEXT DEFAULT '[]',
            custom_fields TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
        ''')

        # ==================== BUDGET ITEMS TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_items (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            category TEXT NOT NULL,
            item_name TEXT NOT NULL,
            estimated_cost REAL DEFAULT 0,
            actual_cost REAL DEFAULT 0,
            supplier TEXT,
            quote_date TEXT,
            status TEXT DEFAULT 'estimated' CHECK(status IN ('estimated', 'quoted', 'approved', 'ordered', 'paid')),
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
        ''')

        # ==================== DOCUMENTS TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            document_type TEXT DEFAULT 'other' CHECK(document_type IN ('planning', 'building_regs', 'certificate', 'drawing', 'contract', 'invoice', 'photo', 'other')),
            version INTEGER DEFAULT 1,
            linked_task_id TEXT,
            linked_phase TEXT,
            upload_date TEXT DEFAULT (datetime('now')),
            tags TEXT DEFAULT '[]',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (linked_task_id) REFERENCES tasks(id) ON DELETE SET NULL
        )
        ''')

        # ==================== CONTACTS TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'other',
            company TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            notes TEXT DEFAULT '[]',
            contracts TEXT DEFAULT '[]',
            performance_rating INTEGER CHECK(performance_rating BETWEEN 1 AND 5),
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
        ''')

        # ==================== MILESTONES TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            name TEXT NOT NULL,
            phase TEXT,
            target_date TEXT,
            actual_date TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in-progress', 'completed', 'delayed', 'cancelled')),
            dependencies TEXT DEFAULT '[]',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
        ''')

        # ==================== MATERIALS TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            item_name TEXT NOT NULL,
            quantity REAL,
            unit TEXT DEFAULT 'units',
            supplier_id TEXT,
            cost REAL DEFAULT 0,
            lead_time_days INTEGER DEFAULT 0,
            delivery_date TEXT,
            delivery_status TEXT DEFAULT 'not-ordered' CHECK(delivery_status IN ('not-ordered', 'ordered', 'in-transit', 'delivered', 'overdue')),
            warranty_info TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (supplier_id) REFERENCES contacts(id) ON DELETE SET NULL
        )
        ''')

        # ==================== CATEGORIES TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT PRIMARY KEY,
            created_at TEXT DEFAULT (datetime('now'))
        )
        ''')

        # Insert default categories for UK self-build
        default_categories = ['planning', 'groundworks', 'structure', 'first-fix', 'second-fix', 'finishes', 'external', 'other']
        for cat in default_categories:
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))

        # ==================== AUTOMATION RULES TABLE ====================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS automation_rules (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            enabled INTEGER DEFAULT 1,
            trigger TEXT NOT NULL,
            conditions TEXT NOT NULL,
            actions TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            last_triggered TEXT,
            trigger_count INTEGER DEFAULT 0
        )
        ''')

        self.conn.commit()
        print("✅ Database schema initialized")

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute raw SQL query"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetchone(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetchall(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def insert(self, table: str, data: Dict[str, Any]) -> str:
        """Insert record and return ID"""
        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = str(uuid4())

        # Convert lists/dicts to JSON strings
        data = self._serialize_data(data)

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self.conn.cursor()
        cursor.execute(query, tuple(data.values()))
        self.conn.commit()

        return data['id']

    def update(self, table: str, id: str, data: Dict[str, Any]) -> bool:
        """Update record by ID"""
        # Add updated_at timestamp
        data['updated_at'] = datetime.utcnow().isoformat()

        # Convert lists/dicts to JSON strings
        data = self._serialize_data(data)

        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"

        cursor = self.conn.cursor()
        cursor.execute(query, tuple(data.values()) + (id,))
        self.conn.commit()

        return cursor.rowcount > 0

    def delete(self, table: str, id: str) -> bool:
        """Delete record by ID"""
        query = f"DELETE FROM {table} WHERE id = ?"

        cursor = self.conn.cursor()
        cursor.execute(query, (id,))
        self.conn.commit()

        return cursor.rowcount > 0

    def get(self, table: str, id: str) -> Optional[Dict]:
        """Get single record by ID"""
        row = self.fetchone(f"SELECT * FROM {table} WHERE id = ?", (id,))
        return self._deserialize_row(row) if row else None

    def query(self, table: str, filters: Dict[str, Any] = None) -> List[Dict]:
        """Query with filters"""
        query = f"SELECT * FROM {table}"
        params = []

        if filters:
            # Remove None values
            filters = {k: v for k, v in filters.items() if v is not None}

            if filters:
                where_clauses = [f"{k} = ?" for k in filters.keys()]
                query += " WHERE " + " AND ".join(where_clauses)
                params = list(filters.values())

        rows = self.fetchall(query, tuple(params))
        return [self._deserialize_row(row) for row in rows]

    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Python objects to SQLite-compatible types"""
        serialized = {}

        for key, value in data.items():
            if isinstance(value, (list, dict)):
                # Convert to JSON string
                serialized[key] = json.dumps(value)
            elif isinstance(value, bool):
                # Convert bool to int (SQLite doesn't have bool)
                serialized[key] = 1 if value else 0
            elif isinstance(value, datetime):
                # Convert datetime to ISO string
                serialized[key] = value.isoformat()
            else:
                serialized[key] = value

        return serialized

    def _deserialize_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Convert SQLite types back to Python objects"""
        if not row:
            return None

        deserialized = dict(row)

        # Fields that should be parsed as JSON
        json_fields = [
            'tags', 'blocked_by', 'comments', 'attachments', 'checklist',
            'subtasks', 'custom_fields', 'conditions', 'actions',
            'notes', 'contracts', 'dependencies'  # New fields from new tables
        ]

        for field in json_fields:
            if field in deserialized and isinstance(deserialized[field], str):
                try:
                    deserialized[field] = json.loads(deserialized[field])
                except:
                    pass

        # Convert integer booleans back to bool
        if 'enabled' in deserialized:
            deserialized['enabled'] = bool(deserialized['enabled'])

        return deserialized
