# API Usage Examples

This document provides comprehensive examples of how to use the Event Scheduler API with various tools and programming languages.

## Table of Contents

- [cURL Examples](#curl-examples)
- [Python Examples](#python-examples)
- [JavaScript Examples](#javascript-examples)
- [POSTMAN Collection](#postman-collection)
- [Response Examples](#response-examples)

## cURL Examples

### 1. Create a New Event

```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Stand-up",
    "description": "Daily team synchronization meeting",
    "start_time": "2025-06-29T09:00:00",
    "end_time": "2025-06-29T09:30:00"
  }'
```

### 2. Get All Events

```bash
curl -X GET http://localhost:5000/api/events \
  -H "Content-Type: application/json"
```

### 3. Get Specific Event by ID

```bash
curl -X GET http://localhost:5000/api/events/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json"
```

### 4. Update an Event

```bash
curl -X PUT http://localhost:5000/api/events/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Team Stand-up",
    "end_time": "2025-06-29T10:00:00"
  }'
```

### 5. Delete an Event

```bash
curl -X DELETE http://localhost:5000/api/events/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json"
```

### 6. Search Events

```bash
curl -X GET "http://localhost:5000/api/events/search?q=meeting" \
  -H "Content-Type: application/json"
```

## Python Examples

### Using requests library

```python
import requests
import json
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://localhost:5000/api"

# Create an event
def create_event():
    url = f"{BASE_URL}/events"
    
    # Calculate future dates
    now = datetime.now()
    start_time = now + timedelta(hours=2)
    end_time = start_time + timedelta(hours=1)
    
    event_data = {
        "title": "Python API Test Event",
        "description": "Testing the API using Python requests",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = requests.post(url, json=event_data)
    if response.status_code == 201:
        event = response.json()
        print("Event created successfully!")
        print(f"Event ID: {event['data']['id']}")
        return event['data']['id']
    else:
        print("Error creating event:", response.json())
        return None

# Get all events
def get_all_events():
    url = f"{BASE_URL}/events"
    response = requests.get(url)
    
    if response.status_code == 200:
        events = response.json()
        print(f"Found {events['count']} events:")
        for event in events['data']:
            print(f"- {event['title']} ({event['start_time']})")
        return events['data']
    else:
        print("Error fetching events:", response.json())
        return []

# Search events
def search_events(query):
    url = f"{BASE_URL}/events/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json()
        print(f"Found {results['count']} events matching '{query}':")
        for event in results['data']:
            print(f"- {event['title']}: {event['description']}")
        return results['data']
    else:
        print("Error searching events:", response.json())
        return []

# Update an event
def update_event(event_id, updates):
    url = f"{BASE_URL}/events/{event_id}"
    response = requests.put(url, json=updates)
    
    if response.status_code == 200:
        event = response.json()
        print("Event updated successfully!")
        print(f"New title: {event['data']['title']}")
        return event['data']
    else:
        print("Error updating event:", response.json())
        return None

# Delete an event
def delete_event(event_id):
    url = f"{BASE_URL}/events/{event_id}"
    response = requests.delete(url)
    
    if response.status_code == 200:
        print("Event deleted successfully!")
        return True
    else:
        print("Error deleting event:", response.json())
        return False

# Example usage
if __name__ == "__main__":
    # Create a new event
    event_id = create_event()
    
    if event_id:
        # Get all events
        get_all_events()
        
        # Search for events
        search_events("Python")
        
        # Update the event
        update_event(event_id, {
            "title": "Updated Python Test Event",
            "description": "This event was updated via Python"
        })
        
        # Delete the event
        delete_event(event_id)
```

## JavaScript Examples

### Using fetch API

```javascript
// Base URL
const BASE_URL = 'http://localhost:5000/api';

// Create an event
async function createEvent() {
    const now = new Date();
    const startTime = new Date(now.getTime() + 2 * 60 * 60 * 1000); // 2 hours from now
    const endTime = new Date(startTime.getTime() + 60 * 60 * 1000); // 1 hour duration
    
    const eventData = {
        title: 'JavaScript API Test Event',
        description: 'Testing the API using JavaScript fetch',
        start_time: startTime.toISOString().slice(0, 19),
        end_time: endTime.toISOString().slice(0, 19)
    };
    
    try {
        const response = await fetch(`${BASE_URL}/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            console.log('Event created successfully!');
            console.log('Event ID:', result.data.id);
            return result.data.id;
        } else {
            console.error('Error creating event:', result);
            return null;
        }
    } catch (error) {
        console.error('Network error:', error);
        return null;
    }
}

// Get all events
async function getAllEvents() {
    try {
        const response = await fetch(`${BASE_URL}/events`);
        const result = await response.json();
        
        if (response.ok) {
            console.log(`Found ${result.count} events:`);
            result.data.forEach(event => {
                console.log(`- ${event.title} (${event.start_time})`);
            });
            return result.data;
        } else {
            console.error('Error fetching events:', result);
            return [];
        }
    } catch (error) {
        console.error('Network error:', error);
        return [];
    }
}

// Search events
async function searchEvents(query) {
    try {
        const response = await fetch(`${BASE_URL}/events/search?q=${encodeURIComponent(query)}`);
        const result = await response.json();
        
        if (response.ok) {
            console.log(`Found ${result.count} events matching '${query}':`);
            result.data.forEach(event => {
                console.log(`- ${event.title}: ${event.description}`);
            });
            return result.data;
        } else {
            console.error('Error searching events:', result);
            return [];
        }
    } catch (error) {
        console.error('Network error:', error);
        return [];
    }
}

// Update an event
async function updateEvent(eventId, updates) {
    try {
        const response = await fetch(`${BASE_URL}/events/${eventId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            console.log('Event updated successfully!');
            console.log('New title:', result.data.title);
            return result.data;
        } else {
            console.error('Error updating event:', result);
            return null;
        }
    } catch (error) {
        console.error('Network error:', error);
        return null;
    }
}

// Delete an event
async function deleteEvent(eventId) {
    try {
        const response = await fetch(`${BASE_URL}/events/${eventId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            console.log('Event deleted successfully!');
            return true;
        } else {
            console.error('Error deleting event:', result);
            return false;
        }
    } catch (error) {
        console.error('Network error:', error);
        return false;
    }
}

// Example usage
async function runExample() {
    // Create a new event
    const eventId = await createEvent();
    
    if (eventId) {
        // Get all events
        await getAllEvents();
        
        // Search for events
        await searchEvents('JavaScript');
        
        // Update the event
        await updateEvent(eventId, {
            title: 'Updated JavaScript Test Event',
            description: 'This event was updated via JavaScript'
        });
        
        // Delete the event
        await deleteEvent(eventId);
    }
}

// Run the example
runExample().catch(console.error);
```

## POSTMAN Collection

The included POSTMAN collection (`postman_collection.json`) provides:

1. **Pre-configured requests** for all endpoints
2. **Environment variables** with base URL
3. **Example responses** for testing
4. **Error scenarios** for validation testing

### Importing the Collection

1. Open POSTMAN
2. Click "Import" button
3. Select the `postman_collection.json` file
4. The collection will be imported with all requests ready to use

### Using the Collection

1. Set the `base_url` variable to `http://localhost:5000/api`
2. Run requests in sequence or individually
3. Check the example responses for expected formats
4. Modify request bodies as needed for testing

## Response Examples

### Successful Event Creation (201)

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "start_time": "2025-06-29T09:00:00",
    "end_time": "2025-06-29T10:00:00",
    "created_at": "2025-06-28T12:00:00",
    "updated_at": "2025-06-28T12:00:00"
  },
  "message": "Event created successfully"
}
```

### Get All Events (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Team Meeting",
      "description": "Weekly team sync",
      "start_time": "2025-06-29T09:00:00",
      "end_time": "2025-06-29T10:00:00",
      "created_at": "2025-06-28T12:00:00",
      "updated_at": "2025-06-28T12:00:00"
    }
  ],
  "count": 1
}
```

### Validation Error (400)

```json
{
  "success": false,
  "error": "Validation failed",
  "details": [
    "Field 'title' is required",
    "End time must be after start time"
  ]
}
```

### Event Not Found (404)

```json
{
  "success": false,
  "error": "Event not found"
}
```

### Search Results (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Team Meeting",
      "description": "Weekly team sync meeting",
      "start_time": "2025-06-29T09:00:00",
      "end_time": "2025-06-29T10:00:00",
      "created_at": "2025-06-28T12:00:00",
      "updated_at": "2025-06-28T12:00:00"
    }
  ],
  "count": 1,
  "query": "meeting"
}
```

## Error Handling Best Practices

When using the API, always:

1. **Check HTTP status codes** before processing responses
2. **Handle network errors** gracefully
3. **Validate input data** before sending requests
4. **Parse error messages** from the API for user feedback
5. **Implement retry logic** for temporary failures

## Rate Limiting and Performance

Currently, the API has no rate limiting, but for production use:

- Implement reasonable request intervals
- Cache responses when appropriate
- Use efficient datetime formats
- Batch operations when possible