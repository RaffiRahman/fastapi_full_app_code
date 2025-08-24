from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase (BaseModel):
    """Base pydantic schema for user data."""

    email: EmailStr
    name: str | None = None


class UserCreate(UserBase):
    """Pydantic schema for creating a new user."""

    password: str
    is_superuser: bool = False
    roles: str = "user"
    is_active: bool = True


class UserUpdate(UserBase):
    """Pydantic schema for updating user data."""

    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    roles:str | None = None


class User(UserBase):
    """Pydantic schema for returning user data."""

    id: int
    is_active: bool
    is_superuser: bool
    roles: str
    model_config = ConfigDict(from_attributes= True)


class UserInDB(User):
    """Pydantic schema for user data stored in the database."""

    hashed_password: str
    refresh_token: str | None = None


class Token(BaseModel):
    """Pydantic schema for OAuth2 token response."""

    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """Pydantic schema for data contained in JWT token."""

    email: str | None = None


class UserEmail(BaseModel):
    """Pydantic schema for user email."""

    email: EmailStr


class UserPasswordReset(BaseModel):
    """Pydantic schema for password reset request."""

    token: str
    new_password: str


class UserPasswordChange(BaseModel):
    """Pydantic schema for password change request."""

    current_password: str
    new_password: str


class RefreshToken(BaseModel):
    """Pydantic schema for refresh requests."""

    refresh_token: str

class RefreshTokenRequest(BaseModel):
    """Pydantic schema for refresh token requests."""

    refresh_token: str