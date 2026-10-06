# Event Scheduler REST API 🗓️

A comprehensive Flask REST API for event scheduling with full CRUD operations.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete events
- **Event Management**: Events with title, description, start time, and end time
- **File Persistence**: JSON-based storage that persists between sessions
- **Chronological Sorting**: Events automatically sorted by start time (earliest first)
- **Search Functionality**: Search events by title or description
- **Real-time Reminders**: Automatic minute-by-minute checks for events due within the next hour
- **Kolkata Timezone Support**: Fully integrated with IST (Indian Standard Time) for accurate local time calculations
- **Smart Notifications**: Background service continuously monitors upcoming events
- **Input Validation**: Comprehensive validation with detailed error messages
- **POSTMAN Integration**: Complete collection for API testing
- **Error Handling**: Proper HTTP status codes and meaningful error responses
- **Web Interface**: Beautiful documentation and API reference pages
- **Dark Theme UI**: Bootstrap 5 with modern dark theme
- **Auto-refresh Dashboard**: Real-time reminder display with automatic updates

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.x
- **Storage**: JSON file-based persistence
- **Scheduler**: APScheduler for background reminder tasks
- **Timezone**: pytz for Kolkata (IST) timezone support
- **Validation**: Custom validation with datetime parsing
- **Frontend**: Bootstrap 5 with dark theme
- **Documentation**: Interactive HTML documentation
- **Testing**: POSTMAN collection included

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/samarth0127/event-scheduler-api.git
cd event-scheduler-api
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask==3.0.0 APScheduler==3.11.0 pytz==2025.2 gunicorn==23.0.0
```

### 3. Run the Application

```bash
python main.py
```

### 4. Access the Application

- **Web Interface**: http://localhost:5000
- **Event Management**: http://localhost:5000/events
- **Reminders Dashboard**: http://localhost:5000/reminders
- **API Documentation**: http://localhost:5000/api/docs
- **API Base URL**: http://localhost:5000/api

The server will start on `localhost:5000` and automatically create an `events.json` file for data persistence.

## 📖 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events` | Get all events |
| POST | `/events` | Create a new event |
| GET | `/events/{id}` | Get specific event |
| PUT | `/events/{id}` | Update an event |
| DELETE | `/events/{id}` | Delete an event |
| GET | `/events/search?q={query}` | Search events |
| GET | `/reminders` | Get active reminders |
| POST | `/reminders/check` | Force reminder check |
| GET | `/reminders/status` | Get service status |

## 🔧 API Usage Examples

### Create Event

```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly team sync meeting",
    "start_time": "2025-06-29T09:00:00",
    "end_time": "2025-06-29T10:00:00"
  }'
```

#### Get All Events

```bash
curl -X GET http://localhost:5000/api/events
```

#### Search Events

```bash
curl -X GET "http://localhost:5000/api/events/search?q=meeting"
```

## ⏰ Reminder System

The Event Scheduler includes a powerful real-time reminder system that automatically monitors your events and notifies you of upcoming deadlines.

### How It Works

- **Automatic Monitoring**: Background service checks every minute for events due within the next hour
- **Kolkata Timezone**: All time calculations use IST (Indian Standard Time) for accurate local scheduling
- **Real-time Updates**: Web interface auto-refreshes every 30 seconds to show current reminders
- **Smart Notifications**: Events are highlighted based on urgency (15 minutes or less)
- **Persistent Service**: Reminder service runs continuously in the background

### Reminder API Endpoints

#### Get Active Reminders
```bash
curl -X GET http://localhost:5000/api/reminders
```

#### Force Immediate Check
```bash
curl -X POST http://localhost:5000/api/reminders/check
```

#### Get Service Status
```bash
curl -X GET http://localhost:5000/api/reminders/status
```

### Web Interface

Access the reminder dashboard at `http://localhost:5000/reminders` to see:
- Live list of upcoming events (next hour)
- Time remaining for each event
- Visual urgency indicators
- Auto-refreshing status
- Service health monitoring

### Example Response

```json
{
  "success": true,
  "data": [
    {
      "event_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Team Meeting",
      "description": "Weekly team sync",
      "start_time": "2025-06-29T14:00:00",
      "end_time": "2025-06-29T15:00:00",
      "minutes_until": 30,
      "reminder_time": "2025-06-29 13:30:00 IST",
      "current_time_kolkata": "2025-06-29 13:30:00 IST"
    }
  ],
  "count": 1,
  "message": "Found 1 events due within the next hour"
}
```

## 🧪 Testing with POSTMAN

1. Download the POSTMAN collection from the web interface at `http://localhost:5000`
2. Import the collection into POSTMAN
3. The collection includes all endpoints with example requests and responses
4. Base URL variable is pre-configured for `http://localhost:5000/api`

## 📁 Project Structure

```
event-scheduler-api/
├── app.py                    # Main Flask application
├── main.py                   # Application entry point
├── models.py                 # Event data model
├── storage.py                # File-based storage manager
├── validators.py             # Input validation logic
├── reminder_service.py       # Background reminder system
├── requirements.txt          # Python dependencies
├── postman_collection.json   # POSTMAN API collection
├── events.json               # Data storage file (auto-created)
├── templates/
│   ├── index.html           # Homepage
│   ├── events.html          # Event management interface
│   ├── reminders.html       # Reminder dashboard
│   └── api_docs.html        # API documentation
├── static/
│   └── style.css            # Custom styles
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Environment Variables

Set the following environment variables for production:

```bash
export SESSION_SECRET="your-secret-key-here"
export FLASK_ENV="production"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or need support:

1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Include steps to reproduce the problem
4. Provide system information (OS, Python version, etc.)

## 🚀 Roadmap

- [ ] Database integration (PostgreSQL/MySQL support)
- [ ] User authentication and authorization
- [ ] Email notifications for reminders
- [ ] Event recurrence patterns
- [ ] Calendar import/export functionality
- [ ] Mobile app integration
- [ ] Advanced search filters

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- APScheduler developers for background task scheduling
- Bootstrap team for the UI framework
- Contributors and testers

---

**Made with ❤️ for efficient event management**
