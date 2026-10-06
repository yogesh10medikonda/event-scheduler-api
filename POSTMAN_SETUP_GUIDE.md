# POSTMAN Setup Guide for Event Scheduler API

This guide will help you set up and use the POSTMAN collection to test all the Event Scheduler API endpoints.

## 📥 Download the Collection

### Method 1: Direct Download from Running Application

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Download the collection**:
   - Visit: `http://localhost:5000/postman_collection.json`
   - The file will download automatically as `Event_Scheduler_API_Collection.json`

### Method 2: Download from Web Interface

1. Go to `http://localhost:5000` (homepage)
2. Click the "Download POSTMAN Collection" button
3. Or go to `http://localhost:5000/api/docs` and download from there

### Method 3: Direct File Access

Copy the `postman_collection.json` file from your project directory.

## 📦 Import into POSTMAN

### Step 1: Open POSTMAN

1. Launch POSTMAN application
2. If you don't have POSTMAN, download it from [postman.com](https://www.postman.com/downloads/)

### Step 2: Import Collection

1. **Click "Import"** button in POSTMAN (top-left area)
2. **Choose "Upload Files"** or drag and drop the JSON file
3. **Select** the downloaded `Event_Scheduler_API_Collection.json` file
4. **Click "Import"**

### Step 3: Verify Import

You should see a new collection named **"Event Scheduler API"** in your collections panel.

## ⚙️ Configure Environment

### Option 1: Use Collection Variables (Recommended)

The collection comes with a pre-configured variable:
- `base_url`: `http://localhost:5000/api`

### Option 2: Create Custom Environment

1. **Click the gear icon** (top-right) in POSTMAN
2. **Select "Manage Environments"**
3. **Click "Add"** to create new environment
4. **Add variable**:
   - **Variable**: `base_url`
   - **Initial Value**: `http://localhost:5000/api`
   - **Current Value**: `http://localhost:5000/api`
5. **Save the environment**
6. **Select it** from the environment dropdown

## 🚀 Using the Collection

### Collection Structure

The collection is organized into the following folders:

```
Event Scheduler API/
├── Events/
│   ├── Get All Events
│   ├── Get Event by ID
│   ├── Create New Event
│   ├── Update Event
│   ├── Delete Event
│   └── Search Events
```

### Testing Workflow

#### 1. Start with Getting All Events

- **Request**: `GET {{base_url}}/events`
- **Purpose**: Verify API is running and see existing events
- **Expected**: Empty list initially or existing events

#### 2. Create a New Event

- **Request**: `POST {{base_url}}/events`
- **Body**: JSON with event details
- **Required fields**: `title`, `start_time`, `end_time`
- **Optional**: `description`

**Example Request Body**:
```json
{
  "title": "Team Meeting",
  "description": "Weekly team sync meeting",
  "start_time": "2025-06-30T09:00:00",
  "end_time": "2025-06-30T10:00:00"
}
```

#### 3. Get Specific Event

- **Request**: `GET {{base_url}}/events/{event_id}`
- **Replace** `{event_id}` with actual ID from created event
- **Purpose**: Verify event was created correctly

#### 4. Update Event

- **Request**: `PUT {{base_url}}/events/{event_id}`
- **Body**: JSON with fields to update (partial updates supported)
- **Purpose**: Test update functionality

**Example Update Body**:
```json
{
  "title": "Updated Team Meeting",
  "end_time": "2025-06-30T11:00:00"
}
```

#### 5. Search Events

- **Request**: `GET {{base_url}}/events/search?q=meeting`
- **Purpose**: Test search functionality
- **Parameter**: `q` = search query

#### 6. Delete Event

- **Request**: `DELETE {{base_url}}/events/{event_id}`
- **Purpose**: Clean up test data
- **Warning**: This permanently deletes the event

## 📋 Complete Testing Checklist

### Basic CRUD Operations
- [ ] **GET** `/events` - List all events
- [ ] **POST** `/events` - Create new event
- [ ] **GET** `/events/{id}` - Get specific event
- [ ] **PUT** `/events/{id}` - Update event
- [ ] **DELETE** `/events/{id}` - Delete event

### Advanced Features
- [ ] **GET** `/events/search?q=query` - Search events
- [ ] **Partial Updates** - Update only some fields
- [ ] **Validation** - Test with invalid data

