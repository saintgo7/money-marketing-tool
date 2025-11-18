from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Template

from src.config import settings


class EmailService:
    """Email service for sending transactional emails"""

    def __init__(self):
        if settings.sendgrid_api_key:
            self.client = SendGridAPIClient(settings.sendgrid_api_key)
        else:
            self.client = None

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send an email"""
        if not self.client:
            print(f"Email would be sent to {to_email}: {subject}")
            return True

        try:
            message = Mail(
                from_email=Email(f"noreply@{settings.app_name.lower().replace(' ', '')}.com"),
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content),
            )

            if text_content:
                message.content = [
                    Content("text/plain", text_content),
                    Content("text/html", html_content),
                ]

            response = self.client.send(message)
            return response.status_code == 202

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_welcome_email(self, to_email: str, name: str) -> bool:
        """Send welcome email to new user"""
        template = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>환영합니다, {{ name }}님!</h1>
            <p>Money Marketing Tool에 가입해 주셔서 감사합니다.</p>
            <p>AI 기반 마케팅 자동화로 더 나은 성과를 만들어보세요.</p>

            <h2>시작하기</h2>
            <ul>
                <li>소셜 미디어 계정 연결하기</li>
                <li>첫 AI 콘텐츠 생성하기</li>
                <li>스케줄러로 게시물 예약하기</li>
            </ul>

            <p>
                <a href="https://app.moneymarketing.io/dashboard"
                   style="background-color: #2563eb; color: white; padding: 10px 20px;
                          text-decoration: none; border-radius: 5px;">
                    대시보드로 이동
                </a>
            </p>

            <p>궁금한 점이 있으시면 언제든 문의해 주세요.</p>

            <p>감사합니다,<br>Money Marketing Tool 팀</p>
        </body>
        </html>
        """

        html = Template(template).render(name=name)

        return self.send_email(
            to_email=to_email,
            subject="Money Marketing Tool에 오신 것을 환영합니다!",
            html_content=html,
        )

    def send_post_published_notification(
        self, to_email: str, platform: str, content_preview: str
    ) -> bool:
        """Send notification when post is published"""
        template = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>게시물이 발행되었습니다</h2>
            <p>{{ platform }}에 게시물이 성공적으로 발행되었습니다.</p>

            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 0;">{{ content_preview }}</p>
            </div>

            <p>
                <a href="https://app.moneymarketing.io/analytics"
                   style="background-color: #2563eb; color: white; padding: 10px 20px;
                          text-decoration: none; border-radius: 5px;">
                    성과 확인하기
                </a>
            </p>
        </body>
        </html>
        """

        html = Template(template).render(
            platform=platform.capitalize(),
            content_preview=content_preview[:100] + "..." if len(content_preview) > 100 else content_preview
        )

        return self.send_email(
            to_email=to_email,
            subject=f"{platform.capitalize()} 게시물이 발행되었습니다",
            html_content=html,
        )

    def send_weekly_report(
        self, to_email: str, name: str, stats: dict
    ) -> bool:
        """Send weekly performance report"""
        template = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>{{ name }}님의 주간 리포트</h1>
            <p>이번 주 마케팅 성과를 확인하세요.</p>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">
                <div style="background-color: #eff6ff; padding: 20px; border-radius: 10px;">
                    <h3 style="margin: 0; color: #1e40af;">게시물</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{{ stats.posts }}</p>
                </div>

                <div style="background-color: #f0fdf4; padding: 20px; border-radius: 10px;">
                    <h3 style="margin: 0; color: #15803d;">도달 수</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{{ stats.reach }}</p>
                </div>

                <div style="background-color: #fef3c7; padding: 20px; border-radius: 10px;">
                    <h3 style="margin: 0; color: #a16207;">참여</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{{ stats.engagement }}</p>
                </div>

                <div style="background-color: #fce7f3; padding: 20px; border-radius: 10px;">
                    <h3 style="margin: 0; color: #9f1239;">참여율</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{{ stats.engagement_rate }}%</p>
                </div>
            </div>

            <p>
                <a href="https://app.moneymarketing.io/analytics"
                   style="background-color: #2563eb; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 5px;">
                    전체 리포트 보기
                </a>
            </p>
        </body>
        </html>
        """

        html = Template(template).render(name=name, stats=stats)

        return self.send_email(
            to_email=to_email,
            subject="주간 마케팅 성과 리포트",
            html_content=html,
        )

    def send_password_reset(self, to_email: str, reset_token: str) -> bool:
        """Send password reset email"""
        template = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>비밀번호 재설정</h2>
            <p>비밀번호 재설정을 요청하셨습니다.</p>
            <p>아래 버튼을 클릭하여 비밀번호를 재설정하세요.</p>

            <p>
                <a href="https://app.moneymarketing.io/reset-password?token={{ token }}"
                   style="background-color: #2563eb; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 5px;">
                    비밀번호 재설정
                </a>
            </p>

            <p style="color: #6b7280; font-size: 14px;">
                이 링크는 24시간 동안 유효합니다.<br>
                요청하지 않으셨다면 이 이메일을 무시하세요.
            </p>
        </body>
        </html>
        """

        html = Template(template).render(token=reset_token)

        return self.send_email(
            to_email=to_email,
            subject="비밀번호 재설정 요청",
            html_content=html,
        )


# Singleton instance
email_service = EmailService()
