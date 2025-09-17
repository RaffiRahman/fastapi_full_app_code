class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same email or mobile number already exists."""

    def __init__(self, detail: str = "User already exists"):
        self.detail = detail

class InvalidCredentialsError(Exception):
    """Exception raised for invlid login credentials."""

    def __init__(self, detail: str = "Invalid username or password"):
        self.detail = detail

class TokenExpiredError(Exception):
    """Exception raised when a toke has expired."""

    def __init__(self, detail: str = "Token has expired"):
        self.detail = detail

class PermissionDeniedError(Exception):
    """Exception raised for insufficient permissions."""

    def __init__(self, detail: str = "Permission denied"):
        self.detail = detail
