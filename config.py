"""
Configuration module.

Loads environment variables and defines application configuration parameters
such as database connection URI, secret key for JWT, and SQLAlchemy settings.
"""

import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()

# Minimum key length recommended by RFC 7518 (Section 3.2) for HMAC-SHA256.
# PyJWT emits an InsecureKeyLengthWarning below this threshold.
MIN_SECRET_KEY_LENGTH = 32

# Shown whenever the secret is missing or too weak to sign JWTs with.
_GENERATE_HINT = (
    'Generate one with: '
    'uv run python -c "import secrets; print(secrets.token_urlsafe(32))"'
)


def _require_secret_key():
    """
    Read SECRET_KEY from the environment, refusing to start without a strong one.

    Returns:
        str: The validated secret key used to sign JWTs.

    Raises:
        RuntimeError: If SECRET_KEY is unset, empty, or shorter than
            MIN_SECRET_KEY_LENGTH characters.
    """
    secret_key = os.getenv("SECRET_KEY")

    # Fail fast instead of silently falling back to a hardcoded default
    if not secret_key:
        raise RuntimeError(
            f"SECRET_KEY is not set. Add it to your .env file. {_GENERATE_HINT}"
        )

    # A short key still signs tokens, but weakly enough that PyJWT warns about it
    if len(secret_key) < MIN_SECRET_KEY_LENGTH:
        raise RuntimeError(
            f"SECRET_KEY is too short ({len(secret_key)} characters). "
            f"It must be at least {MIN_SECRET_KEY_LENGTH} characters. {_GENERATE_HINT}"
        )

    return secret_key


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://your_user:your_password@localhost/your_database")
    SECRET_KEY = _require_secret_key()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
