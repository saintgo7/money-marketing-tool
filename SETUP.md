# 설치 및 설정 가이드 / Setup Guide

## 빠른 시작 / Quick Start

### 1. 환경 변수 설정 / Environment Setup

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your configuration
```

### 2. 개발 환경 실행 / Development Setup

```bash
# Automated setup (recommended)
./dev-setup.sh

# Or manual setup
docker-compose up -d
```

### 3. 데이터베이스 초기화 / Database Initialization

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create admin user
docker-compose exec backend python scripts/create_admin.py

# Seed demo data (optional)
docker-compose exec backend python scripts/seed_data.py
```

### 4. 테스트 실행 / Run Tests

```bash
# Backend tests
cd backend && pytest --cov=src

# Frontend tests (if configured)
cd frontend && npm test
```

## 프로덕션 배포 / Production Deployment

자세한 내용은 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참조하세요.
See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

## API 키 발급 / API Keys Required

- **Anthropic API** (Claude): https://console.anthropic.com/
- **Replicate API** (Image Generation): https://replicate.com/account
- **Stripe** (Payments): https://dashboard.stripe.com/
- **SendGrid** (Email): https://sendgrid.com/
- **Social Media APIs**: Instagram, Facebook, Twitter, LinkedIn, TikTok

## 문제 해결 / Troubleshooting

### 데이터베이스 연결 실패 / Database Connection Failed
```bash
docker-compose down -v
docker-compose up -d postgres redis
# Wait 10 seconds
docker-compose up backend
```

### 포트 충돌 / Port Conflicts
```bash
# Check ports 3000, 8000, 5432, 6379
lsof -i :8000
# Kill process or change port in docker-compose.yml
```

### 의존성 문제 / Dependency Issues
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
