"""
Categories Module
Manages task categories
"""

from typing import Dict, Any


class CategoriesModule:
    """Category management module"""

    def __init__(self):
        self.name = "categories"

    def handle(self, request: Dict[str, Any], data_layer) -> Dict[str, Any]:
        """Handle category requests"""
        action = request.get('action')

        if action == 'list':
            return self._list_categories(data_layer)
        elif action == 'create':
            return self._create_category(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_category(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_category(request.get('id'), data_layer)
        else:
            return {'success': False, 'error': f"Unknown action: {action}"}

    def _list_categories(self, data_layer) -> Dict[str, Any]:
        """List all categories"""
        try:
            categories = data_layer.fetchall("SELECT name FROM categories ORDER BY name")
            names = [cat['name'] for cat in categories]
            return {'success': True, 'data': names}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_category(self, data: Dict, data_layer) -> Dict[str, Any]:
        """Create new category"""
        try:
            name = data['name']

            # Check if exists
            existing = data_layer.fetchone("SELECT name FROM categories WHERE name = ?", (name,))
            if existing:
                return {'success': False, 'error': 'Category already exists'}

            # Insert
            data_layer.execute("INSERT INTO categories (name) VALUES (?)", (name,))

            return {'success': True, 'data': {'name': name}}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_category(self, old_name: str, data: Dict, data_layer) -> Dict[str, Any]:
        """Update category name"""
        try:
            new_name = data['name']

            # Update category
            data_layer.execute("UPDATE categories SET name = ? WHERE name = ?", (new_name, old_name))

            # Update tasks with this category
            data_layer.execute("UPDATE tasks SET category = ? WHERE category = ?", (new_name, old_name))

            return {'success': True, 'data': {'name': new_name}}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_category(self, name: str, data_layer) -> Dict[str, Any]:
        """Delete category"""
        try:
            # Don't allow deleting 'other'
            if name == 'other':
                return {'success': False, 'error': 'Cannot delete default category'}

            # Update tasks with this category to 'other'
            data_layer.execute("UPDATE tasks SET category = 'other' WHERE category = ?", (name,))

            # Delete category
            data_layer.execute("DELETE FROM categories WHERE name = ?", (name,))

            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
