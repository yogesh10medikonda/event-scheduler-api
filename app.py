import os
import logging
import atexit
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from models import Event
from storage import EventStorage
from validators import EventValidator
from reminder_service import ReminderService

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize storage and services
storage = EventStorage()
validator = EventValidator()
reminder_service = ReminderService(storage)

# Start reminder service
reminder_service.start()

# Ensure reminder service stops when app shuts down
atexit.register(reminder_service.stop)

@app.route('/')
def index():
    """Main page with event management interface"""
    return render_template('index.html')

@app.route('/events')
def events_page():
    """Events management page"""
    return render_template('events.html')

@app.route('/reminders')
def reminders_page():
    """Reminders page showing upcoming events"""
    return render_template('reminders.html')

@app.route('/postman_collection.json')
def download_postman_collection():
    """Download POSTMAN collection"""
    from flask import send_file
    import os
    try:
        return send_file(
            'postman_collection.json',
            as_attachment=True,
            download_name='Event_Scheduler_API_Collection.json',
            mimetype='application/json'
        )
    except Exception as e:
        app.logger.error(f"Error serving POSTMAN collection: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'POSTMAN collection not found'
        }), 404

@app.route('/api/docs')
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events, sorted by start time (earliest first)"""
    try:
        events = storage.get_all_events()
        # Sort events by start_time
        events.sort(key=lambda x: datetime.fromisoformat(x.start_time))
        
        return jsonify({
            'success': True,
            'data': [event.to_dict() for event in events],
            'count': len(events)
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting events: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve events'
        }), 500

@app.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event by ID"""
    try:
        event = storage.get_event(event_id)
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': event.to_dict()
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting event {event_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve event'
        }), 500

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate the event data
        validation_result = validator.validate_event_data(data)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_result['errors']
            }), 400
        
        # Create new event
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            start_time=data['start_time'],
            end_time=data['end_time']
        )
        
        # Save event
        saved_event = storage.save_event(event)
        
        return jsonify({
            'success': True,
            'data': saved_event.to_dict(),
            'message': 'Event created successfully'
        }), 201
        
    except Exception as e:
        app.logger.error(f"Error creating event: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create event'
        }), 500

@app.route('/api/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    try:
        # Check if event exists
        existing_event = storage.get_event(event_id)
        if not existing_event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate the event data
        validation_result = validator.validate_event_data(data, is_update=True)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_result['errors']
            }), 400
        
        # Update event fields
        if 'title' in data:
            existing_event.title = data['title']
        if 'description' in data:
            existing_event.description = data['description']
        if 'start_time' in data:
            existing_event.start_time = data['start_time']
        if 'end_time' in data:
            existing_event.end_time = data['end_time']
        
        # Update modification time
        existing_event.updated_at = datetime.now().isoformat()
        
        # Save updated event
        updated_event = storage.update_event(existing_event)
        
        return jsonify({
            'success': True,
            'data': updated_event.to_dict(),
            'message': 'Event updated successfully'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error updating event {event_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update event'
        }), 500

@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    try:
        # Check if event exists
        existing_event = storage.get_event(event_id)
        if not existing_event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        # Delete the event
        storage.delete_event(event_id)
        
        return jsonify({
            'success': True,
            'message': 'Event deleted successfully'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error deleting event {event_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete event'
        }), 500

@app.route('/api/events/search', methods=['GET'])
def search_events():
    """Search events by title or description"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query parameter "q" is required'
            }), 400
        
        events = storage.search_events(query)
        # Sort events by start_time
        events.sort(key=lambda x: datetime.fromisoformat(x.start_time))
        
        return jsonify({
            'success': True,
            'data': [event.to_dict() for event in events],
            'count': len(events),
            'query': query
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error searching events: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to search events'
        }), 500

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    """Get all active reminders for events due within the next hour"""
    try:
        reminders = reminder_service.get_active_reminders()
        
        return jsonify({
            'success': True,
            'data': reminders,
            'count': len(reminders),
            'message': f'Found {len(reminders)} events due within the next hour'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error getting reminders: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get reminders'
        }), 500

@app.route('/api/reminders/check', methods=['POST'])
def force_reminder_check():
    """Force an immediate reminder check (useful for testing)"""
    try:
        reminder_service.force_check()
        reminders = reminder_service.get_active_reminders()
        
        return jsonify({
            'success': True,
            'message': 'Reminder check completed',
            'data': reminders,
            'count': len(reminders)
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error forcing reminder check: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to check reminders'
        }), 500

@app.route('/api/reminders/status', methods=['GET'])
def get_reminder_status():
    """Get the status of the reminder service"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'service_running': reminder_service.scheduler.running,
                'active_reminders': reminder_service.get_reminder_count(),
                'has_reminders': reminder_service.has_reminders(),
                'next_check': 'Every minute'
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error getting reminder status: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get reminder status'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
