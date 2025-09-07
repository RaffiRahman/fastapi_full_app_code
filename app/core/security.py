import logging
import re
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError, TokenExpiredError

#Configure logging
logging.getLogger("passlib").setLevel(logging.ERROR)

#Configure password hashing
pwd_context = CryptContext(
    schemes= ["bcrypt"], deprecated="auto", bcrypt__rounds=12  #Recommended number of rounds for security
)

def verify_password(plain_password: str, hash_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hash_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def send_email(to: str, subject: str, body: str):
    """Send an email (placeholder)."""
    print(f'Sending email to {to} with subject "{subject}" and body "{body}"')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def validate_password_complexity(password: str) -> bool:
    """Validate password complexity requirements."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character.")
    return True

class TokenBlacklist:
    def __init__(self):
        self._blacklist = set()

    def add_to_blacklist(self, jti: str, exp: datetime):
        self._blacklist.add(jti)

    def is_blacklisted(self, jti: str) -> bool:
        return jti in self._blacklist

token_blacklist = TokenBlacklist()

def create_refresh_token() -> str:
    """Create a secure refresh token."""
    return secrets.token_urlsafe(32)


def create_tokens(user_data: dict) -> tuple[str, str]:
    """Create both access and refresh tokens."""
    jti = secrets.token_urlsafe(8)
    access_token = create_access_token(
        data={**user_data, "jti": jti},
        expires_delta= timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_refresh_token()
    return access_token, refresh_token

def verify_token(token: str) -> dict:
    """Verify a token and check if it's blacklisted."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if token_blacklist.is_blacklisted(payload.get("jti", "")):
            raise TokenExpiredError("Token has been revoked")
        return payload
    except JWTError:
        raise InvalidCredentialsError("Invalid token")