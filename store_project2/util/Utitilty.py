import hashlib
import uuid

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def generate_id() -> str:
    return str(uuid.uuid4())