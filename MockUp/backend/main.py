"""
AvenStudio Backend - FastAPI Application
Main entry point for Python backend server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import Orchestrator

# Initialize FastAPI app
app = FastAPI(
    title="AvenStudio API",
    description="Backend API for AvenStudio self-build management platform",
    version="0.1.0"
)

# Enable CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/aven.db')
orchestrator = Orchestrator({
    'db_type': 'sqlite',
    'db_path': DB_PATH
})

print(f"✅ Database initialized at: {DB_PATH}")


# ============================================================================
# Pydantic Models (match TypeScript types)
# ============================================================================

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    category: str
    tags: List[str] = []
    dueDate: Optional[str] = None
    startDate: Optional[str] = None
    assignedTo: Optional[str] = None
    estimatedHours: Optional[float] = None
    completionPercentage: Optional[int] = 0
    blockedBy: List[str] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    dueDate: Optional[str] = None
    startDate: Optional[str] = None
    completionPercentage: Optional[int] = None
    estimatedHours: Optional[float] = None
    blockedBy: Optional[List[str]] = None


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class AutomationRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    enabled: bool = True
    trigger: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]


class AutomationExecute(BaseModel):
    taskId: str
    trigger: str


# ============================================================================
# Health Check
# ============================================================================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "0.1.0",
        "message": "AvenStudio API is running"
    }


# ============================================================================
# Tasks Endpoints
# ============================================================================

@app.get("/api/tasks")
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None
):
    """List all tasks with optional filters"""
    try:
        response = orchestrator.handle_request({
            'module': 'tasks',
            'action': 'list',
            'filters': {
                'status': status,
                'priority': priority,
                'category': category
            }
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """Get single task by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'tasks',
            'action': 'get',
            'id': task_id
        })

        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Task not found")

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tasks")
def create_task(task: TaskCreate):
    """Create new task"""
    try:
        response = orchestrator.handle_request({
            'module': 'tasks',
            'action': 'create',
            'data': task.dict()
        })

        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    """Update existing task"""
    try:
        response = orchestrator.handle_request({
            'module': 'tasks',
            'action': 'update',
            'id': task_id,
            'data': task.dict(exclude_unset=True)
        })

        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Task not found")

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete task"""
    try:
        response = orchestrator.handle_request({
            'module': 'tasks',
            'action': 'delete',
            'id': task_id
        })

        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Task not found")

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Stats Endpoint
# ============================================================================

@app.get("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    try:
        response = orchestrator.handle_request({
            'module': 'stats',
            'action': 'get_dashboard_stats'
        })
        return response.get('data', {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Categories Endpoints
# ============================================================================

@app.get("/api/categories")
def list_categories():
    """List all categories"""
    try:
        response = orchestrator.handle_request({
            'module': 'categories',
            'action': 'list'
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/categories")
def create_category(category: CategoryCreate):
    """Create new category"""
    try:
        response = orchestrator.handle_request({
            'module': 'categories',
            'action': 'create',
            'data': category.dict()
        })

        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/categories/{category_name}")
def update_category(category_name: str, category: CategoryUpdate):
    """Update category name"""
    try:
        response = orchestrator.handle_request({
            'module': 'categories',
            'action': 'update',
            'id': category_name,
            'data': category.dict()
        })

        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Category not found")

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/categories/{category_name}")
def delete_category(category_name: str):
    """Delete category"""
    try:
        response = orchestrator.handle_request({
            'module': 'categories',
            'action': 'delete',
            'id': category_name
        })

        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Category not found")

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Automation Rules Endpoints
# ============================================================================

@app.get("/api/automation/rules")
def list_automation_rules():
    """List all automation rules"""
    try:
        response = orchestrator.handle_request({
            'module': 'automation',
            'action': 'list_rules'
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/automation/rules")
def create_automation_rule(rule: AutomationRuleCreate):
    """Create automation rule"""
    try:
        response = orchestrator.handle_request({
            'module': 'automation',
            'action': 'create_rule',
            'data': rule.dict()
        })

        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))

        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/automation/execute")
def execute_automation(data: AutomationExecute):
    """Execute automation rules for a task"""
    try:
        response = orchestrator.handle_request({
            'module': 'automation',
            'action': 'execute',
            'data': data.dict()
        })
        return {"success": True, "triggered": response.get('data', [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting AvenStudio Backend...")
    print(f"📍 Database: {DB_PATH}")
    print("🌐 API will be available at: http://127.0.0.1:8000")
    print("📖 API docs at: http://127.0.0.1:8000/docs")
    print("")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
