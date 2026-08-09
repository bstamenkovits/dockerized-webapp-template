from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2."""
    return _password_hasher.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Return True if the plaintext password matches the Argon2 hash."""
    try:
        return _password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
