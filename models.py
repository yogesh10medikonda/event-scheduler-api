import uuid
from datetime import datetime
from typing import Dict, Any

class Event:
    """Event model class for representing scheduled events"""
    
    def __init__(self, title: str, description: str, start_time: str, end_time: str, event_id: str = None):
        """
        Initialize an Event instance
        
        Args:
            title: Event title
            description: Event description
            start_time: Event start time in ISO format
            end_time: Event end time in ISO format
            event_id: Unique event ID (generated if not provided)
        """
        self.id = event_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create Event instance from dictionary"""
        event = cls(
            title=data['title'],
            description=data['description'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            event_id=data['id']
        )
        event.created_at = data.get('created_at', datetime.now().isoformat())
        event.updated_at = data.get('updated_at', datetime.now().isoformat())
        return event
    
    def __str__(self) -> str:
        """String representation of the event"""
        return f"Event(id={self.id}, title='{self.title}', start={self.start_time})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the event"""
        return (f"Event(id='{self.id}', title='{self.title}', "
                f"description='{self.description}', start_time='{self.start_time}', "
                f"end_time='{self.end_time}')")
