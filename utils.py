# utils.py
import hashlib
from typing import Optional

def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

def check_code(code: str, stored_hash: Optional[str]) -> bool:
    if not stored_hash:
        return False
    return hash_code(code) == stored_hash
