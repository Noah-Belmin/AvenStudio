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


class ProjectCreate(BaseModel):
    name: str
    location: Optional[str] = None
    project_type: str = 'self-build'
    start_date: Optional[str] = None
    target_completion: Optional[str] = None
    budget_total: Optional[float] = None
    description: str = ""


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    project_type: Optional[str] = None
    start_date: Optional[str] = None
    target_completion: Optional[str] = None
    status: Optional[str] = None
    budget_total: Optional[float] = None
    description: Optional[str] = None


class BudgetItemCreate(BaseModel):
    project_id: str
    category: str
    item_name: str
    estimated_cost: float = 0
    actual_cost: float = 0
    supplier: Optional[str] = None
    quote_date: Optional[str] = None
    status: str = 'estimated'
    notes: str = ""


class BudgetItemUpdate(BaseModel):
    category: Optional[str] = None
    item_name: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    supplier: Optional[str] = None
    quote_date: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class DocumentCreate(BaseModel):
    project_id: str
    filename: str
    file_path: str
    document_type: str = 'other'
    linked_task_id: Optional[str] = None
    linked_phase: Optional[str] = None
    tags: List[str] = []
    notes: str = ""


class DocumentUpdate(BaseModel):
    filename: Optional[str] = None
    document_type: Optional[str] = None
    linked_task_id: Optional[str] = None
    linked_phase: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class ContactCreate(BaseModel):
    project_id: str
    name: str
    role: str = 'other'
    company: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    performance_rating: Optional[int] = None


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    performance_rating: Optional[int] = None


class MilestoneCreate(BaseModel):
    project_id: str
    name: str
    phase: Optional[str] = None
    target_date: Optional[str] = None
    status: str = 'pending'
    dependencies: List[str] = []
    notes: str = ""


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    phase: Optional[str] = None
    target_date: Optional[str] = None
    actual_date: Optional[str] = None
    status: Optional[str] = None
    dependencies: Optional[List[str]] = None
    notes: Optional[str] = None


class MaterialCreate(BaseModel):
    project_id: str
    item_name: str
    quantity: Optional[float] = None
    unit: str = 'units'
    supplier_id: Optional[str] = None
    cost: float = 0
    lead_time_days: int = 0
    delivery_date: Optional[str] = None
    delivery_status: str = 'not-ordered'
    warranty_info: str = ""
    notes: str = ""


class MaterialUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    supplier_id: Optional[str] = None
    cost: Optional[float] = None
    lead_time_days: Optional[int] = None
    delivery_date: Optional[str] = None
    delivery_status: Optional[str] = None
    warranty_info: Optional[str] = None
    notes: Optional[str] = None


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
# Projects Endpoints
# ============================================================================

@app.get("/api/projects")
def list_projects(status: Optional[str] = None):
    """List all projects with optional filters"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'list',
            'filters': {'status': status} if status else {}
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    """Get single project by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'get',
            'id': project_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Project not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects")
def create_project(project: ProjectCreate):
    """Create new project"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'create',
            'data': project.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/projects/{project_id}")
def update_project(project_id: str, project: ProjectUpdate):
    """Update existing project"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'update',
            'id': project_id,
            'data': project.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Project not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str):
    """Delete project"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'delete',
            'id': project_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Project not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/stats")
def get_project_stats(project_id: str):
    """Get project statistics"""
    try:
        response = orchestrator.handle_request({
            'module': 'projects',
            'action': 'get_stats',
            'id': project_id
        })
        return response.get('data', {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Budget Endpoints
# ============================================================================

@app.get("/api/budget")
def list_budget_items(project_id: str, category: Optional[str] = None, status: Optional[str] = None):
    """List budget items with optional filters"""
    try:
        filters = {'project_id': project_id}
        if category:
            filters['category'] = category
        if status:
            filters['status'] = status

        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'list',
            'filters': filters
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/budget/{item_id}")
def get_budget_item(item_id: str):
    """Get single budget item by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'get',
            'id': item_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Budget item not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/budget")
def create_budget_item(item: BudgetItemCreate):
    """Create new budget item"""
    try:
        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'create',
            'data': item.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/budget/{item_id}")
def update_budget_item(item_id: str, item: BudgetItemUpdate):
    """Update existing budget item"""
    try:
        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'update',
            'id': item_id,
            'data': item.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Budget item not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/budget/{item_id}")
def delete_budget_item(item_id: str):
    """Delete budget item"""
    try:
        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'delete',
            'id': item_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Budget item not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/budget/summary/{project_id}")
