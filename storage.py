import json
import os
import logging
from typing import List, Optional
from models import Event

class EventStorage:
    """File-based storage manager for events"""
    
    def __init__(self, filename: str = 'events.json'):
        """
        Initialize storage with specified filename
        
        Args:
            filename: Name of the JSON file to store events
        """
        self.filename = filename
        self.logger = logging.getLogger(__name__)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure the storage file exists, create empty one if not"""
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as f:
                    json.dump([], f)
                self.logger.info(f"Created new storage file: {self.filename}")
            except Exception as e:
                self.logger.error(f"Failed to create storage file: {str(e)}")
                raise
    
    def _load_events(self) -> List[Event]:
        """Load all events from the storage file"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Event.from_dict(event_data) for event_data in data]
        except FileNotFoundError:
            self.logger.warning(f"Storage file {self.filename} not found, returning empty list")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in storage file: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading events: {str(e)}")
            raise
    
    def _save_events(self, events: List[Event]) -> None:
        """Save all events to the storage file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump([event.to_dict() for event in events], f, indent=2)
            self.logger.debug(f"Saved {len(events)} events to storage")
        except Exception as e:
            self.logger.error(f"Error saving events: {str(e)}")
            raise
    
    def get_all_events(self) -> List[Event]:
        """Get all events from storage"""
        return self._load_events()
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """
        Get a specific event by ID
        
        Args:
            event_id: The unique ID of the event
            
        Returns:
            Event if found, None otherwise
        """
        events = self._load_events()
        for event in events:
            if event.id == event_id:
                return event
        return None
    
    def save_event(self, event: Event) -> Event:
        """
        Save a new event to storage
        
        Args:
            event: Event instance to save
            
        Returns:
            The saved event
        """
        events = self._load_events()
        events.append(event)
        self._save_events(events)
        self.logger.info(f"Saved new event: {event.id}")
        return event
    
    def update_event(self, updated_event: Event) -> Event:
        """
        Update an existing event in storage
        
        Args:
            updated_event: Event instance with updated data
            
        Returns:
            The updated event
        """
        events = self._load_events()
        for i, event in enumerate(events):
            if event.id == updated_event.id:
                events[i] = updated_event
                self._save_events(events)
                self.logger.info(f"Updated event: {updated_event.id}")
                return updated_event
        
        # If event not found, raise an exception
        raise ValueError(f"Event with ID {updated_event.id} not found")
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from storage
        
        Args:
            event_id: The unique ID of the event to delete
            
        Returns:
            True if event was deleted, False if not found
        """
        events = self._load_events()
        for i, event in enumerate(events):
            if event.id == event_id:
                del events[i]
                self._save_events(events)
                self.logger.info(f"Deleted event: {event_id}")
                return True
        return False
    
    def search_events(self, query: str) -> List[Event]:
        """
        Search events by title or description
        
        Args:
            query: Search query string
            
        Returns:
            List of events matching the query
        """
        events = self._load_events()
        query_lower = query.lower()
        matching_events = []
        
        for event in events:
            if (query_lower in event.title.lower() or 
                query_lower in event.description.lower()):
                matching_events.append(event)
        
        self.logger.debug(f"Found {len(matching_events)} events matching query: {query}")
        return matching_events
    
    def get_events_count(self) -> int:
        """Get the total number of events in storage"""
        return len(self._load_events())
