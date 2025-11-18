# Money Marketing Tool - AI-Powered Marketing Automation Platform

An intelligent, all-in-one marketing automation SaaS platform that leverages AI to generate content, schedule posts, and analyze performance across multiple social media platforms.

## Features

### 🔐 Authentication & User Management
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **User Registration**: Easy signup process with email verification
- **Multi-Tier Subscriptions**: Free, Starter, Pro, and Agency tiers
- **Usage Tracking**: Real-time tracking of AI generations and resource usage
- **Profile Management**: Update user information and preferences

### AI Content Generation
- **Multi-Platform Content**: Generate platform-optimized content for Instagram, Facebook, Twitter, LinkedIn, TikTok, and more
- **Powered by Claude AI**: Uses Claude Sonnet 4.5 for high-quality, engaging content
- **Email Campaigns**: Create compelling email campaigns with A/B test variants
- **Ad Copy Generation**: Generate multiple ad copy variants for performance testing
- **Content Optimization**: Optimize existing content for better engagement
- **Content Ideas**: AI-generated content ideas based on trends and industry
- **Interactive UI**: Beautiful content creation interface with live preview

### Media Generation
- **AI Image Generation**: Create marketing images using Stable Diffusion XL
- **Carousel Creator**: Generate Instagram/LinkedIn carousel posts
- **Video Scripts**: AI-generated video scripts and storyboards
- **Thumbnail Generator**: Create eye-catching video thumbnails
- **Logo Design**: Generate logo design prompts for various styles

### Smart Scheduling
- **Optimal Timing**: AI-powered scheduling based on audience engagement patterns
- **Multi-Platform Publishing**: Post to multiple platforms simultaneously
- **Campaign Management**: Schedule entire campaigns with automated posting
- **Performance-Based Scheduling**: Learn from historical data to optimize posting times

### Analytics & Insights
- **Unified Dashboard**: Track performance across all platforms in one place
- **Performance Metrics**: Monitor impressions, reach, engagement, and conversions
- **AI Insights**: Get actionable recommendations to improve performance
- **Trend Analysis**: Identify content patterns that drive engagement
- **Competitive Analysis**: Benchmark against industry standards

### 💳 Payment & Billing
- **Stripe Integration**: Secure payment processing
- **Subscription Management**: Easy upgrade/downgrade between tiers
- **Usage-Based Billing**: Track and manage API usage
- **Webhook Support**: Real-time payment status updates

### Multi-Platform Support
- Instagram (Feed, Stories, Reels, Carousel)
- Facebook (Posts, Pages, Groups)
- Twitter/X (Tweets, Threads)
- LinkedIn (Personal, Company Pages)
- TikTok
- YouTube (Community, Shorts)
- Pinterest

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Authentication**: JWT with OAuth2, Passlib (bcrypt)
- **AI**: Anthropic Claude API, Stable Diffusion XL
- **Database**: PostgreSQL with SQLAlchemy ORM, Alembic migrations
- **Task Queue**: Celery with Redis
- **Caching**: Redis
- **Payment**: Stripe API
- **Analytics**: Pandas, NumPy
- **Testing**: Pytest with coverage

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Styling**: TailwindCSS, shadcn/ui
- **Charts**: Recharts
- **State Management**: Zustand
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Sentry, Prometheus
- **Email**: SendGrid, AWS SES

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/money-marketing-tool.git
cd money-marketing-tool
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `ANTHROPIC_API_KEY`: Get from https://console.anthropic.com
- `REPLICATE_API_TOKEN`: Get from https://replicate.com
- Social media API credentials
- Email service credentials
- Stripe keys for payments

3. **Quick Setup (Automated)**
```bash
chmod +x setup.sh
./setup.sh
```

Or manually with Docker Compose:
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)
- Celery worker
- Celery beat scheduler
- Flower monitoring (port 5555)

4. **Initialize the database**
```bash
docker-compose exec backend python scripts/init_db.py
```

5. **Create an admin user**
```bash
docker-compose exec backend python scripts/create_admin.py
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Flower (Celery monitoring): http://localhost:5555

## Development Setup

### Quick Dev Setup (Automated)
```bash
chmod +x dev-setup.sh
./dev-setup.sh
```

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python scripts/init_db.py

# Create admin user
python scripts/create_admin.py

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in another terminal)
celery -A src.scheduler.auto_scheduler:celery_app worker --loglevel=info

# Start Celery beat scheduler (in another terminal)
celery -A src.scheduler.auto_scheduler:celery_app beat --loglevel=info
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

Visit http://localhost:3000

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage report
pytest --cov=src --cov-report=html
```

## API Documentation

### Content Generation API