def get_budget_summary(project_id: str):
    """Get budget summary for a project"""
    try:
        response = orchestrator.handle_request({
            'module': 'budget',
            'action': 'get_summary',
            'project_id': project_id
        })
        return response.get('data', {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Documents Endpoints
# ============================================================================

@app.get("/api/documents")
def list_documents(project_id: str, document_type: Optional[str] = None):
    """List documents with optional filters"""
    try:
        filters = {'project_id': project_id}
        if document_type:
            filters['document_type'] = document_type

        response = orchestrator.handle_request({
            'module': 'documents',
            'action': 'list',
            'filters': filters
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/{document_id}")
def get_document(document_id: str):
    """Get single document by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'documents',
            'action': 'get',
            'id': document_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Document not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents")
def create_document(doc: DocumentCreate):
    """Create new document record"""
    try:
        response = orchestrator.handle_request({
            'module': 'documents',
            'action': 'create',
            'data': doc.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/documents/{document_id}")
def update_document(document_id: str, doc: DocumentUpdate):
    """Update existing document"""
    try:
        response = orchestrator.handle_request({
            'module': 'documents',
            'action': 'update',
            'id': document_id,
            'data': doc.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Document not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/documents/{document_id}")
def delete_document(document_id: str):
    """Delete document record"""
    try:
        response = orchestrator.handle_request({
            'module': 'documents',
            'action': 'delete',
            'id': document_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Document not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Contacts Endpoints
# ============================================================================

@app.get("/api/contacts")
def list_contacts(project_id: str, role: Optional[str] = None):
    """List contacts with optional filters"""
    try:
        filters = {'project_id': project_id}
        if role:
            filters['role'] = role

        response = orchestrator.handle_request({
            'module': 'contacts',
            'action': 'list',
            'filters': filters
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: str):
    """Get single contact by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'contacts',
            'action': 'get',
            'id': contact_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Contact not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/contacts")
def create_contact(contact: ContactCreate):
    """Create new contact"""
    try:
        response = orchestrator.handle_request({
            'module': 'contacts',
            'action': 'create',
            'data': contact.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/contacts/{contact_id}")
def update_contact(contact_id: str, contact: ContactUpdate):
    """Update existing contact"""
    try:
        response = orchestrator.handle_request({
            'module': 'contacts',
            'action': 'update',
            'id': contact_id,
            'data': contact.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Contact not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/contacts/{contact_id}")
def delete_contact(contact_id: str):
    """Delete contact"""
    try:
        response = orchestrator.handle_request({
            'module': 'contacts',
            'action': 'delete',
            'id': contact_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Contact not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Milestones Endpoints
# ============================================================================

@app.get("/api/milestones")
def list_milestones(project_id: str, phase: Optional[str] = None, status: Optional[str] = None):
    """List milestones with optional filters"""
    try:
        filters = {'project_id': project_id}
        if phase:
            filters['phase'] = phase
        if status:
            filters['status'] = status

        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'list',
            'filters': filters
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/milestones/{milestone_id}")
def get_milestone(milestone_id: str):
    """Get single milestone by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'get',
            'id': milestone_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Milestone not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/milestones")
def create_milestone(milestone: MilestoneCreate):
    """Create new milestone"""
    try:
        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'create',
            'data': milestone.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/milestones/{milestone_id}")
def update_milestone(milestone_id: str, milestone: MilestoneUpdate):
    """Update existing milestone"""
    try:
        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'update',
            'id': milestone_id,
            'data': milestone.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Milestone not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/milestones/{milestone_id}")
def delete_milestone(milestone_id: str):
    """Delete milestone"""
    try:
        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'delete',
            'id': milestone_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Milestone not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/milestones/timeline/{project_id}")
def get_milestones_timeline(project_id: str):
    """Get complete milestone timeline for a project"""
    try:
        response = orchestrator.handle_request({
            'module': 'milestones',
            'action': 'get_timeline',
            'project_id': project_id
        })
        return response.get('data', {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Materials Endpoints
# ============================================================================

@app.get("/api/materials")
def list_materials(project_id: str, delivery_status: Optional[str] = None):
    """List materials with optional filters"""
    try:
        filters = {'project_id': project_id}
        if delivery_status:
            filters['delivery_status'] = delivery_status

        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'list',
            'filters': filters
        })
        return response.get('data', [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials/{material_id}")
def get_material(material_id: str):
    """Get single material by ID"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'get',
            'id': material_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Material not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/materials")
def create_material(material: MaterialCreate):
    """Create new material"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'create',
            'data': material.dict()
        })
        if not response.get('success'):
            raise HTTPException(status_code=400, detail=response.get('error'))
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/materials/{material_id}")
def update_material(material_id: str, material: MaterialUpdate):
    """Update existing material"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'update',
            'id': material_id,
            'data': material.dict(exclude_unset=True)
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Material not found")
        return response.get('data')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/materials/{material_id}")
def delete_material(material_id: str):
    """Delete material"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'delete',
            'id': material_id
        })
        if not response.get('success'):
            raise HTTPException(status_code=404, detail="Material not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials/summary/{project_id}")
def get_materials_summary(project_id: str):
    """Get materials summary for a project"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'get_summary',
            'project_id': project_id
        })
        return response.get('data', {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/materials/overdue/{project_id}")
def get_overdue_materials(project_id: str):
    """Get overdue materials for a project"""
    try:
        response = orchestrator.handle_request({
            'module': 'materials',
            'action': 'get_overdue',
            'project_id': project_id
        })
        return response.get('data', [])
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
