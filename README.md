# Event Scheduler REST API 🗓️

A production-oriented **Flask REST API for event scheduling and real-time reminders**, featuring CRUD operations, event search, timezone-aware scheduling, background reminder processing, API documentation, and a responsive web interface.

## 🚀 Features

* **Complete CRUD Operations** — Create, read, update, and delete events
* **Event Management** — Manage event titles, descriptions, start times, and end times
* **Persistent Storage** — JSON-based file persistence between application sessions
* **Chronological Sorting** — Events are automatically sorted by start time
* **Event Search** — Search events by title or description
* **Real-Time Reminders** — Automatically detects events occurring within the next hour
* **Background Scheduler** — Continuous reminder monitoring using APScheduler
* **IST Timezone Support** — Time calculations use Indian Standard Time
* **Smart Reminder Status** — Displays urgency based on remaining time
* **Input Validation** — Validates event data and datetime formats
* **RESTful API** — Clean API endpoints with appropriate HTTP status codes
* **Postman Collection** — Ready-to-use API testing collection
* **Web Dashboard** — Browser-based event and reminder management
* **API Documentation** — Built-in API reference page
* **Responsive UI** — Bootstrap 5-based dark interface

## 🛠️ Tech Stack

| Category        | Technology             |
| --------------- | ---------------------- |
| Backend         | Python, Flask          |
| API             | REST API               |
| Scheduler       | APScheduler            |
| Storage         | JSON File Storage      |
| Timezone        | pytz                   |
| Frontend        | HTML, CSS, Bootstrap 5 |
| API Testing     | Postman                |
| Server          | Gunicorn               |
| Version Control | Git & GitHub           |

## 📋 Prerequisites

Before running the project, install:

* Python 3.7+
* pip
* Git

Check your installed versions:

```bash
python --version
pip --version
git --version
```

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yogesh10medikonda/event-scheduler-api.git
cd event-scheduler-api
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

The application will start on:

```text
http://localhost:5000
```

## 🌐 Application Pages

| Page                | URL                             |
| ------------------- | ------------------------------- |
| Home                | http://localhost:5000           |
| Event Management    | http://localhost:5000/events    |
| Reminders Dashboard | http://localhost:5000/reminders |
| API Documentation   | http://localhost:5000/api/docs  |
| REST API            | http://localhost:5000/api       |

## 📖 REST API

### Base URL

```text
http://localhost:5000/api
```

### Event Endpoints

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| GET    | `/events`                  | Get all events       |
| POST   | `/events`                  | Create an event      |
| GET    | `/events/{id}`             | Get a specific event |
| PUT    | `/events/{id}`             | Update an event      |
| DELETE | `/events/{id}`             | Delete an event      |
| GET    | `/events/search?q={query}` | Search events        |

### Reminder Endpoints

| Method | Endpoint            | Description                     |
| ------ | ------------------- | ------------------------------- |
| GET    | `/reminders`        | Get active reminders            |
| POST   | `/reminders/check`  | Run an immediate reminder check |
| GET    | `/reminders/status` | Check reminder service status   |

## 🔧 API Usage

### Create an Event

```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly team sync meeting",
    "start_time": "2026-10-10T09:00:00",
    "end_time": "2026-10-10T10:00:00"
  }'
```

### Get All Events

```bash
curl http://localhost:5000/api/events
```

### Search Events

```bash
curl "http://localhost:5000/api/events/search?q=meeting"
```

### Delete an Event

```bash
curl -X DELETE http://localhost:5000/api/events/{id}
```

## ⏰ Reminder System

The application includes a background reminder service that continuously monitors upcoming events.

### How It Works

1. APScheduler runs the reminder task periodically.
2. Upcoming events are checked automatically.
3. Events occurring within the next hour are identified.
4. Reminder information is displayed through the API and dashboard.
5. Events with less remaining time are highlighted as more urgent.

### Reminder Dashboard

Open:

```text
http://localhost:5000/reminders
```

The dashboard provides:

* Upcoming events
* Time remaining
* Reminder status
* Event urgency
* Automatic refresh
* Service health information

## 🕐 Timezone Handling

The application uses **Indian Standard Time (IST)** for event and reminder calculations.

This helps ensure that:

* Event times are interpreted consistently
* Reminder calculations use the correct local timezone
* Users in India receive accurate scheduling information

## 🧪 Testing with Postman

A Postman collection is included in the repository.

### Steps

1. Start the Flask application.
2. Open Postman.
3. Import `postman_collection.json`.
4. Send requests to the available endpoints.
5. Verify API responses and HTTP status codes.

The collection covers event and reminder operations.

## 📁 Project Structure

```text
event-scheduler-api/
│
├── app.py
├── main.py
├── models.py
├── storage.py
├── validators.py
├── reminder_service.py
├── requirements.txt
├── postman_collection.json
├── README.md
├── LICENSE
│
├── templates/
│   ├── index.html
│   ├── events.html
│   ├── reminders.html
│   └── api_docs.html
│
└── static/
    └── style.css
```

> `events.json` is generated automatically by the application for local data persistence.

## 🏗️ Architecture

```text
                    Client
                      │
          ┌───────────┴───────────┐
          │                       │
       Browser                 Postman
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
               Flask REST API
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Routes      Validation   Reminders
          │                       │
          ▼                       ▼
       Storage              APScheduler
          │
          ▼
       events.json
```

## 🚀 Production Deployment

The application supports deployment using Gunicorn.

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

For production deployments, configure environment variables such as:

```bash
SESSION_SECRET=your-secret-key
FLASK_ENV=production
```

## ☁️ Future Cloud Improvements

The project can be extended for cloud deployment using:

* Docker
* AWS
* Render
* PostgreSQL
* Redis
* GitHub Actions CI/CD

These are planned improvements and are not represented as currently implemented features.

## 🔐 Security Improvements

Future versions can introduce:

* JWT authentication
* User registration and login
* Role-based authorization
* Secure environment variables
* Rate limiting
* API authentication
* Database-backed user management

## 🗺️ Roadmap

* [ ] PostgreSQL database integration
* [ ] JWT authentication
* [ ] User registration and login
* [ ] Role-based authorization
* [ ] Docker containerization
* [ ] Cloud deployment
* [ ] GitHub Actions CI/CD
* [ ] Redis-based task processing
* [ ] Email notifications
* [ ] Recurring events
* [ ] Calendar import/export
* [ ] Advanced search and filtering
* [ ] Automated unit and API tests
* [ ] Swagger/OpenAPI documentation

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:

```bash
git commit -m "Add amazing feature"
```

4. Push the branch:

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Medikonda Yogesh Reddy**

B.Tech — Computer and Communication Engineering
Amrita Vishwa Vidyapeetham

GitHub: https://github.com/yogesh10medikonda

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

**Built with Python, Flask, and a focus on scalable backend development.**
