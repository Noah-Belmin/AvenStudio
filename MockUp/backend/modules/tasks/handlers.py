"""
Tasks Module
Handles all task-related operations
"""

from typing import Dict, Any
from datetime import datetime
from uuid import uuid4


class TasksModule:
    """Task management module"""

    def __init__(self):
        self.name = "tasks"
        self.version = "1.0.0"

    def handle(self, request: Dict[str, Any], data_layer) -> Dict[str, Any]:
        """Handle task requests"""
        action = request.get('action')

        if action == 'list':
            return self._list_tasks(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_task(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_task(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_task(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_task(request.get('id'), data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _list_tasks(self, filters: Dict, data_layer) -> Dict[str, Any]:
        """List tasks with optional filters"""
        try:
            tasks = data_layer.query('tasks', filters)
            return {'success': True, 'data': tasks}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_task(self, task_id: str, data_layer) -> Dict[str, Any]:
        """Get single task"""
        try:
            task = data_layer.get('tasks', task_id)
            if not task:
                return {'success': False, 'error': 'Task not found'}
            return {'success': True, 'data': task}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_task(self, data: Dict, data_layer) -> Dict[str, Any]:
        """Create new task"""
        try:
            # Generate ID and timestamps
            task_data = {
                'id': str(uuid4()),
                'title': data['title'],
                'description': data.get('description', ''),
                'status': 'todo',
                'priority': data.get('priority', 'medium'),
                'category': data['category'],
                'tags': data.get('tags', []),
                'due_date': data.get('dueDate'),
                'start_date': data.get('startDate'),
                'assigned_to': data.get('assignedTo'),
                'estimated_hours': data.get('estimatedHours'),
                'completion_percentage': data.get('completionPercentage', 0),
                'blocked_by': data.get('blockedBy', []),
                'comments': [],
                'attachments': [],
                'checklist': [],
                'subtasks': [],
                'custom_fields': {},
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            task_id = data_layer.insert('tasks', task_data)
            created_task = data_layer.get('tasks', task_id)

            return {'success': True, 'data': created_task}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_task(self, task_id: str, data: Dict, data_layer) -> Dict[str, Any]:
        """Update task"""
        try:
            # Check if task exists
            existing = data_layer.get('tasks', task_id)
            if not existing:
                return {'success': False, 'error': 'Task not found'}

            # Update task
            success = data_layer.update('tasks', task_id, data)
            if not success:
                return {'success': False, 'error': 'Update failed'}

            # Return updated task
            updated_task = data_layer.get('tasks', task_id)
            return {'success': True, 'data': updated_task}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_task(self, task_id: str, data_layer) -> Dict[str, Any]:
        """Delete task"""
        try:
            success = data_layer.delete('tasks', task_id)
            if not success:
                return {'success': False, 'error': 'Task not found'}
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
