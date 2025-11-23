"""
Stats Module
Provides dashboard statistics
"""

from typing import Dict, Any
from datetime import datetime, timedelta


class StatsModule:
    """Statistics module for dashboard"""

    def __init__(self):
        self.name = "stats"

    def handle(self, request: Dict[str, Any], data_layer) -> Dict[str, Any]:
        """Handle stats requests"""
        action = request.get('action')

        if action == 'get_dashboard_stats':
            return self._get_dashboard_stats(data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _get_dashboard_stats(self, data_layer) -> Dict[str, Any]:
        """Calculate dashboard statistics"""
        try:
            tasks = data_layer.query('tasks')

            # Count by status
            total = len(tasks)
            in_progress = len([t for t in tasks if t['status'] == 'in-progress'])
            completed = len([t for t in tasks if t['status'] == 'done'])
            blocked = len([t for t in tasks if t['status'] == 'blocked'])

            # Completion rate
            completion_rate = round((completed / total * 100)) if total > 0 else 0

            # Count by priority
            by_priority = {}
            for task in tasks:
                priority = task['priority']
                by_priority[priority] = by_priority.get(priority, 0) + 1

            # Count by category
            by_category = {}
            for task in tasks:
                category = task['category']
                by_category[category] = by_category.get(category, 0) + 1

            # Due dates
            now = datetime.utcnow()
            week_later = now + timedelta(days=7)

            overdue = 0
            due_soon = 0

            for task in tasks:
                if task['status'] == 'done' or not task.get('due_date'):
                    continue

                try:
                    due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                    if due_date < now:
                        overdue += 1
                    elif due_date <= week_later:
                        due_soon += 1
                except:
                    pass

            stats = {
                'total_tasks': total,
                'in_progress': in_progress,
                'completed': completed,
                'blocked': blocked,
                'completion_rate': completion_rate,
                'by_priority': by_priority,
                'by_category': by_category,
                'overdue': overdue,
                'due_soon': due_soon
            }

            return {'success': True, 'data': stats}
        except Exception as e:
            return {'success': False, 'error': str(e)}
