import secrets
from datetime import datetime, timedelta, timezone
UTC = timezone.utc

from sqlalchemy.orm import Session

from app.models.password_reset_token import PasswordResetToken
from app.models.user import User

def create_password_reset_token(db: Session, user:User, expires_minutes: int = 60) -> str:
    """Create and persist a password reset token for a user."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    db_token = PasswordResetToken(token=token, user_id=user.id, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token

def verify_password_reset_token(db: Session, token: str) -> User | None:
    """Return the user associated with a valid reset token."""
    record = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == token,
            PasswordResetToken.expires_at > datetime.now(UTC),
        ).first()
    )
    if record:
        return db.query(User).filter(User.id == record.user_id).first()
    return None

def delete_password_reset_token(db: Session, token: str) -> User | None:
    """Remove a used or expired password reset token."""
    db.query(PasswordResetToken).filter(PasswordResetToken.token == token).delete()
    db.commit()

