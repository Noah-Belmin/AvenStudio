"""
Documents Module Handler
Manages project documents, drawings, certificates, and file versioning
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List


class DocumentsModule:
    """Handler for document management operations"""

    def __init__(self):
        self.name = "documents"
        self.version = "1.0.0"

    def handle(self, request: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Route document requests to appropriate handlers

        Args:
            request: Dictionary containing action and parameters
            data_layer: Database abstraction layer

        Returns:
            Dictionary with success status and data/error
        """
        action = request.get('action')

        if action == 'list':
            return self._list_documents(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_document(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_document(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_document(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_document(request.get('id'), data_layer)
        elif action == 'get_by_type':
            return self._get_by_type(request.get('project_id'), request.get('document_type'), data_layer)
        elif action == 'get_by_phase':
            return self._get_by_phase(request.get('project_id'), request.get('phase'), data_layer)
        elif action == 'increment_version':
            return self._increment_version(request.get('id'), data_layer)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    def _list_documents(self, filters: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        List documents with optional filtering

        Args:
            filters: Dictionary of filter criteria (project_id, document_type, linked_task_id)
            data_layer: Database layer

        Returns:
            List of documents
        """
        try:
            all_documents = data_layer.query('documents', filters)

            # Sort by upload date (newest first)
            all_documents.sort(key=lambda x: x.get('upload_date', ''), reverse=True)

            return {
                'success': True,
                'data': all_documents,
                'count': len(all_documents)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_document(self, document_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get single document by ID"""
        try:
            if not document_id:
                return {'success': False, 'error': 'Document ID required'}

            document = data_layer.get('documents', document_id)

            if not document:
                return {'success': False, 'error': 'Document not found'}

            return {'success': True, 'data': document}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_document(self, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Create new document record

        Required fields: project_id, filename, file_path
        Optional: document_type, linked_task_id, linked_phase, tags, notes
        """
        try:
            # Validate required fields
            required_fields = ['project_id', 'filename', 'file_path']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'error': f'Missing required field: {field}'}

            # Generate ID and timestamps
            document = {
                'id': data.get('id', str(uuid.uuid4())),
                'project_id': data['project_id'],
                'filename': data['filename'],
                'file_path': data['file_path'],
                'document_type': data.get('document_type', 'other'),
                'version': data.get('version', 1),
                'linked_task_id': data.get('linked_task_id'),
                'linked_phase': data.get('linked_phase'),
                'tags': data.get('tags', []),
                'notes': data.get('notes', ''),
                'upload_date': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.create('documents', document)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_document(self, document_id: str, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """Update existing document"""
        try:
            if not document_id:
                return {'success': False, 'error': 'Document ID required'}

            # Check if document exists
            existing = data_layer.get('documents', document_id)
            if not existing:
                return {'success': False, 'error': 'Document not found'}

            # Add updated timestamp
            data['updated_at'] = datetime.utcnow().isoformat()

            result = data_layer.update('documents', document_id, data)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_document(self, document_id: str, data_layer: Any) -> Dict[str, Any]:
        """Delete document record (Note: actual file deletion should be handled separately)"""
        try:
            if not document_id:
                return {'success': False, 'error': 'Document ID required'}

            # Check if document exists
            existing = data_layer.get('documents', document_id)
            if not existing:
                return {'success': False, 'error': 'Document not found'}

            data_layer.delete('documents', document_id)

            return {
                'success': True,
                'message': f'Document {document_id} deleted',
                'file_path': existing.get('file_path')  # Return path for actual file deletion
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_type(self, project_id: str, document_type: str, data_layer: Any) -> Dict[str, Any]:
        """Get all documents of a specific type for a project"""
        try:
            if not project_id or not document_type:
                return {'success': False, 'error': 'project_id and document_type required'}

            filters = {
                'project_id': project_id,
                'document_type': document_type
            }

            documents = data_layer.query('documents', filters)

            # Sort by version (highest first)
            documents.sort(key=lambda x: x.get('version', 0), reverse=True)

            return {
                'success': True,
                'data': documents,
                'count': len(documents)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_phase(self, project_id: str, phase: str, data_layer: Any) -> Dict[str, Any]:
        """Get all documents linked to a specific build phase"""
        try:
            if not project_id or not phase:
                return {'success': False, 'error': 'project_id and phase required'}

            filters = {
                'project_id': project_id,
                'linked_phase': phase
            }

            documents = data_layer.query('documents', filters)

            return {
                'success': True,
                'data': documents,
                'count': len(documents)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _increment_version(self, document_id: str, data_layer: Any) -> Dict[str, Any]:
        """Increment document version number"""
        try:
            if not document_id:
                return {'success': False, 'error': 'Document ID required'}

            # Get current document
            document = data_layer.get('documents', document_id)
            if not document:
                return {'success': False, 'error': 'Document not found'}

            # Increment version
            current_version = document.get('version', 1)
            new_version = current_version + 1

            update_data = {
                'version': new_version,
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('documents', document_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': f'Version incremented to {new_version}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_info(self) -> Dict[str, Any]:
        """Return module information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Document management with versioning and phase linking',
            'actions': [
                'list',
                'get',
                'create',
                'update',
                'delete',
                'get_by_type',
                'get_by_phase',
                'increment_version'
            ]
        }
