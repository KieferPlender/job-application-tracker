from argon2 import PasswordHasher, VerificationError, InvalidHashError, VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(stored_password: str, provided_password: str) -> bool:
    try:
        ph.verify(stored_password, provided_password)
        return True
    except VerifyMismatchError:
        return False