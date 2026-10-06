"""
Reminder service for Event scheduler
Handles background checking of upcoming events and reminder notifications
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from storage import EventStorage
from models import Event

logger = logging.getLogger(__name__)

class ReminderService:
    """Service for managing event reminders and notifications"""
    
    def __init__(self, storage: EventStorage):
        """
        Initialize the reminder service
        
        Args:
            storage: EventStorage instance for accessing events
        """
        self.storage = storage
        self.scheduler = BackgroundScheduler()
        self.active_reminders = []  # Store current reminders
        
        # Configure timezone for Kolkata (IST)
        self.kolkata_tz = pytz.timezone('Asia/Kolkata')
        
    def start(self):
        """Start the background scheduler"""
        try:
            # Schedule reminder check every minute
            self.scheduler.add_job(
                func=self.check_reminders,
                trigger="interval",
                minutes=1,
                id='reminder_check',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("Reminder service started - checking every minute")
        except Exception as e:
            logger.error(f"Failed to start reminder service: {str(e)}")
    
    def stop(self):
        """Stop the background scheduler"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Reminder service stopped")
        except Exception as e:
            logger.error(f"Error stopping reminder service: {str(e)}")
    
    def check_reminders(self):
        """Check for events due within the next hour and update reminders"""
        try:
            # Get current time in Kolkata timezone
            now = datetime.now(self.kolkata_tz)
            one_hour_later = now + timedelta(hours=1)
            
            # Get all events
            all_events = self.storage.get_all_events()
            
            # Filter events due within the next hour
            upcoming_events = []
            for event in all_events:
                try:
                    # Parse event start time - handle various ISO formats
                    start_time = event.start_time
                    # Remove any timezone info and work in local time
                    if start_time.endswith('Z'):
                        start_time = start_time[:-1]
                    elif '+' in start_time:
                        start_time = start_time.split('+')[0]
                    elif start_time.endswith('+00:00'):
                        start_time = start_time[:-6]
                    
                    # Parse as naive datetime and assume it's in Kolkata timezone
                    event_start_naive = datetime.fromisoformat(start_time)
                    # Convert current Kolkata time to naive for comparison
                    now_naive = now.replace(tzinfo=None)
                    
                    # Create one hour later in naive time for comparison
                    one_hour_later_naive = now_naive + timedelta(hours=1)
                    
                    # Check if event is within the next hour and hasn't started yet
                    if now_naive <= event_start_naive <= one_hour_later_naive:
                        # Calculate minutes until event
                        time_diff = event_start_naive - now_naive
                        minutes_until = int(time_diff.total_seconds() / 60)
                        
                        reminder_data = {
                            'event_id': event.id,
                            'title': event.title,
                            'description': event.description,
                            'start_time': event.start_time,
                            'end_time': event.end_time,
                            'minutes_until': minutes_until,
                            'reminder_time': now.strftime('%Y-%m-%d %H:%M:%S %Z'),
                            'current_time_kolkata': now.strftime('%Y-%m-%d %H:%M:%S IST')
                        }
                        upcoming_events.append(reminder_data)
                        
                except Exception as e:
                    logger.error(f"Error processing event {event.id}: {str(e)}")
                    continue
            
            # Update active reminders
            self.active_reminders = upcoming_events
            
            if upcoming_events:
                logger.info(f"Found {len(upcoming_events)} events due within the next hour")
                for reminder in upcoming_events:
                    logger.info(f"Reminder: '{reminder['title']}' starts in {reminder['minutes_until']} minutes")
            else:
                logger.debug("No events due within the next hour")
                
        except Exception as e:
            logger.error(f"Error checking reminders: {str(e)}")
    
    def get_active_reminders(self) -> List[Dict[str, Any]]:
        """
        Get current active reminders
        
        Returns:
            List of reminder dictionaries
        """
        return self.active_reminders.copy()
    
    def has_reminders(self) -> bool:
        """
        Check if there are any active reminders
        
        Returns:
            True if there are active reminders, False otherwise
        """
        return len(self.active_reminders) > 0
    
    def get_reminder_count(self) -> int:
        """
        Get the count of active reminders
        
        Returns:
            Number of active reminders
        """
        return len(self.active_reminders)
    
    def force_check(self):
        """Force an immediate reminder check (useful for testing)"""
        logger.info("Forcing immediate reminder check")
        self.check_reminders()