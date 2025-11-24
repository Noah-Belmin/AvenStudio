"""
Projects Module Handler
Manages project CRUD operations and project-level data
"""

from uuid import uuid4
from datetime import datetime


class ProjectsModule:
    def __init__(self):
        self.name = "projects"
        self.version = "1.0.0"

    def handle(self, request, data_layer):
        """Route project requests"""
        action = request.get('action')

        if action == 'list':
            return self._list_projects(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_project(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_project(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_project(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_project(request.get('id'), data_layer)
        elif action == 'get_stats':
            return self._get_project_stats(request.get('id'), data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _list_projects(self, filters, data_layer):
        """List all projects with optional filters"""
        try:
            projects = data_layer.query('projects', filters)
            return {'success': True, 'data': projects}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_project(self, project_id, data_layer):
        """Get single project by ID"""
        try:
            if not project_id:
                return {'success': False, 'error': 'Project ID required'}

            project = data_layer.get('projects', project_id)

            if not project:
                return {'success': False, 'error': 'Project not found'}

            return {'success': True, 'data': project}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_project(self, data, data_layer):
        """Create new project"""
        try:
            if not data.get('name'):
                return {'success': False, 'error': 'Project name required'}

            project_data = {
                'id': str(uuid4()),
                'name': data['name'],
                'location': data.get('location', ''),
                'project_type': data.get('project_type', 'self-build'),
                'start_date': data.get('start_date'),
                'target_completion': data.get('target_completion'),
                'status': data.get('status', 'planning'),
                'budget_total': data.get('budget_total', 0),
                'description': data.get('description', ''),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            project_id = data_layer.insert('projects', project_data)
            created_project = data_layer.get('projects', project_id)

            return {'success': True, 'data': created_project}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_project(self, project_id, data, data_layer):
        """Update existing project"""
        try:
            if not project_id:
                return {'success': False, 'error': 'Project ID required'}

            # Check project exists
            existing = data_layer.get('projects', project_id)
            if not existing:
                return {'success': False, 'error': 'Project not found'}

            # Update only provided fields
            update_data = {}
            allowed_fields = [
                'name', 'location', 'project_type', 'start_date',
                'target_completion', 'status', 'budget_total', 'description'
            ]

            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]

            if update_data:
                data_layer.update('projects', project_id, update_data)

            updated_project = data_layer.get('projects', project_id)
            return {'success': True, 'data': updated_project}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_project(self, project_id, data_layer):
        """Delete project (cascades to all related data)"""
        try:
            if not project_id:
                return {'success': False, 'error': 'Project ID required'}

            # Don't allow deleting default project
            if project_id == 'default-project':
                return {'success': False, 'error': 'Cannot delete default project'}

            success = data_layer.delete('projects', project_id)

            if not success:
                return {'success': False, 'error': 'Project not found'}

            return {'success': True, 'data': {'id': project_id}}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_project_stats(self, project_id, data_layer):
        """Get project statistics"""
        try:
            if not project_id:
                return {'success': False, 'error': 'Project ID required'}

            # Get project
            project = data_layer.get('projects', project_id)
            if not project:
                return {'success': False, 'error': 'Project not found'}

            # Get counts for related entities
            tasks = data_layer.query('tasks', {'project_id': project_id})
            budget_items = data_layer.query('budget_items', {'project_id': project_id})
            documents = data_layer.query('documents', {'project_id': project_id})
            contacts = data_layer.query('contacts', {'project_id': project_id})
            milestones = data_layer.query('milestones', {'project_id': project_id})
            materials = data_layer.query('materials', {'project_id': project_id})

            # Calculate task statistics
            task_stats = {
                'total': len(tasks),
                'by_status': {},
                'by_phase': {},
                'completion_rate': 0
            }

            for task in tasks:
                # Count by status
                status = task.get('status', 'todo')
                task_stats['by_status'][status] = task_stats['by_status'].get(status, 0) + 1

                # Count by phase
                phase = task.get('phase', 'unassigned')
                task_stats['by_phase'][phase] = task_stats['by_phase'].get(phase, 0) + 1

            # Calculate completion rate
            completed = task_stats['by_status'].get('done', 0)
            if task_stats['total'] > 0:
                task_stats['completion_rate'] = round((completed / task_stats['total']) * 100, 1)

            # Calculate budget statistics
            budget_stats = {
                'total_estimated': sum(item.get('estimated_cost', 0) for item in budget_items),
                'total_actual': sum(item.get('actual_cost', 0) for item in budget_items),
                'variance': 0,
                'items_count': len(budget_items)
            }
            budget_stats['variance'] = budget_stats['total_actual'] - budget_stats['total_estimated']

            # Milestone statistics
            milestone_stats = {
                'total': len(milestones),
                'by_status': {}
            }
            for milestone in milestones:
                status = milestone.get('status', 'pending')
                milestone_stats['by_status'][status] = milestone_stats['by_status'].get(status, 0) + 1

            stats = {
                'project': project,
                'tasks': task_stats,
                'budget': budget_stats,
                'documents_count': len(documents),
                'contacts_count': len(contacts),
                'milestones': milestone_stats,
                'materials_count': len(materials)
            }

            return {'success': True, 'data': stats}
        except Exception as e:
            return {'success': False, 'error': str(e)}