### Error Scenarios
- [ ] **404 Error** - Request non-existent event
- [ ] **400 Error** - Send invalid data
- [ ] **Validation Errors** - Missing required fields

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Refused
**Problem**: `Error: connect ECONNREFUSED 127.0.0.1:5000`
**Solution**: 
- Ensure the Flask app is running (`python main.py`)
- Check if port 5000 is available
- Verify `base_url` variable is correct

#### 2. 404 Not Found
**Problem**: `404 Not Found` for API endpoints
**Solution**:
- Check the `base_url` includes `/api`
- Correct format: `http://localhost:5000/api`
- Verify endpoint paths in requests

#### 3. Variable Not Defined
**Problem**: `{{base_url}}` not resolving
**Solution**:
- Check collection variables are imported
- Manually set environment variable
- Refresh POSTMAN

#### 4. JSON Parse Error
**Problem**: Invalid JSON in request body
**Solution**:
- Validate JSON syntax
- Check for trailing commas
- Use POSTMAN's JSON validator

### Validation Testing

#### Test Invalid Data

1. **Missing Required Fields**:
```json
{
  "description": "Missing title, start_time, end_time"
}
```

2. **Invalid DateTime Format**:
```json
{
  "title": "Test Event",
  "start_time": "invalid-date",
  "end_time": "2025-06-30T10:00:00"
}
```

3. **End Time Before Start Time**:
```json
{
  "title": "Test Event",
  "start_time": "2025-06-30T10:00:00",
  "end_time": "2025-06-30T09:00:00"
}
```

## 📊 Expected Responses

### Successful Event Creation (201)
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "start_time": "2025-06-30T09:00:00",
    "end_time": "2025-06-30T10:00:00",
    "created_at": "2025-06-29T12:00:00",
    "updated_at": "2025-06-29T12:00:00"
  },
  "message": "Event created successfully"
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

## 🔄 Collection Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:5000/api` | API base URL |

## 📝 Custom Requests

### Creating Custom Requests

You can create additional requests for specific test scenarios:

1. **Right-click** on the collection
2. **Select "Add Request"**
3. **Configure** method, URL, headers, body
4. **Use** `{{base_url}}` variable for consistency

### Example Custom Requests

#### Bulk Event Creation
Create multiple events using a loop in POSTMAN's pre-request script:

```javascript
// Pre-request Script
const events = [
    { title: "Meeting 1", start_time: "2025-06-30T09:00:00", end_time: "2025-06-30T10:00:00" },
    { title: "Meeting 2", start_time: "2025-06-30T11:00:00", end_time: "2025-06-30T12:00:00" }
];

pm.collectionVariables.set("events", JSON.stringify(events));
```

## 🎯 Advanced Testing Scenarios

### Scenario 1: Event Lifecycle Test
1. Create event
2. Verify creation
3. Update event
4. Verify update
5. Delete event
6. Verify deletion

### Scenario 2: Search Functionality Test
1. Create multiple events with different titles
2. Search for specific terms
3. Verify search results
4. Test empty search results

### Scenario 3: Validation Edge Cases
1. Test maximum field lengths
2. Test special characters
3. Test different datetime formats
4. Test boundary conditions

## 📈 Performance Testing

### Load Testing with POSTMAN

1. **Use Collection Runner**
2. **Set iterations** (e.g., 100)
3. **Add delays** between requests
4. **Monitor response times**
5. **Check for errors**

## 🔗 Sharing the Collection

### Export Collection
1. **Right-click** on collection
2. **Select "Export"**
3. **Choose format** (Collection v2.1)
4. **Save file**
5. **Share** the JSON file

### Share via Link
1. **Right-click** on collection
2. **Select "Share Collection"**
3. **Generate link**
4. **Copy and share** link

## 📞 Support

If you encounter issues:

1. **Check** this guide first
2. **Verify** the Flask app is running
3. **Test** with cURL commands first
4. **Check** POSTMAN console for errors
5. **Review** API documentation at `http://localhost:5000/api/docs`

## ✅ Quick Verification

After importing, quickly verify everything works:

1. **Send** "Get All Events" request
2. **Should return** `200 OK` with events list
3. **Send** "Create New Event" request
4. **Should return** `201 Created` with event data
5. **Collection is ready** for full testing!

Happy testing with POSTMAN! 🚀