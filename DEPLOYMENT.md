# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured (optional for production)
- SSL certificates (for production HTTPS)
- All API keys and credentials

## Development Deployment

### Using Quick Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd money-marketing-tool

# 2. Set environment variables
cp .env.example .env
# Edit .env with your API keys

# 3. Start services
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python scripts/init_db.py

# 5. Create admin user
docker-compose exec backend python scripts/create_admin.py
```

## Production Deployment

### 1. Prepare Environment

```bash
# Copy production environment template
cp .env.production.example .env.production

# Edit .env.production with production credentials
nano .env.production
```

Required environment variables:
- `SECRET_KEY`: Strong random secret key
- `POSTGRES_PASSWORD`: Strong database password
- `REDIS_PASSWORD`: Strong Redis password
- `ANTHROPIC_API_KEY`: Production Anthropic API key
- `STRIPE_SECRET_KEY`: Production Stripe key
- `SENDGRID_API_KEY`: Production SendGrid key
- Social media API credentials

### 2. SSL Certificates

#### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot

# Generate certificates
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

### 3. Update Nginx Configuration

Edit `nginx/nginx.conf` and uncomment the HTTPS server block. Update `server_name` with your domain.

### 4. Deploy with Docker Compose

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Initialize database
docker-compose -f docker-compose.prod.yml exec backend python scripts/init_db.py

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Create admin user
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_admin.py
```

### 5. Verify Deployment

```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Test API
curl https://yourdomain.com/health

# Test frontend
curl https://yourdomain.com
```

## Cloud Platform Deployments

### AWS (Amazon Web Services)

#### Using ECS (Elastic Container Service)

1. Push Docker images to ECR
```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag images
docker build -t marketing-backend:latest -f backend/Dockerfile.prod backend/
docker build -t marketing-frontend:latest -f frontend/Dockerfile.prod frontend/

# Tag for ECR
docker tag marketing-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/marketing-backend:latest
docker tag marketing-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/marketing-frontend:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/marketing-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/marketing-frontend:latest
```

2. Set up RDS PostgreSQL database
3. Set up ElastiCache Redis
4. Create ECS task definitions
5. Deploy to ECS cluster

### Google Cloud Platform (GCP)

#### Using Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/[PROJECT-ID]/marketing-backend backend/
gcloud builds submit --tag gcr.io/[PROJECT-ID]/marketing-frontend frontend/

# Deploy to Cloud Run
gcloud run deploy marketing-backend \
  --image gcr.io/[PROJECT-ID]/marketing-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy marketing-frontend \
  --image gcr.io/[PROJECT-ID]/marketing-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### DigitalOcean

1. Create Droplet (Ubuntu 22.04)
2. Install Docker and Docker Compose
3. Clone repository
4. Follow production deployment steps above

### Heroku

```bash
# Login to Heroku
heroku login

# Create apps
heroku create marketing-backend
heroku create marketing-frontend

# Add PostgreSQL and Redis
heroku addons:create heroku-postgresql:hobby-dev -a marketing-backend
heroku addons:create heroku-redis:hobby-dev -a marketing-backend

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=xxx -a marketing-backend
# ... set all other environment variables

# Deploy
git push heroku main
```

## Database Migrations

### Creating a Migration

```bash
# After changing models
cd backend
alembic revision --autogenerate -m "Description of changes"

# Review migration file in alembic/versions/

# Apply migration
alembic upgrade head
```

### Rolling Back

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision-id>
```

## Monitoring and Logging

### Application Logs

```bash
# View backend logs
docker-compose -f docker-compose.prod.yml logs -f backend

# View Celery worker logs
docker-compose -f docker-compose.prod.yml logs -f celery_worker

# View all logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Monitoring Services

- **Sentry**: Error tracking and performance monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/health

# Database connectivity
docker-compose -f docker-compose.prod.yml exec backend python -c "from src.models.database import engine; print(engine.connect())"

# Redis connectivity
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

## Backup and Recovery

### Database Backup

```bash
# Manual backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U marketing_user marketing_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated daily backups (add to crontab)
0 2 * * * cd /path/to/project && docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U marketing_user marketing_prod > backups/backup_$(date +\%Y\%m\%d).sql
```

### Database Restore

```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U marketing_user marketing_prod < backup_20250120.sql
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend workers
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Scale Celery workers
docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=4
```

### Load Balancing

Use Nginx or a cloud load balancer to distribute traffic across multiple backend instances.

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable database backups
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable 2FA for admin accounts
- [ ] Regular security updates
- [ ] Configure Sentry for error tracking
- [ ] Set up monitoring and alerts

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Rebuild containers
docker-compose -f docker-compose.prod.yml up -d --build --force-recreate
```

### Database Connection Errors

```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps postgres

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U marketing_user -d marketing_prod
```

### High Memory Usage

```bash
# Check container resource usage
docker stats

# Limit container resources in docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

## Support

For deployment issues:
- Check documentation: https://docs.moneymarketing.io
- GitHub Issues: https://github.com/yourusername/money-marketing-tool/issues
- Email: support@moneymarketing.io
