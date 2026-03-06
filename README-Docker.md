# AP Bus Booking - Docker Deployment

## Overview
This Docker setup provides a production-ready containerized deployment for the AP Bus Booking application using Waitress WSGI server.

## Quick Start

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Using Docker directly
```bash
# Build the image
docker build -t apbusbooking .

# Run the container
docker run -p 5000:5000 --name apbusbooking apbusbooking
```

## Access
- **Application URL**: http://localhost:5000
- **Health Check**: Automatic health monitoring enabled

## Docker Configuration

### Dockerfile Features
- **Base Image**: Python 3.11 slim (lightweight)
- **WSGI Server**: Waitress for production performance
- **Security**: Non-root user execution
- **Health Monitoring**: Built-in health checks
- **Optimization**: Multi-stage build with caching

### Services
- **apbusbooking**: Main application container
- **Port**: 5000 (host:container mapping)
- **Network**: Custom bridge network
- **Volumes**: Logs directory mounted

## Environment Variables
- `PORT=5000`: Application port (configurable)

## Development vs Production

### Development
```bash
python app.py
```

### Production (Docker)
```bash
docker-compose up --build
```

## Monitoring
- Health check runs every 30 seconds
- Container restarts on failure
- Logs available in mounted volume

## Troubleshooting

### View Logs
```bash
docker-compose logs apbusbooking
```

### Stop Services
```bash
docker-compose down
```

### Rebuild and Restart
```bash
docker-compose up --build --force-recreate
```
