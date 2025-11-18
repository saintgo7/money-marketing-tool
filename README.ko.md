# 머니 마케팅 툴 - AI 마케팅 자동화 플랫폼

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Next.js](https://img.shields.io/badge/next.js-14.0+-black.svg)
![Claude](https://img.shields.io/badge/AI-Claude%20Sonnet%204.5-purple.svg)

**Claude AI 기반의 강력한 소셜 미디어 마케팅 자동화 SaaS 플랫폼**

[English](./README.md) | 한국어

</div>

## 📋 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [빠른 시작](#빠른-시작)
- [설치 가이드](#설치-가이드)
- [사용법](#사용법)
- [API 문서](#api-문서)
- [배포](#배포)
- [라이선스](#라이선스)

## 개요

**머니 마케팅 툴**은 Anthropic의 Claude Sonnet 4.5 AI를 활용하여 소셜 미디어 마케팅을 자동화하는 차세대 SaaS 플랫폼입니다. AI 기반 콘텐츠 생성, 스마트 스케줄링, 멀티 플랫폼 게시, 실시간 분석 기능을 제공합니다.

### 지원 플랫폼

- 📸 **Instagram** - 피드, 스토리, 릴스
- 👍 **Facebook** - 게시물, 페이지 관리
- 🐦 **Twitter/X** - 트윗, 스레드
- 💼 **LinkedIn** - 게시물, 기업 페이지
- 🎵 **TikTok** - 숏폼 비디오

## 주요 기능

### 🤖 AI 콘텐츠 생성

- **Claude Sonnet 4.5** 기반 고품질 콘텐츠 자동 생성
- 플랫폼별 최적화된 콘텐츠 (해시태그, 길이, 형식)
- 소셜 미디어, 이메일, 광고 카피, 비디오 스크립트 생성
- 커스텀 브랜드 보이스 및 톤 설정
- 키워드 최적화 및 타겟 오디언스 맞춤화

### 📅 스마트 스케줄링

- **Celery 기반** 비동기 작업 큐
- 과거 데이터 분석을 통한 최적 게시 시간 자동 추천
- 여러 플랫폼 동시 게시 예약
- 반복 게시 설정 (일간, 주간, 월간)
- 시간대 자동 조정

### 📊 실시간 분석 대시보드

- 상세한 성과 지표 (노출, 참여율, 클릭, 전환)
- 플랫폼별 비교 분석
- A/B 테스팅 지원
- 커스텀 리포트 생성
- 데이터 시각화 (차트, 그래프)

### 💳 구독 및 결제

Stripe 통합으로 안전한 결제 처리:

| 플랜 | 가격 | 월 AI 콘텐츠 | 소셜 계정 | 주요 기능 |
|------|------|-------------|----------|----------|
| **무료** | ₩0 | 10개 | 2개 | 기본 분석, 커뮤니티 지원 |
| **스타터** | ₩29,000 | 100개 | 5개 | 고급 분석, 스마트 스케줄링, 이메일 지원 |
| **프로** | ₩79,000 | 무제한 | 15개 | A/B 테스팅, 우선 지원, 커스텀 브랜드 보이스 |
| **에이전시** | ₩199,000 | 무제한 | 무제한 | 화이트라벨, 팀 협업, 전담 매니저, API 액세스 |

### 🎨 이미지 생성

- **Stable Diffusion XL** 통합 (Replicate API)
- AI 기반 이미지 자동 생성
- 스타일 및 품질 커스터마이징
- 소셜 미디어 최적화 이미지

### 📧 이메일 캠페인

- SendGrid 통합
- 환영 이메일 자동 발송
- 주간 성과 리포트
- 게시 알림
- 커스텀 템플릿

## 기술 스택

### 백엔드

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 + SQLAlchemy ORM
- **Cache/Queue**: Redis + Celery
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)
- **Image Gen**: Stable Diffusion XL (Replicate)
- **Payments**: Stripe API
- **Email**: SendGrid
- **Auth**: JWT + OAuth2

### 프론트엔드

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS + shadcn/ui
- **State**: Zustand
- **Charts**: Recharts
- **HTTP Client**: Axios
- **i18n**: next-intl (한글/영어 지원)

### 인프라

- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (리버스 프록시)
- **CI/CD**: GitHub Actions
- **Monitoring**: Health checks, Prometheus 메트릭
- **Error Tracking**: Sentry 통합

## 빠른 시작

### 필수 요구사항

- Docker & Docker Compose
- Node.js 18+ (로컬 개발용)
- Python 3.11+ (로컬 개발용)

### 1분 안에 시작하기

```bash
# 저장소 클론
git clone https://github.com/yourusername/money-marketing-tool.git
cd money-marketing-tool

# 환경 변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# .env 파일을 편집하여 API 키를 입력하세요

# 개발 환경 실행
./dev-setup.sh
```

서비스 접속:
- 🎨 **프론트엔드**: http://localhost:3000
- 🚀 **백엔드 API**: http://localhost:8000
- 📚 **API 문서**: http://localhost:8000/docs

## 설치 가이드

### 상세 설정

#### 1. 환경 변수 구성

필수 API 키 발급:

1. **Anthropic API** (Claude)
   - https://console.anthropic.com/ 에서 발급
   - `ANTHROPIC_API_KEY` 설정

2. **Replicate API** (이미지 생성)
   - https://replicate.com/account 에서 발급
   - `REPLICATE_API_TOKEN` 설정

3. **Stripe** (결제)
   - https://dashboard.stripe.com/ 에서 발급
   - `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` 설정

4. **SendGrid** (이메일)
   - https://sendgrid.com/ 에서 발급
   - `SENDGRID_API_KEY` 설정

5. **소셜 미디어 API**
   - Instagram, Facebook, Twitter, LinkedIn, TikTok API 키 설정

#### 2. 데이터베이스 초기화

```bash
# 마이그레이션 실행
docker-compose exec backend alembic upgrade head

# 관리자 계정 생성
docker-compose exec backend python scripts/create_admin.py

# 데모 데이터 추가 (선택사항)
docker-compose exec backend python scripts/seed_data.py
```

#### 3. 테스트 실행

```bash
# 백엔드 테스트
cd backend
pytest --cov=src --cov-report=html

# 프론트엔드 테스트
cd frontend
npm test
```

## 사용법

### AI 콘텐츠 생성

```python
# Python 예제
from src.ai.content_generator import ContentGenerator

generator = ContentGenerator(api_key="your-api-key")
content = await generator.generate_social_content(
    topic="새로운 제품 출시",
    platforms=["instagram", "twitter"],
    tone="professional",
    keywords=["혁신", "기술", "미래"]
)
```

### API 호출 예제

```bash
# 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# 콘텐츠 생성
curl -X POST http://localhost:8000/api/content/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "마케팅 팁",
    "platforms": ["instagram"],
    "tone": "friendly"
  }'
```

## API 문서

완전한 API 문서는 다음에서 확인하세요:
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Markdown**: [API_DOCS.md](./API_DOCS.md)

### 주요 엔드포인트

| 엔드포인트 | 메소드 | 설명 |
|-----------|--------|------|
| `/api/auth/login` | POST | 사용자 로그인 |
| `/api/auth/signup` | POST | 회원가입 |
| `/api/content/generate` | POST | AI 콘텐츠 생성 |
| `/api/scheduler/schedule` | POST | 게시물 예약 |
| `/api/analytics/dashboard` | GET | 분석 데이터 조회 |
| `/api/campaigns` | GET/POST | 캠페인 관리 |
| `/api/payments/subscribe` | POST | 구독 결제 |

## 배포

### 프로덕션 배포

```bash
# 프로덕션 환경 빌드 및 실행
docker-compose -f docker-compose.prod.yml up -d

# SSL 인증서 설정 (Let's Encrypt)
certbot --nginx -d yourdomain.com

# 로그 확인
docker-compose -f docker-compose.prod.yml logs -f
```

### 환경별 설정

- **개발**: `docker-compose.yml`
- **프로덕션**: `docker-compose.prod.yml`
- **CI/CD**: `.github/workflows/ci.yml`

상세한 배포 가이드: [DEPLOYMENT.md](./DEPLOYMENT.md)

## 프로젝트 구조

```
money-marketing-tool/
├── backend/                 # FastAPI 백엔드
│   ├── src/
│   │   ├── ai/             # AI 통합 (Claude, Replicate)
│   │   ├── api/            # API 라우터
│   │   ├── models/         # 데이터베이스 모델
│   │   ├── publishers/     # 소셜 미디어 게시
│   │   ├── scheduler/      # Celery 작업
│   │   └── utils/          # 유틸리티 함수
│   ├── tests/              # 테스트
│   └── scripts/            # 초기화 스크립트
├── frontend/               # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # React 컴포넌트
│   │   ├── hooks/         # 커스텀 훅
│   │   └── lib/           # API 클라이언트
│   └── messages/          # i18n 번역 파일
├── nginx/                 # Nginx 설정
├── .github/               # GitHub Actions CI/CD
└── docs/                  # 문서
```

## 성능 최적화

- **캐싱**: Redis로 API 응답 캐싱
- **비동기 처리**: Celery로 백그라운드 작업
- **데이터베이스**: 인덱싱 및 쿼리 최적화
- **CDN**: 정적 파일 최적화
- **이미지**: Next.js Image 최적화

## 보안

- ✅ JWT 기반 인증
- ✅ 비밀번호 bcrypt 해싱
- ✅ Rate limiting
- ✅ CORS 설정
- ✅ SQL 인젝션 방지 (ORM)
- ✅ XSS 방지
- ✅ HTTPS 지원

## 기여하기

풀 리퀘스트를 환영합니다! 주요 변경사항의 경우 먼저 이슈를 열어 논의해주세요.

### 개발 워크플로우

1. 포크하기
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'feat: Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 오픈

## 라이선스

MIT License - 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.

## 지원

- 📧 Email: support@moneymarketing.io
- 📚 Documentation: https://docs.moneymarketing.io
- 💬 Discord: https://discord.gg/moneymarketing
- 🐛 Issues: https://github.com/yourusername/money-marketing-tool/issues

## 로드맵

- [ ] 더 많은 소셜 미디어 플랫폼 지원 (Pinterest, Snapchat)
- [ ] 비디오 편집 기능
- [ ] AI 보이스오버 생성
- [ ] 인플루언서 협업 도구
- [ ] 고급 A/B 테스팅
- [ ] 모바일 앱 (iOS/Android)
- [ ] Zapier 통합
- [ ] 더 많은 언어 지원

## 감사의 말

- [Anthropic](https://www.anthropic.com/) - Claude AI
- [Replicate](https://replicate.com/) - Stable Diffusion XL
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Stripe](https://stripe.com/)

---

<div align="center">

**Made with ❤️ for marketers everywhere**

[Website](https://moneymarketing.io) • [Demo](https://demo.moneymarketing.io) • [Docs](https://docs.moneymarketing.io)

</div>