**Generate Social Media Content**
```bash
POST /api/v1/content/generate/social
{
  "topic": "5 tips for better productivity",
  "platforms": ["instagram", "linkedin", "twitter"],
  "tone": "professional",
  "brand_voice": "helpful and encouraging",
  "keywords": ["productivity", "time management"],
  "target_audience": "working professionals"
}
```

**Generate Image**
```bash
POST /api/v1/content/generate/image
{
  "prompt": "Modern office workspace with laptop",
  "style": "professional",
  "aspect_ratio": "16:9"
}
```

**Generate Email Campaign**
```bash
POST /api/v1/content/generate/email
{
  "campaign_type": "promotional",
  "subject_variants": 3,
  "product_info": "New productivity app launch",
  "key_points": ["Save 2 hours daily", "Easy to use", "Free trial"]
}
```

### Campaign Scheduling API

**Schedule Post**
```bash
POST /api/v1/campaigns/schedule/post
{
  "content_id": "content_123",
  "platform": "instagram",
  "user_id": "user_456",
  "account_id": "account_789",
  "use_optimal_timing": true
}
```

**Get Optimal Posting Time**
```bash
GET /api/v1/campaigns/optimal-time?platform=instagram&audience_timezone=America/New_York
```

### Analytics API

**Get Overview**
```bash
GET /api/v1/analytics/overview?user_id=123&start_date=2025-01-01&end_date=2025-01-31
```

**Get Platform Performance**
```bash
GET /api/v1/analytics/platform-performance?user_id=123
```

**Get Top Posts**
```bash
GET /api/v1/analytics/top-posts?user_id=123&limit=10&metric=engagement_rate
```

Full API documentation available at: http://localhost:8000/docs

## Architecture

```
money-marketing-tool/
├── backend/
│   ├── src/
│   │   ├── ai/
│   │   │   ├── content_generator.py  # Claude AI content generation
│   │   │   └── media_generator.py    # Image/video generation
│   │   ├── api/
│   │   │   ├── content.py           # Content API endpoints
│   │   │   ├── campaigns.py         # Campaign scheduling
│   │   │   ├── analytics.py         # Analytics endpoints
│   │   │   └── social_accounts.py   # Social account management
│   │   ├── models/
│   │   │   └── database.py          # SQLAlchemy models
│   │   ├── publishers/
│   │   │   └── social_publisher.py  # Multi-platform publisher
│   │   ├── scheduler/
│   │   │   └── auto_scheduler.py    # Celery tasks & scheduling
│   │   ├── config.py                # Configuration
│   │   └── main.py                  # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx             # Landing page
│   │   │   ├── dashboard/           # Analytics dashboard
│   │   │   └── layout.tsx
│   │   └── lib/
│   │       └── api.ts               # API client
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Subscription Tiers

### Free Tier
- 3 social accounts
- 30 AI generations/month
- Basic scheduling
- Weekly reports

### Starter ($29/month)
- 10 social accounts
- 200 AI generations/month
- 50 image generations/month
- Optimal timing
- Daily reports
- Email support

### Pro ($79/month)
- 25 social accounts
- Unlimited AI generations
- 200 image generations/month
- Team collaboration (5 members)
- Approval workflows
- API access
- Priority support

### Agency ($199/month)
- Unlimited accounts
- Client management
- White-label reports
- Bulk scheduling
- Dedicated manager
- SLA guarantee

## Roadmap

### Phase 1 (Weeks 1-4) - MVP
- [x] AI content generation engine
- [x] Basic social media integration
- [x] Database models
- [x] API endpoints
- [x] Frontend dashboard

### Phase 2 (Weeks 5-8)
- [ ] User authentication & authorization
- [ ] Social media OAuth integration
- [ ] Actual posting functionality
- [ ] Real-time analytics

### Phase 3 (Weeks 9-11)
- [ ] Payment integration (Stripe)
- [ ] Subscription management
- [ ] Usage tracking & limits
- [ ] Email notifications

### Phase 4 (Weeks 12-14)
- [ ] Advanced analytics
- [ ] A/B testing features
- [ ] Team collaboration
- [ ] White-label options

### Phase 5 (Weeks 15-16)
- [ ] Mobile app (React Native)
- [ ] Browser extension
- [ ] API marketplace
- [ ] Advanced automations

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- Documentation: https://docs.moneymarketing.io
- Email: support@moneymarketing.io
- Discord: https://discord.gg/moneymarketing

## Security

For security issues, please email security@moneymarketing.io instead of using the issue tracker.

## Acknowledgments

- Powered by [Anthropic Claude](https://www.anthropic.com)
- UI components by [shadcn/ui](https://ui.shadcn.com)
- Icons by [Lucide](https://lucide.dev)

---

Built with by the Money Marketing Tool team
