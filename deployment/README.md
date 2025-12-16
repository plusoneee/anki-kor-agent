# AnkiKor Deployment Guide

This directory contains Docker configuration for deploying the AnkiKor application.

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Network (bridge)          │
│                                           │
│  ┌─────────────┐      ┌──────────────┐  │
│  │  Frontend   │      │   Backend    │  │
│  │  (Nginx)    │─────▶│  (FastAPI)   │  │
│  │  Port: 3000 │      │  Port: 8000  │  │
│  └─────────────┘      └──────────────┘  │
│                              │            │
└──────────────────────────────┼───────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │    Anki     │
                        │ (host:8765) │
                        └─────────────┘
```

## Services

### Backend (FastAPI)
- **Container Name**: `anki-kor-backend`
- **Port**: 8000 (internal only, not exposed)
- **Image**: `anki-kor-agent:latest`
- **Health Check**: `http://localhost:8000/`
- **Resources**:
  - CPU: 0.5-2 cores
  - Memory: 256MB-1GB

### Frontend (React + Nginx)
- **Container Name**: `anki-kor-frontend`
- **Port**: 3000 (mapped to host)
- **Image**: `anki-kor-frontend:latest`
- **Health Check**: `http://localhost/`
- **Resources**:
  - CPU: 0.25-1 core
  - Memory: 128MB-512MB

## Quick Start

### Prerequisites
1. Docker and Docker Compose installed
2. Anki running on host machine with AnkiConnect addon
3. `.env` file in project root

### Build and Start

From project root:
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

From deployment directory:
```bash
# Build and start
docker-compose -f docker-compose.yml up -d

# Rebuild images
docker-compose -f docker-compose.yml up -d --build
```

### Access

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:3000/api/docs (proxied through nginx)

## Nginx Configuration

The frontend uses Nginx with the following features:

### Static Files
- **Path**: `/static/*`
- **Caching**: 1 year with immutable cache control
- **Gzip**: Enabled for text/css/js/json files

### Assets
- **Path**: `/assets/*`
- **Caching**: 1 year with immutable cache control

### API Proxy
- **Path**: `/api/*`
- **Upstream**: `http://backend:8000/`
- **Headers**: Forwarded properly for proxying
- **CORS**: Enabled for development

### SPA Routing
- All non-API routes fallback to `index.html`
- Supports React Router client-side routing

## Volumes

### audio-data
- **Type**: Named volume
- **Mount**: `/app/audio` in backend container
- **Purpose**: Persistent storage for TTS audio files

## Environment Variables

### Backend (.env in project root)
```env
# Anki Connect URL (use host.docker.internal in Docker)
ANKI_URL=http://host.docker.internal:8765

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1

# TTS Configuration
TTS_MODEL=tts-1
TTS_VOICE=nova

# Naver Papago Configuration (optional)
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# CORS Configuration (optional, comma-separated list)
# Default allows common development ports
# CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174
```

### Frontend (.env.production)
```env
# API base URL (use /api for nginx proxy)
VITE_API_BASE_URL=/api
```

## Development vs Production

### Development (Local)
```bash
# Backend
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

Frontend connects directly to backend at `http://127.0.0.1:8000`

### Production (Docker)
```bash
# Start containers
docker-compose up -d
```

Frontend proxies API requests through Nginx to backend service

## Troubleshooting

### Frontend can't connect to backend
1. Check backend is healthy: `docker-compose ps`
2. Check logs: `docker-compose logs backend`
3. Verify network: `docker network inspect deployment_anki-network`

### Backend can't connect to Anki
1. Ensure Anki is running on host
2. Check AnkiConnect addon is installed and enabled
3. Verify `ANKI_URL=http://host.docker.internal:8765` in environment

### Static files not loading
1. Check nginx config: `docker exec anki-kor-frontend cat /etc/nginx/conf.d/default.conf`
2. Verify build output: `docker exec anki-kor-frontend ls -la /usr/share/nginx/html`
3. Check nginx logs: `docker-compose logs frontend`

### Rebuild containers
```bash
# Stop and remove containers
docker-compose down

# Rebuild images
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

## Resource Management

### View Resource Usage
```bash
docker stats anki-kor-frontend anki-kor-backend
```

### Adjust Resource Limits
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

## Security Considerations

1. **Nginx Headers**: Security headers are set in nginx.conf
2. **Non-root User**: Backend runs as non-root user (appuser)
3. **Health Checks**: Both services have health checks configured
4. **Network Isolation**: Services communicate on private bridge network
5. **Port Exposure**: Only frontend port 3000 is exposed to host

## Monitoring

### Health Checks
```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect anki-kor-frontend | jq '.[0].State.Health'
docker inspect anki-kor-backend | jq '.[0].State.Health'
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100
```

## Maintenance

### Update Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Clean Up
```bash
# Remove containers and networks
docker-compose down

# Remove volumes too (WARNING: deletes data)
docker-compose down -v

# Remove images
docker rmi anki-kor-frontend:latest anki-kor-agent:latest
```

## Production Deployment

For production deployment, consider:

1. Use a reverse proxy (Traefik, Caddy) for HTTPS
2. Set up proper logging and monitoring
3. Configure automatic backups for audio volume
4. Use Docker secrets for sensitive environment variables
5. Set up container orchestration (Docker Swarm, Kubernetes) for scaling
6. Implement CI/CD pipeline for automated deployment

---

**Generated by**: Claude Code (Sonnet 4.5)
**Last Updated**: December 16, 2024
