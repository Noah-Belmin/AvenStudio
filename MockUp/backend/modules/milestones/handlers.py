"""
Milestones Module Handler
Manages project milestones, phase completion tracking, and dependencies
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List


class MilestonesModule:
    """Handler for milestone management operations"""

    def __init__(self):
        self.name = "milestones"
        self.version = "1.0.0"

    def handle(self, request: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Route milestone requests to appropriate handlers

        Args:
            request: Dictionary containing action and parameters
            data_layer: Database abstraction layer

        Returns:
            Dictionary with success status and data/error
        """
        action = request.get('action')

        if action == 'list':
            return self._list_milestones(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_milestone(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_milestone(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_milestone(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_milestone(request.get('id'), data_layer)
        elif action == 'get_by_phase':
            return self._get_by_phase(request.get('project_id'), request.get('phase'), data_layer)
        elif action == 'get_by_status':
            return self._get_by_status(request.get('project_id'), request.get('status'), data_layer)
        elif action == 'mark_complete':
            return self._mark_complete(request.get('id'), data_layer)
        elif action == 'get_timeline':
            return self._get_timeline(request.get('project_id'), data_layer)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    def _list_milestones(self, filters: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        List milestones with optional filtering

        Args:
            filters: Dictionary of filter criteria (project_id, phase, status)
            data_layer: Database layer

        Returns:
            List of milestones
        """
        try:
            all_milestones = data_layer.query('milestones', filters)

            # Sort by target date
            all_milestones.sort(key=lambda x: x.get('target_date', '9999-12-31'))

            return {
                'success': True,
                'data': all_milestones,
                'count': len(all_milestones)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_milestone(self, milestone_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get single milestone by ID"""
        try:
            if not milestone_id:
                return {'success': False, 'error': 'Milestone ID required'}

            milestone = data_layer.get('milestones', milestone_id)

            if not milestone:
                return {'success': False, 'error': 'Milestone not found'}

            return {'success': True, 'data': milestone}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_milestone(self, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Create new milestone

        Required fields: project_id, name
        Optional: phase, target_date, status, dependencies, notes
        """
        try:
            # Validate required fields
            required_fields = ['project_id', 'name']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'error': f'Missing required field: {field}'}

            # Generate ID and timestamps
            milestone = {
                'id': data.get('id', str(uuid.uuid4())),
                'project_id': data['project_id'],
                'name': data['name'],
                'phase': data.get('phase'),
                'target_date': data.get('target_date'),
                'actual_date': data.get('actual_date'),
                'status': data.get('status', 'pending'),
                'dependencies': data.get('dependencies', []),
                'notes': data.get('notes', ''),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.create('milestones', milestone)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_milestone(self, milestone_id: str, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """Update existing milestone"""
        try:
            if not milestone_id:
                return {'success': False, 'error': 'Milestone ID required'}

            # Check if milestone exists
            existing = data_layer.get('milestones', milestone_id)
            if not existing:
                return {'success': False, 'error': 'Milestone not found'}

            # Add updated timestamp
            data['updated_at'] = datetime.utcnow().isoformat()

            result = data_layer.update('milestones', milestone_id, data)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_milestone(self, milestone_id: str, data_layer: Any) -> Dict[str, Any]:
        """Delete milestone"""
        try:
            if not milestone_id:
                return {'success': False, 'error': 'Milestone ID required'}

            # Check if milestone exists
            existing = data_layer.get('milestones', milestone_id)
            if not existing:
                return {'success': False, 'error': 'Milestone not found'}

            data_layer.delete('milestones', milestone_id)

            return {
                'success': True,
                'message': f'Milestone {existing.get("name")} deleted'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_phase(self, project_id: str, phase: str, data_layer: Any) -> Dict[str, Any]:
        """Get all milestones for a specific build phase"""
        try:
            if not project_id or not phase:
                return {'success': False, 'error': 'project_id and phase required'}

            filters = {
                'project_id': project_id,
                'phase': phase
            }

            milestones = data_layer.query('milestones', filters)

            # Sort by target date
            milestones.sort(key=lambda x: x.get('target_date', '9999-12-31'))

            return {
                'success': True,
                'data': milestones,
                'count': len(milestones)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_status(self, project_id: str, status: str, data_layer: Any) -> Dict[str, Any]:
        """Get all milestones with a specific status"""
        try:
            if not project_id or not status:
                return {'success': False, 'error': 'project_id and status required'}

            filters = {
                'project_id': project_id,
                'status': status
            }

            milestones = data_layer.query('milestones', filters)

            # Sort by target date
            milestones.sort(key=lambda x: x.get('target_date', '9999-12-31'))

            return {
                'success': True,
                'data': milestones,
                'count': len(milestones)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _mark_complete(self, milestone_id: str, data_layer: Any) -> Dict[str, Any]:
        """Mark a milestone as completed with current date"""
        try:
            if not milestone_id:
                return {'success': False, 'error': 'Milestone ID required'}

            # Get current milestone
            milestone = data_layer.get('milestones', milestone_id)
            if not milestone:
                return {'success': False, 'error': 'Milestone not found'}

            # Update to completed status with actual date
            update_data = {
                'status': 'completed',
                'actual_date': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('milestones', milestone_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': f'Milestone "{milestone.get("name")}" marked as completed'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_timeline(self, project_id: str, data_layer: Any) -> Dict[str, Any]:
        """
        Get complete project timeline with all milestones
        Includes status breakdown and delay analysis
        """
        try:
            if not project_id:
                return {'success': False, 'error': 'project_id required'}

            # Get all milestones for project
            filters = {'project_id': project_id}
            milestones = data_layer.query('milestones', filters)

            # Sort by target date
            milestones.sort(key=lambda x: x.get('target_date', '9999-12-31'))

            # Calculate statistics
            now = datetime.utcnow().isoformat()

            status_counts = {
                'pending': 0,
                'in-progress': 0,
                'completed': 0,
                'delayed': 0,
                'cancelled': 0
            }

            delayed_milestones = []
            upcoming_milestones = []

            for milestone in milestones:
                status = milestone.get('status', 'pending')
                if status in status_counts:
                    status_counts[status] += 1

                # Check for delays
                target_date = milestone.get('target_date')
                if target_date and status not in ['completed', 'cancelled']:
                    if target_date < now:
                        delayed_milestones.append(milestone)
                    elif len(upcoming_milestones) < 5:  # Next 5 upcoming
                        upcoming_milestones.append(milestone)

            return {
                'success': True,
                'data': {
                    'milestones': milestones,
                    'total_count': len(milestones),
                    'status_breakdown': status_counts,
                    'delayed_count': len(delayed_milestones),
                    'delayed_milestones': delayed_milestones,
                    'upcoming_milestones': upcoming_milestones
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_info(self) -> Dict[str, Any]:
        """Return module information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Milestone tracking with phase linking and dependency management',
            'actions': [
                'list',
                'get',
                'create',
                'update',
                'delete',
                'get_by_phase',
                'get_by_status',
                'mark_complete',
                'get_timeline'
            ]
        }
