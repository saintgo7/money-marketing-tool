# Money Marketing Tool API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "company_name": "Acme Inc"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "subscription_tier": "free",
  "created_at": "2025-01-20T10:00:00Z"
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

## Content Generation

### Generate Social Media Content
```http
POST /api/v1/content/generate/social
Authorization: Bearer <token>
Content-Type: application/json

{
  "topic": "5 tips for better productivity",
  "platforms": ["instagram", "linkedin", "twitter"],
  "tone": "professional",
  "brand_voice": "helpful and encouraging",
  "keywords": ["productivity", "tips", "business"],
  "target_audience": "working professionals"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "instagram": {
      "content": "Ready to boost your productivity? Here are 5 game-changing tips...",
      "hashtags": ["#productivity", "#tips", "#business"],
      "best_time_to_post": "Wednesday at 11 AM",
      "engagement_tips": ["Ask a question", "Use carousel format"]
    },
    "linkedin": {
      "content": "In today's fast-paced work environment...",
      "hashtags": ["#Productivity", "#ProfessionalDevelopment"],
      "best_time_to_post": "Tuesday at 10 AM"
    }
  }
}
```

### Generate Image
```http
POST /api/v1/content/generate/image
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Modern office workspace with laptop",
  "style": "professional",
  "aspect_ratio": "16:9",
  "negative_prompt": "cluttered, messy"
}
```

### Generate Email Campaign
```http
POST /api/v1/content/generate/email
Authorization: Bearer <token>
Content-Type: application/json

{
  "campaign_type": "promotional",
  "subject_variants": 3,
  "product_info": "New productivity app",
  "key_points": ["Save 2 hours daily", "Easy to use"],
  "cta": "Start free trial"
}
```

### Generate Ad Copy
```http
POST /api/v1/content/generate/ad-copy
Authorization: Bearer <token>
Content-Type: application/json

{
  "platform": "facebook",
  "objective": "conversions",
  "target_audience": "Small business owners",
  "product_name": "Marketing Tool Pro",
  "key_benefits": ["Save time", "Increase ROI"],
  "variants": 3
}
```

## Campaigns & Scheduling

### Schedule Post
```http
POST /api/v1/campaigns/schedule/post
Authorization: Bearer <token>
Content-Type: application/json

{
  "content_id": "content_123",
  "platform": "instagram",
  "user_id": "user_456",
  "account_id": "account_789",
  "use_optimal_timing": true,
  "audience_timezone": "America/New_York"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123",
    "scheduled_time": "2025-01-21T14:00:00Z",
    "platform": "instagram"
  }
}
```

### Get Optimal Posting Time
```http
GET /api/v1/campaigns/optimal-time?platform=instagram&audience_timezone=America/New_York
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "platform": "instagram",
    "optimal_time": "2025-01-21T14:00:00Z",
    "timezone": "America/New_York"
  }
}
```

### Get Schedule Recommendations
```http
GET /api/v1/campaigns/recommendations?platform=instagram&content_type=image&target_reach=10000
Authorization: Bearer <token>
```

## Analytics

### Get Overview
```http
GET /api/v1/analytics/overview?user_id=1&start_date=2025-01-01&end_date=2025-01-31
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "period": {
      "start": "2025-01-01",
      "end": "2025-01-31"
    },
    "summary": {
      "total_posts": 45,
      "total_impressions": 125000,
      "total_reach": 98000,
      "total_engagement": 5240,
      "avg_engagement_rate": 4.2
    }
  }
}
```

### Get Platform Performance
```http
GET /api/v1/analytics/platform-performance?user_id=1
Authorization: Bearer <token>
```

### Get Top Posts
```http
GET /api/v1/analytics/top-posts?user_id=1&limit=10&metric=engagement_rate
Authorization: Bearer <token>
```

### Get AI Insights
```http
GET /api/v1/analytics/insights?user_id=1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "type": "content_type",
      "title": "Best Performing Content Type",
      "description": "Carousel posts generate 450 average engagement",
      "recommendation": "Consider creating more carousel content",
      "priority": "high"
    }
  ]
}
```

## Social Accounts

### Connect Account
```http
POST /api/v1/social-accounts/connect
Authorization: Bearer <token>
Content-Type: application/json

{
  "platform": "instagram",
  "account_name": "@mycompany",
  "account_id": "instagram_123",
  "access_token": "token_here",
  "refresh_token": "refresh_token_here"
}
```

### List Accounts
```http
GET /api/v1/social-accounts/list?user_id=1
Authorization: Bearer <token>
```

### Disconnect Account
```http
DELETE /api/v1/social-accounts/{account_id}
Authorization: Bearer <token>
```

## Payments & Subscription

### Create Checkout Session
```http
POST /api/v1/payments/create-checkout-session
Authorization: Bearer <token>
Content-Type: application/json

{
  "tier": "pro",
  "success_url": "https://app.example.com/success",
  "cancel_url": "https://app.example.com/cancel"
}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_test_..."
}
```

### Get Subscription
```http
GET /api/v1/payments/subscription
Authorization: Bearer <token>
```

**Response:**
```json
{
  "tier": "pro",
  "status": "active",
  "max_social_accounts": 25,
  "max_ai_generations_monthly": -1,
  "ai_generations_used": 145,
  "current_period_end": "2025-02-20T00:00:00Z"
}
```

### Get Usage
```http
GET /api/v1/payments/usage
Authorization: Bearer <token>
```

**Response:**
```json
{
  "tier": "pro",
  "ai_generations": {
    "used": 145,
    "limit": -1,
    "unlimited": true
  },
  "image_generations": {
    "used": 45,
    "limit": 200,
    "percentage": 22.5
  }
}
```

### Cancel Subscription
```http
POST /api/v1/payments/cancel-subscription
Authorization: Bearer <token>
```

## Health & Monitoring

### Liveness Check
```http
GET /health/live
```

**Response:**
```json
{
  "status": "alive"
}
```

### Readiness Check
```http
GET /health/ready
```

**Response:**
```json
{
  "status": "ready",
  "checks": {
    "database": "healthy",
    "redis": "healthy"
  }
}
```

### Metrics
```http
GET /health/metrics
```

**Response:**
```json
{
  "system": {
    "cpu_percent": 45.2,
    "memory_percent": 62.1,
    "disk_percent": 34.5
  },
  "application": {
    "name": "Money Marketing Tool",
    "version": "v1",
    "environment": "production"
  }
}
```

### Application Info
```http
GET /health/info
```

## Error Responses

All endpoints may return the following error formats:

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden:**
```json
{
  "detail": "Insufficient permissions"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Too many requests",
  "message": "Rate limit exceeded. Max 100 requests per 60 seconds."
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error",
  "message": "An error occurred"
}
```

## Rate Limits

- Default: 100 requests per 60 seconds
- Per endpoint limits may vary
- Rate limit headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Pagination

List endpoints support pagination:
```http
GET /api/v1/endpoint?page=1&limit=20
```

## Interactive Documentation

Visit `/docs` for interactive API documentation (Swagger UI)
Visit `/redoc` for alternative documentation (ReDoc)
