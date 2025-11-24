"""
Materials Module Handler
Manages materials procurement, delivery tracking, and supplier coordination
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List


class MaterialsModule:
    """Handler for materials management operations"""

    def __init__(self):
        self.name = "materials"
        self.version = "1.0.0"

    def handle(self, request: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Route materials requests to appropriate handlers

        Args:
            request: Dictionary containing action and parameters
            data_layer: Database abstraction layer

        Returns:
            Dictionary with success status and data/error
        """
        action = request.get('action')

        if action == 'list':
            return self._list_materials(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_material(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_material(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_material(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_material(request.get('id'), data_layer)
        elif action == 'get_by_status':
            return self._get_by_status(request.get('project_id'), request.get('delivery_status'), data_layer)
        elif action == 'get_by_supplier':
            return self._get_by_supplier(request.get('project_id'), request.get('supplier_id'), data_layer)
        elif action == 'mark_delivered':
            return self._mark_delivered(request.get('id'), data_layer)
        elif action == 'get_overdue':
            return self._get_overdue(request.get('project_id'), data_layer)
        elif action == 'get_summary':
            return self._get_summary(request.get('project_id'), data_layer)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    def _list_materials(self, filters: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        List materials with optional filtering

        Args:
            filters: Dictionary of filter criteria (project_id, delivery_status, supplier_id)
            data_layer: Database layer

        Returns:
            List of materials
        """
        try:
            all_materials = data_layer.query('materials', filters)

            # Sort by delivery date (earliest first)
            all_materials.sort(key=lambda x: x.get('delivery_date', '9999-12-31'))

            return {
                'success': True,
                'data': all_materials,
                'count': len(all_materials)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_material(self, material_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get single material by ID"""
        try:
            if not material_id:
                return {'success': False, 'error': 'Material ID required'}

            material = data_layer.get('materials', material_id)

            if not material:
                return {'success': False, 'error': 'Material not found'}

            return {'success': True, 'data': material}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_material(self, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Create new material record

        Required fields: project_id, item_name
        Optional: quantity, unit, supplier_id, cost, lead_time_days, delivery_date,
                 delivery_status, warranty_info, notes
        """
        try:
            # Validate required fields
            required_fields = ['project_id', 'item_name']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'error': f'Missing required field: {field}'}

            # Generate ID and timestamps
            material = {
                'id': data.get('id', str(uuid.uuid4())),
                'project_id': data['project_id'],
                'item_name': data['item_name'],
                'quantity': data.get('quantity'),
                'unit': data.get('unit', 'units'),
                'supplier_id': data.get('supplier_id'),
                'cost': data.get('cost', 0),
                'lead_time_days': data.get('lead_time_days', 0),
                'delivery_date': data.get('delivery_date'),
                'delivery_status': data.get('delivery_status', 'not-ordered'),
                'warranty_info': data.get('warranty_info', ''),
                'notes': data.get('notes', ''),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.create('materials', material)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_material(self, material_id: str, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """Update existing material"""
        try:
            if not material_id:
                return {'success': False, 'error': 'Material ID required'}

            # Check if material exists
            existing = data_layer.get('materials', material_id)
            if not existing:
                return {'success': False, 'error': 'Material not found'}

            # Add updated timestamp
            data['updated_at'] = datetime.utcnow().isoformat()

            result = data_layer.update('materials', material_id, data)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_material(self, material_id: str, data_layer: Any) -> Dict[str, Any]:
        """Delete material record"""
        try:
            if not material_id:
                return {'success': False, 'error': 'Material ID required'}

            # Check if material exists
            existing = data_layer.get('materials', material_id)
            if not existing:
                return {'success': False, 'error': 'Material not found'}

            data_layer.delete('materials', material_id)

            return {
                'success': True,
                'message': f'Material {existing.get("item_name")} deleted'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_status(self, project_id: str, delivery_status: str, data_layer: Any) -> Dict[str, Any]:
        """Get all materials with a specific delivery status"""
        try:
            if not project_id or not delivery_status:
                return {'success': False, 'error': 'project_id and delivery_status required'}

            filters = {
                'project_id': project_id,
                'delivery_status': delivery_status
            }

            materials = data_layer.query('materials', filters)

            # Sort by delivery date
            materials.sort(key=lambda x: x.get('delivery_date', '9999-12-31'))

            return {
                'success': True,
                'data': materials,
                'count': len(materials)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_supplier(self, project_id: str, supplier_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get all materials from a specific supplier"""
        try:
            if not project_id or not supplier_id:
                return {'success': False, 'error': 'project_id and supplier_id required'}

            filters = {
                'project_id': project_id,
                'supplier_id': supplier_id
            }

            materials = data_layer.query('materials', filters)

            # Calculate total cost from this supplier
            total_cost = sum(m.get('cost', 0) for m in materials)

            return {
                'success': True,
                'data': materials,
                'count': len(materials),
                'total_cost': total_cost
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _mark_delivered(self, material_id: str, data_layer: Any) -> Dict[str, Any]:
        """Mark a material as delivered"""
        try:
            if not material_id:
                return {'success': False, 'error': 'Material ID required'}

            # Get current material
            material = data_layer.get('materials', material_id)
            if not material:
                return {'success': False, 'error': 'Material not found'}

            # Update to delivered status
            update_data = {
                'delivery_status': 'delivered',
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('materials', material_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': f'Material "{material.get("item_name")}" marked as delivered'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_overdue(self, project_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get all materials that are overdue for delivery"""
        try:
            if not project_id:
                return {'success': False, 'error': 'project_id required'}

            # Get all materials for project
            filters = {'project_id': project_id}
            all_materials = data_layer.query('materials', filters)

            # Filter for overdue items
            now = datetime.utcnow().isoformat()
            overdue_materials = []

            for material in all_materials:
                delivery_status = material.get('delivery_status', 'not-ordered')
                delivery_date = material.get('delivery_date')

                # Material is overdue if:
                # - Has delivery date
                # - Delivery date is in the past
                # - Status is not 'delivered' or 'not-ordered'
                if delivery_date and delivery_date < now:
                    if delivery_status not in ['delivered', 'not-ordered']:
                        overdue_materials.append(material)

            # Sort by how overdue (oldest first)
            overdue_materials.sort(key=lambda x: x.get('delivery_date', ''))

            return {
                'success': True,
                'data': overdue_materials,
                'count': len(overdue_materials)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_summary(self, project_id: str, data_layer: Any) -> Dict[str, Any]:
        """
        Get materials summary for a project
        Includes status breakdown and cost totals
        """
        try:
            if not project_id:
                return {'success': False, 'error': 'project_id required'}

            # Get all materials for project
            filters = {'project_id': project_id}
            materials = data_layer.query('materials', filters)

            # Calculate statistics
            summary = {
                'total_items': len(materials),
                'total_cost': 0,
                'by_status': {
                    'not-ordered': 0,
                    'ordered': 0,
                    'in-transit': 0,
                    'delivered': 0,
                    'overdue': 0
                },
                'by_supplier': {},
                'overdue_count': 0
            }

            now = datetime.utcnow().isoformat()

            for material in materials:
                # Count by status
                status = material.get('delivery_status', 'not-ordered')
                if status in summary['by_status']:
                    summary['by_status'][status] += 1

                # Sum costs
                summary['total_cost'] += material.get('cost', 0)

                # Count by supplier
                supplier_id = material.get('supplier_id')
                if supplier_id:
                    if supplier_id not in summary['by_supplier']:
                        summary['by_supplier'][supplier_id] = {
                            'count': 0,
                            'total_cost': 0
                        }
                    summary['by_supplier'][supplier_id]['count'] += 1
                    summary['by_supplier'][supplier_id]['total_cost'] += material.get('cost', 0)

                # Check for overdue
                delivery_date = material.get('delivery_date')
                if delivery_date and delivery_date < now:
                    if status not in ['delivered', 'not-ordered']:
                        summary['overdue_count'] += 1

            return {
                'success': True,
                'data': summary
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_info(self) -> Dict[str, Any]:
        """Return module information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Materials procurement and delivery tracking with supplier coordination',
            'actions': [
                'list',
                'get',
                'create',
                'update',
                'delete',
                'get_by_status',
                'get_by_supplier',
                'mark_delivered',
                'get_overdue',
                'get_summary'
            ]
        }
