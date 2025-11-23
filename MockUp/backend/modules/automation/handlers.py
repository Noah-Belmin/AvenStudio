"""
Automation Module
Manages automation rules
"""

from typing import Dict, Any
from uuid import uuid4
from datetime import datetime


class AutomationModule:
    """Automation rules module"""

    def __init__(self):
        self.name = "automation"

    def handle(self, request: Dict[str, Any], data_layer) -> Dict[str, Any]:
        """Handle automation requests"""
        action = request.get('action')

        if action == 'list_rules':
            return self._list_rules(data_layer)
        elif action == 'create_rule':
            return self._create_rule(request.get('data'), data_layer)
        elif action == 'execute':
            return self._execute(request.get('data'), data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _list_rules(self, data_layer) -> Dict[str, Any]:
        """List all automation rules"""
        try:
            rules = data_layer.query('automation_rules')
            return {'success': True, 'data': rules}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_rule(self, data: Dict, data_layer) -> Dict[str, Any]:
        """Create automation rule"""
        try:
            rule_data = {
                'id': str(uuid4()),
                'name': data['name'],
                'description': data.get('description', ''),
                'enabled': data.get('enabled', True),
                'trigger': data['trigger'],
                'conditions': data.get('conditions', []),
                'actions': data.get('actions', []),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'trigger_count': 0
            }

            rule_id = data_layer.insert('automation_rules', rule_data)
            created_rule = data_layer.get('automation_rules', rule_id)

            return {'success': True, 'data': created_rule}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _execute(self, data: Dict, data_layer) -> Dict[str, Any]:
        """Execute automation rules for a task"""
        try:
            task_id = data['taskId']
            trigger = data['trigger']

            # Get task
            task = data_layer.get('tasks', task_id)
            if not task:
                return {'success': False, 'error': 'Task not found'}

            # Get enabled rules for this trigger
            rules = data_layer.fetchall(
                "SELECT * FROM automation_rules WHERE enabled = 1 AND trigger = ?",
                (trigger,)
            )

            triggered = []

            for rule in rules:
                # Check conditions (simplified - just execute all for now)
                # In real implementation, would evaluate conditions against task

                # Execute actions (simplified)
                triggered.append(rule['id'])

                # Increment trigger count
                data_layer.execute(
                    "UPDATE automation_rules SET trigger_count = trigger_count + 1, last_triggered = ? WHERE id = ?",
                    (datetime.utcnow().isoformat(), rule['id'])
                )

            return {'success': True, 'data': triggered}
        except Exception as e:
            return {'success': False, 'error': str(e)}
