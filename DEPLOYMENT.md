# Deployment Guide

This guide covers various deployment options for the Event Scheduler API.

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Database Migration](#database-migration)

## Local Development

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/event-scheduler-api.git
cd event-scheduler-api

# Install dependencies
pip install Flask gunicorn

# Run the application
python main.py
```

### Development Mode

The application runs in debug mode by default for development:

- Automatic reload on file changes
- Detailed error messages
- Debug logging enabled
- Host: `0.0.0.0:5000`

## Production Deployment

### Using Gunicorn

```bash
# Install gunicorn if not already installed
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app

# With configuration file
gunicorn --config gunicorn.conf.py main:app
```

### Gunicorn Configuration (gunicorn.conf.py)

```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
keepalive = 2
timeout = 30
```

### Using systemd (Linux)

Create a service file `/etc/systemd/system/event-scheduler.service`:

```ini
[Unit]
Description=Event Scheduler API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/event-scheduler-api
Environment=PATH=/path/to/event-scheduler-api/venv/bin
ExecStart=/path/to/event-scheduler-api/venv/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable event-scheduler
sudo systemctl start event-scheduler
```

## Cloud Platforms

### Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn main:app
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Railway

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Flask app
3. Set environment variables in Railway dashboard
4. Deploy with one click

### Replit Deployments

1. Your app is already configured for Replit
2. Click the "Deploy" button in Replit
3. Choose deployment settings
4. Your app will be available at `https://your-repl-name.replit.app`

### DigitalOcean App Platform

1. Create `app.yaml`:
   ```yaml
   name: event-scheduler-api
   services:
   - name: web
     source_dir: /
     github:
       repo: yourusername/event-scheduler-api
       branch: main
     run_command: gunicorn --worker-tmp-dir /dev/shm main:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     http_port: 8080
     routes:
     - path: /
   ```

2. Deploy via DigitalOcean CLI or web interface

### AWS Elastic Beanstalk

1. Create `application.py`:
   ```python
   from main import app as application
   
   if __name__ == "__main__":
       application.run()
   ```

2. Create `.ebextensions/python.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: application.py
   ```

3. Deploy:
   ```bash
   eb init
   eb create
   eb deploy
   ```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  event-scheduler:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - SESSION_SECRET=your-secret-key
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - event-scheduler
    restart: unless-stopped
```

### Build and Run

```bash
# Build the image
docker build -t event-scheduler-api .

# Run the container
docker run -p 5000:5000 event-scheduler-api

# Using docker-compose
docker-compose up -d
```

## Environment Variables

### Required Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_SECRET` | Flask session secret key | `dev-secret-key-change-in-production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to listen on | `5000` |
| `STORAGE_FILE` | JSON storage file path | `events.json` |

### Setting Environment Variables

**Linux/Mac:**
```bash
export SESSION_SECRET="your-super-secret-key"
export FLASK_ENV="production"
```

**Windows:**
```cmd
set SESSION_SECRET=your-super-secret-key
set FLASK_ENV=production
```

**Docker:**
```bash
docker run -e SESSION_SECRET="your-secret-key" -p 5000:5000 event-scheduler-api
```

## Database Migration

### From File Storage to Database

To migrate from JSON file storage to a database:

1. Install database dependencies:
   ```bash
   pip install flask-sqlalchemy psycopg2-binary  # For PostgreSQL
   # or
   pip install flask-sqlalchemy pymysql  # For MySQL
   ```

2. Create migration script:
   ```python
   import json
   from app import app, db
   from models import Event
   
   def migrate_json_to_db():
       with open('events.json', 'r') as f:
           events_data = json.load(f)
       
       with app.app_context():
           for event_data in events_data:
               event = Event.from_dict(event_data)
               db.session.add(event)
           db.session.commit()
   
   if __name__ == '__main__':
       migrate_json_to_db()
   ```

3. Run migration:
   ```bash
   python migrate.py
   ```

## Reverse Proxy (Nginx)

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/event-scheduler-api/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### Application Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint

Add to your Flask app:

```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

## Performance Optimization

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use a proper WSGI server (Gunicorn, uWSGI)
- [ ] Configure reverse proxy (Nginx, Apache)
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Set secure session secret
- [ ] Enable gzip compression
- [ ] Set up file storage backup
- [ ] Configure health checks
- [ ] Set up error tracking (Sentry, etc.)

### Gunicorn Best Practices

- Workers: `(2 * CPU cores) + 1`
- Worker class: `sync` for CPU-bound, `gevent` for I/O-bound
- Max requests: `1000-1200` to prevent memory leaks
- Timeout: `30s` for API requests
- Keep-alive: `2s` for connection reuse

## Backup and Recovery

### File Storage Backup

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp events.json backups/events_$DATE.json

# Keep only last 30 days
find backups/ -name "events_*.json" -mtime +30 -delete
```

### Automated Backup with Cron

```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port or kill existing process
2. **Permission denied**: Check file permissions and user privileges
3. **Module not found**: Ensure all dependencies are installed
4. **JSON decode error**: Check events.json file format
5. **502 Bad Gateway**: Check if application is running and accessible

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Analysis

```bash
# Check application logs
tail -f /var/log/event-scheduler/app.log

# Check system logs
journalctl -u event-scheduler -f

# Check Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```