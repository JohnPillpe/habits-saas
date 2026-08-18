import os
import smtplib
from email.message import EmailMessage


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)


def _send_email(
    to: str,
    subject: str,
    content: str,
):
    if not all(
        [
            SMTP_HOST,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            EMAIL_FROM,
        ]
    ):
        print(
            "WARNING: SMTP is not configured."
        )
        print(
            f"Email would be sent to: {to}"
        )
        print(
            f"Subject: {subject}"
        )
        print(content)

        return

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = EMAIL_FROM
    message["To"] = to

    message.set_content(content)

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT,
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD,
        )

        server.send_message(message)


# ============================================================
# EMAIL VERIFICATION
# ============================================================

def send_verification_email(
    email: str,
    token: str,
):
    verification_url = (
        f"{FRONTEND_URL}/verify-email"
        f"?token={token}"
    )

    content = f"""
Welcome to MatchAI.

Please verify your email address by clicking the link below:

{verification_url}

This link expires in 24 hours.

If you did not create a MatchAI account, you can ignore this email.

MatchAI
""".strip()

    _send_email(
        to=email,
        subject="Verify your MatchAI email",
        content=content,
    )


# ============================================================
# PASSWORD RESET
# ============================================================

def send_password_reset_email(
    email: str,
    token: str,
):
    reset_url = (
        f"{FRONTEND_URL}/reset-password"
        f"?token={token}"
    )

    content = f"""
We received a request to reset your MatchAI password.

Click the link below to create a new password:

{reset_url}

This link expires in 30 minutes.

If you did not request a password reset, you can safely ignore this email.

MatchAI
""".strip()

    _send_email(
        to=email,
        subject="Reset your MatchAI password",
        content=content,
    )