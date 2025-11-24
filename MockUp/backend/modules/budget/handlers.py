"""
Budget Module Handler
Manages budget items, spending tracking, and financial reporting
"""

from uuid import uuid4
from datetime import datetime


class BudgetModule:
    def __init__(self):
        self.name = "budget"
        self.version = "1.0.0"

    def handle(self, request, data_layer):
        """Route budget requests"""
        action = request.get('action')

        if action == 'list':
            return self._list_budget_items(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_budget_item(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_budget_item(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_budget_item(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_budget_item(request.get('id'), data_layer)
        elif action == 'get_summary':
            return self._get_budget_summary(request.get('project_id'), data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _list_budget_items(self, filters, data_layer):
        """List budget items with optional filters"""
        try:
            items = data_layer.query('budget_items', filters)

            # Add calculated variance to each item
            for item in items:
                item['variance'] = item.get('actual_cost', 0) - item.get('estimated_cost', 0)

            return {'success': True, 'data': items}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_budget_item(self, item_id, data_layer):
        """Get single budget item"""
        try:
            if not item_id:
                return {'success': False, 'error': 'Budget item ID required'}

            item = data_layer.get('budget_items', item_id)

            if not item:
                return {'success': False, 'error': 'Budget item not found'}

            # Add calculated variance
            item['variance'] = item.get('actual_cost', 0) - item.get('estimated_cost', 0)

            return {'success': True, 'data': item}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_budget_item(self, data, data_layer):
        """Create new budget item"""
        try:
            if not data.get('project_id'):
                return {'success': False, 'error': 'Project ID required'}

            if not data.get('item_name'):
                return {'success': False, 'error': 'Item name required'}

            item_data = {
                'id': str(uuid4()),
                'project_id': data['project_id'],
                'category': data.get('category', 'other'),
                'item_name': data['item_name'],
                'estimated_cost': float(data.get('estimated_cost', 0)),
                'actual_cost': float(data.get('actual_cost', 0)),
                'supplier': data.get('supplier', ''),
                'quote_date': data.get('quote_date'),
                'status': data.get('status', 'estimated'),
                'notes': data.get('notes', ''),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            item_id = data_layer.insert('budget_items', item_data)
            created_item = data_layer.get('budget_items', item_id)

            # Add variance
            created_item['variance'] = created_item.get('actual_cost', 0) - created_item.get('estimated_cost', 0)

            return {'success': True, 'data': created_item}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_budget_item(self, item_id, data, data_layer):
        """Update budget item"""
        try:
            if not item_id:
                return {'success': False, 'error': 'Budget item ID required'}

            existing = data_layer.get('budget_items', item_id)
            if not existing:
                return {'success': False, 'error': 'Budget item not found'}

            update_data = {}
            allowed_fields = [
                'category', 'item_name', 'estimated_cost', 'actual_cost',
                'supplier', 'quote_date', 'status', 'notes'
            ]

            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]

            if update_data:
                data_layer.update('budget_items', item_id, update_data)

            updated_item = data_layer.get('budget_items', item_id)
            updated_item['variance'] = updated_item.get('actual_cost', 0) - updated_item.get('estimated_cost', 0)

            return {'success': True, 'data': updated_item}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_budget_item(self, item_id, data_layer):
        """Delete budget item"""
        try:
            if not item_id:
                return {'success': False, 'error': 'Budget item ID required'}

            success = data_layer.delete('budget_items', item_id)

            if not success:
                return {'success': False, 'error': 'Budget item not found'}

            return {'success': True, 'data': {'id': item_id}}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_budget_summary(self, project_id, data_layer):
        """Get budget summary for a project"""
        try:
            if not project_id:
                return {'success': False, 'error': 'Project ID required'}

            items = data_layer.query('budget_items', {'project_id': project_id})

            summary = {
                'total_estimated': 0,
                'total_actual': 0,
                'total_variance': 0,
                'by_category': {},
                'by_status': {},
                'items_count': len(items)
            }

            for item in items:
                estimated = item.get('estimated_cost', 0)
                actual = item.get('actual_cost', 0)
                category = item.get('category', 'other')
                status = item.get('status', 'estimated')

                # Overall totals
                summary['total_estimated'] += estimated
                summary['total_actual'] += actual

                # By category
                if category not in summary['by_category']:
                    summary['by_category'][category] = {
                        'estimated': 0,
                        'actual': 0,
                        'variance': 0,
                        'count': 0
                    }

                summary['by_category'][category]['estimated'] += estimated
                summary['by_category'][category]['actual'] += actual
                summary['by_category'][category]['variance'] += (actual - estimated)
                summary['by_category'][category]['count'] += 1

                # By status
                summary['by_status'][status] = summary['by_status'].get(status, 0) + 1

            summary['total_variance'] = summary['total_actual'] - summary['total_estimated']

            # Add percentage calculations
            if summary['total_estimated'] > 0:
                summary['variance_percentage'] = round(
                    (summary['total_variance'] / summary['total_estimated']) * 100, 1
                )
                summary['spent_percentage'] = round(
                    (summary['total_actual'] / summary['total_estimated']) * 100, 1
                )
            else:
                summary['variance_percentage'] = 0
                summary['spent_percentage'] = 0

            return {'success': True, 'data': summary}
        except Exception as e:
            return {'success': False, 'error': str(e)}
