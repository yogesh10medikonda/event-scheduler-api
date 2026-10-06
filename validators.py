from datetime import datetime
from typing import Dict, Any, List

class EventValidator:
    """Validator class for event data"""
    
    def __init__(self):
        """Initialize the validator"""
        pass
    
    def validate_event_data(self, data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
        """
        Validate event data
        
        Args:
            data: Dictionary containing event data
            is_update: Whether this is for an update operation (allows partial data)
            
        Returns:
            Dictionary with validation result and errors
        """
        errors = []
        
        # Required fields for creation
        required_fields = ['title', 'start_time', 'end_time']
        
        if not is_update:
            # Check for required fields in creation
            for field in required_fields:
                if field not in data or not data[field]:
                    errors.append(f"Field '{field}' is required")
        
        # Validate title
        if 'title' in data:
            if not isinstance(data['title'], str):
                errors.append("Title must be a string")
            elif len(data['title'].strip()) == 0:
                errors.append("Title cannot be empty")
            elif len(data['title']) > 200:
                errors.append("Title cannot exceed 200 characters")
        
        # Validate description
        if 'description' in data:
            if not isinstance(data['description'], str):
                errors.append("Description must be a string")
            elif len(data['description']) > 1000:
                errors.append("Description cannot exceed 1000 characters")
        
        # Validate start_time
        start_time_valid = True
        start_datetime = None
        if 'start_time' in data:
            start_time_result = self._validate_datetime(data['start_time'], 'start_time')
            if not start_time_result['valid']:
                errors.extend(start_time_result['errors'])
                start_time_valid = False
            else:
                start_datetime = start_time_result['datetime']
        
        # Validate end_time
        end_time_valid = True
        end_datetime = None
        if 'end_time' in data:
            end_time_result = self._validate_datetime(data['end_time'], 'end_time')
            if not end_time_result['valid']:
                errors.extend(end_time_result['errors'])
                end_time_valid = False
            else:
                end_datetime = end_time_result['datetime']
        
        # Validate that end_time is after start_time
        if start_time_valid and end_time_valid and start_datetime and end_datetime:
            if end_datetime <= start_datetime:
                errors.append("End time must be after start time")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_datetime(self, datetime_str: str, field_name: str) -> Dict[str, Any]:
        """
        Validate datetime string format
        
        Args:
            datetime_str: DateTime string to validate
            field_name: Name of the field being validated
            
        Returns:
            Dictionary with validation result
        """
        errors = []
        parsed_datetime = None
        
        if not isinstance(datetime_str, str):
            errors.append(f"{field_name} must be a string")
            return {'valid': False, 'errors': errors, 'datetime': None}
        
        if not datetime_str.strip():
            errors.append(f"{field_name} cannot be empty")
            return {'valid': False, 'errors': errors, 'datetime': None}
        
        # Try to parse the datetime string
        try:
            # First try ISO format with timezone
            if datetime_str.endswith('Z'):
                parsed_datetime = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            elif '+' in datetime_str[-6:] or datetime_str.endswith('+00:00'):
                parsed_datetime = datetime.fromisoformat(datetime_str)
            else:
                # Try without timezone info
                parsed_datetime = datetime.fromisoformat(datetime_str)
        except ValueError:
            try:
                # Try common formats
                formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%dT%H:%M'
                ]
                
                for fmt in formats:
                    try:
                        parsed_datetime = datetime.strptime(datetime_str, fmt)
                        break
                    except ValueError:
                        continue
                
                if not parsed_datetime:
                    errors.append(f"{field_name} must be in ISO format (YYYY-MM-DDTHH:MM:SS) or similar")
            except Exception:
                errors.append(f"{field_name} has invalid datetime format")
        
        # Check if datetime is in the past (optional warning, not an error)
        if parsed_datetime and parsed_datetime < datetime.now():
            # This is just a warning, not blocking validation
            pass
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'datetime': parsed_datetime
        }
    
    def validate_search_query(self, query: str) -> Dict[str, Any]:
        """
        Validate search query
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with validation result
        """
        errors = []
        
        if not isinstance(query, str):
            errors.append("Search query must be a string")
        elif len(query.strip()) == 0:
            errors.append("Search query cannot be empty")
        elif len(query) > 100:
            errors.append("Search query cannot exceed 100 characters")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
