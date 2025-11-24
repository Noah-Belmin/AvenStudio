"""
Contacts Module Handler
Manages project contacts including architects, engineers, contractors, suppliers
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List


class ContactsModule:
    """Handler for contact management operations"""

    def __init__(self):
        self.name = "contacts"
        self.version = "1.0.0"

    def handle(self, request: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Route contact requests to appropriate handlers

        Args:
            request: Dictionary containing action and parameters
            data_layer: Database abstraction layer

        Returns:
            Dictionary with success status and data/error
        """
        action = request.get('action')

        if action == 'list':
            return self._list_contacts(request.get('filters', {}), data_layer)
        elif action == 'get':
            return self._get_contact(request.get('id'), data_layer)
        elif action == 'create':
            return self._create_contact(request.get('data'), data_layer)
        elif action == 'update':
            return self._update_contact(request.get('id'), request.get('data'), data_layer)
        elif action == 'delete':
            return self._delete_contact(request.get('id'), data_layer)
        elif action == 'get_by_role':
            return self._get_by_role(request.get('project_id'), request.get('role'), data_layer)
        elif action == 'add_note':
            return self._add_note(request.get('id'), request.get('note'), data_layer)
        elif action == 'add_contract':
            return self._add_contract(request.get('id'), request.get('contract'), data_layer)
        elif action == 'rate_contact':
            return self._rate_contact(request.get('id'), request.get('rating'), data_layer)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}

    def _list_contacts(self, filters: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        List contacts with optional filtering

        Args:
            filters: Dictionary of filter criteria (project_id, role)
            data_layer: Database layer

        Returns:
            List of contacts
        """
        try:
            all_contacts = data_layer.query('contacts', filters)

            # Sort by name
            all_contacts.sort(key=lambda x: x.get('name', '').lower())

            return {
                'success': True,
                'data': all_contacts,
                'count': len(all_contacts)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_contact(self, contact_id: str, data_layer: Any) -> Dict[str, Any]:
        """Get single contact by ID"""
        try:
            if not contact_id:
                return {'success': False, 'error': 'Contact ID required'}

            contact = data_layer.get('contacts', contact_id)

            if not contact:
                return {'success': False, 'error': 'Contact not found'}

            return {'success': True, 'data': contact}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_contact(self, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """
        Create new contact

        Required fields: project_id, name
        Optional: role, company, email, phone, address, notes, performance_rating
        """
        try:
            # Validate required fields
            required_fields = ['project_id', 'name']
            for field in required_fields:
                if field not in data:
                    return {'success': False, 'error': f'Missing required field: {field}'}

            # Generate ID and timestamps
            contact = {
                'id': data.get('id', str(uuid.uuid4())),
                'project_id': data['project_id'],
                'name': data['name'],
                'role': data.get('role', 'other'),
                'company': data.get('company', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'address': data.get('address', ''),
                'notes': data.get('notes', []),
                'contracts': data.get('contracts', []),
                'performance_rating': data.get('performance_rating'),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            # Validate performance_rating if provided
            if contact['performance_rating'] is not None:
                if not isinstance(contact['performance_rating'], int) or \
                   contact['performance_rating'] < 1 or contact['performance_rating'] > 5:
                    return {'success': False, 'error': 'performance_rating must be between 1 and 5'}

            result = data_layer.create('contacts', contact)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_contact(self, contact_id: str, data: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """Update existing contact"""
        try:
            if not contact_id:
                return {'success': False, 'error': 'Contact ID required'}

            # Check if contact exists
            existing = data_layer.get('contacts', contact_id)
            if not existing:
                return {'success': False, 'error': 'Contact not found'}

            # Validate performance_rating if being updated
            if 'performance_rating' in data and data['performance_rating'] is not None:
                if not isinstance(data['performance_rating'], int) or \
                   data['performance_rating'] < 1 or data['performance_rating'] > 5:
                    return {'success': False, 'error': 'performance_rating must be between 1 and 5'}

            # Add updated timestamp
            data['updated_at'] = datetime.utcnow().isoformat()

            result = data_layer.update('contacts', contact_id, data)

            return {'success': True, 'data': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _delete_contact(self, contact_id: str, data_layer: Any) -> Dict[str, Any]:
        """Delete contact"""
        try:
            if not contact_id:
                return {'success': False, 'error': 'Contact ID required'}

            # Check if contact exists
            existing = data_layer.get('contacts', contact_id)
            if not existing:
                return {'success': False, 'error': 'Contact not found'}

            data_layer.delete('contacts', contact_id)

            return {
                'success': True,
                'message': f'Contact {existing.get("name")} deleted'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _get_by_role(self, project_id: str, role: str, data_layer: Any) -> Dict[str, Any]:
        """Get all contacts with a specific role for a project"""
        try:
            if not project_id or not role:
                return {'success': False, 'error': 'project_id and role required'}

            filters = {
                'project_id': project_id,
                'role': role
            }

            contacts = data_layer.query('contacts', filters)

            # Sort by performance rating (highest first), then by name
            contacts.sort(key=lambda x: (
                -(x.get('performance_rating') or 0),
                x.get('name', '').lower()
            ))

            return {
                'success': True,
                'data': contacts,
                'count': len(contacts)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _add_note(self, contact_id: str, note: str, data_layer: Any) -> Dict[str, Any]:
        """Add a note to a contact's history"""
        try:
            if not contact_id or not note:
                return {'success': False, 'error': 'contact_id and note required'}

            # Get current contact
            contact = data_layer.get('contacts', contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}

            # Get existing notes
            notes = contact.get('notes', [])
            if isinstance(notes, str):
                try:
                    import json
                    notes = json.loads(notes)
                except:
                    notes = []

            # Add new note with timestamp
            new_note = {
                'date': datetime.utcnow().isoformat(),
                'text': note
            }
            notes.append(new_note)

            # Update contact
            update_data = {
                'notes': notes,
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('contacts', contact_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': 'Note added successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _add_contract(self, contact_id: str, contract: Dict[str, Any], data_layer: Any) -> Dict[str, Any]:
        """Add a contract to a contact"""
        try:
            if not contact_id or not contract:
                return {'success': False, 'error': 'contact_id and contract required'}

            # Get current contact
            contact = data_layer.get('contacts', contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}

            # Get existing contracts
            contracts = contact.get('contracts', [])
            if isinstance(contracts, str):
                try:
                    import json
                    contracts = json.loads(contracts)
                except:
                    contracts = []

            # Add contract ID and timestamp if not provided
            if 'id' not in contract:
                contract['id'] = str(uuid.uuid4())
            if 'created_at' not in contract:
                contract['created_at'] = datetime.utcnow().isoformat()

            contracts.append(contract)

            # Update contact
            update_data = {
                'contracts': contracts,
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('contacts', contact_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': 'Contract added successfully'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _rate_contact(self, contact_id: str, rating: int, data_layer: Any) -> Dict[str, Any]:
        """Set performance rating for a contact (1-5)"""
        try:
            if not contact_id:
                return {'success': False, 'error': 'contact_id required'}

            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return {'success': False, 'error': 'rating must be between 1 and 5'}

            # Get current contact
            contact = data_layer.get('contacts', contact_id)
            if not contact:
                return {'success': False, 'error': 'Contact not found'}

            # Update rating
            update_data = {
                'performance_rating': rating,
                'updated_at': datetime.utcnow().isoformat()
            }

            result = data_layer.update('contacts', contact_id, update_data)

            return {
                'success': True,
                'data': result,
                'message': f'Rating set to {rating}/5'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_info(self) -> Dict[str, Any]:
        """Return module information"""
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Contact management for architects, engineers, contractors, and suppliers',
            'actions': [
                'list',
                'get',
                'create',
                'update',
                'delete',
                'get_by_role',
                'add_note',
                'add_contract',
                'rate_contact'
            ]
        }
