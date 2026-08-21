"""
Authentication service module.

Provides logic to authenticate users by verifying credentials against stored hashes
and generating JWT tokens upon successful authentication.
"""

import bcrypt
from app.infraDB.repositories.users_repository import UsersRepository
from app.services.jwt_service import generate_jwt


def authenticate_user(email: str, password: str):
    """
    Verify user credentials and generate a JWT on success.

    Args:
        email (str): Email address provided by the user.
        password (str): Plaintext password provided by the user.

    Returns:
        tuple(str, Users) or None:
            On success, returns a tuple of (JWT token string, user object).
            On failure (invalid credentials), returns None.
    """
    # Instantiate repository to access user records
    repo = UsersRepository()
    # Retrieve user by email; returns None if not found
    user = repo.select_user_by_email(email=email)

    # Verify user exists and password matches stored hash
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        # Authentication failed: invalid email or password
        return None

    # Generate JWT token using user information
    token = generate_jwt(user)
    # Return both token and user object for further use
    return token, user