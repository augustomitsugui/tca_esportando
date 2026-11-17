import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://post_user:post_pass@db:5432/fastapi_db",
)
JWT_LIFETIME_SECONDS = 3600


def _required_secret(name: str) -> str:
    value = os.getenv(name)
    if value is None or len(value) < 32:
        raise RuntimeError(
            f"{name} must be provided as an environment variable with at least 32 characters."
        )
    return value


JWT_SECRET = _required_secret("JWT_SECRET")
RESET_PASSWORD_TOKEN_SECRET = _required_secret("RESET_PASSWORD_TOKEN_SECRET")
VERIFICATION_TOKEN_SECRET = _required_secret("VERIFICATION_TOKEN_SECRET")