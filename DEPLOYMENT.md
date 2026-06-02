# Deployment Guide

This guide explains how to deploy the Oral Cancer Detection System for production use.

## Production Deployment

### 1. Backend Deployment (FastAPI)

#### Option A: Using Gunicorn (Linux/Mac)

```bash
# Install Gunicorn
pip install gunicorn

# Run with production settings
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Option B: Using Uvicorn with Supervisor (Linux/Mac)

Create `/etc/supervisor/conf.d/oral_cancer.conf`:

```ini
[program:oral_cancer]
directory=/path/to/project
command=/path/to/venv/bin/python app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/oral_cancer.err.log
stdout_logfile=/var/log/oral_cancer.out.log
```

Then:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start oral_cancer
```

#### Option C: Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t oral-cancer-detection .
docker run -p 8000:8000 oral-cancer-detection
```

### 2. Frontend Deployment (React)

#### Build for Production

```bash
cd frontend
npm run build
```

This creates optimized build in `frontend/build/`

#### Option A: Using Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/frontend/build;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

#### Option B: Using Apache

Create `.htaccess` in `frontend/build/`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### 3. Security Considerations

#### HTTPS/SSL

```bash
# Generate SSL certificate (Let's Encrypt)
sudo certbot certonly --standalone -d yourdomain.com
```

Update Nginx:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
}
```

#### Environment Variables

Create `.env` file:

```
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
MAX_FILE_SIZE=10485760
```

Update `app.py` to use `.env`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'default-insecure-key')
```

#### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("30/minute")
async def predict(request: Request, file: UploadFile = File(...)):
    ...
```

#### CORS Restrictions

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain only
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### 4. Database Setup (Optional)

For storing predictions and user data:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/oral_cancer_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

### 5. Monitoring & Logging

#### Backend Logging

```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"Prediction made: {prediction}")
```

#### System Monitoring

```bash
# Monitor processes
htop

# View logs
tail -f logs/app.log

# Check disk usage
df -h

# Check memory
free -h
```

### 6. Backup Strategy

```bash
# Backup models
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/

# Backup uploaded images
tar -czf images_backup_$(date +%Y%m%d).tar.gz uploaded_images/

# Backup database (if using PostgreSQL)
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

### 7. Performance Optimization

#### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)
```

#### Image Optimization

```python
from PIL import Image

def optimize_image(image):
    # Reduce quality for faster processing
    image.thumbnail((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
    return image
```

#### Async Processing

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, process_image, img_array)
    return result
```

### 8. Load Balancing

#### Nginx Load Balancing

```nginx
upstream backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    location /api {
        proxy_pass http://backend;
    }
}
```

### 9. Health Checks

```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }
```

### 10. Domain & DNS

1. Register domain: yourdomain.com
2. Update DNS records:
   - A record: points to server IP
   - CNAME: www.yourdomain.com -> yourdomain.com

### 11. CI/CD Pipeline

#### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          ssh user@server "cd /app && git pull && python train_model.py"
```

### 12. Monitoring Services

Use monitoring tools:

- **Uptime Monitoring**: UptimeRobot, Statuspage
- **Error Tracking**: Sentry, Rollbar
- **Performance**: New Relic, DataDog
- **Logs**: ELK Stack, Splunk

### 13. Testing Before Deployment

```bash
# Run tests
pytest tests/

# Load testing
locust -f locustfile.py

# Security scan
safety check
bandit -r app.py
```

### 14. Rollback Plan

```bash
# Keep previous version
cp -r /app /app.backup

# In case of issues
rm -rf /app
cp -r /app.backup /app
systemctl restart oral_cancer
```

### 15. Scaling Strategy

- **Vertical**: Increase server resources (CPU, RAM)
- **Horizontal**: Add more backend instances with load balancer
- **Database**: Use read replicas for database scaling
- **CDN**: Use CloudFlare/AWS CloudFront for static files

---

## Deployment Checklist

- [ ] SSL/HTTPS configured
- [ ] Environment variables set
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Backups automated
- [ ] Monitoring enabled
- [ ] Health checks working
- [ ] Load balancing setup
- [ ] DNS configured
- [ ] CI/CD pipeline ready
- [ ] Security audit completed
- [ ] Performance tested
- [ ] Rollback plan in place

## Support & Monitoring

After deployment:

1. Monitor logs regularly
2. Check health endpoints
3. Track prediction accuracy
4. Monitor resource usage
5. Update models periodically
6. Keep dependencies updated
7. Security patches applied
8. User feedback collected

---

**For Production Support**: Contact your DevOps team or use managed services like AWS, Google Cloud, or Heroku.
