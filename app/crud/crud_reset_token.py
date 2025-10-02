import secrets
from datetime import datetime, timedelta, timezone
UTC = timezone.utc

from sqlalchemy.orm import Session

from app.models.password_reset_token import PasswordResetToken
from app.models.user import User

def create_password_reset_token(db: Session, uesr:User, expires_minutes: int = 60) -> str:
    """Create and persist a password reset token for a user."""
    token = secrets.token_urlsafe(32)