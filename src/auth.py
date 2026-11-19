"""Teacher credential helpers for the activities API."""

import hashlib
import hmac
import json
import secrets
from pathlib import Path
from typing import TypedDict


TEACHERS_FILE = Path(__file__).with_name("teachers.json")
PASSWORD_HASH_ITERATIONS = 310_000


class TeacherCredential(TypedDict):
    username: str
    salt: str
    password_hash: str


def hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return salt.hex(), password_hash.hex()


def verify_password(password: str, salt_hex: str, password_hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    expected_hash = bytes.fromhex(password_hash_hex)
    actual_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return hmac.compare_digest(actual_hash, expected_hash)


def load_teachers() -> dict[str, TeacherCredential]:
    data = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("teachers"), list):
        raise ValueError(f"{TEACHERS_FILE} must contain a 'teachers' list")

    teachers: dict[str, TeacherCredential] = {}
    for credential in data["teachers"]:
        if not isinstance(credential, dict):
            raise ValueError("Each teacher credential must be an object")

        username = credential.get("username")
        salt = credential.get("salt")
        password_hash = credential.get("password_hash")
        if not all(isinstance(value, str) and value for value in (username, salt, password_hash)):
            raise ValueError("Teacher credentials require username, salt, and password_hash")
        if username in teachers:
            raise ValueError(f"Duplicate teacher username: {username}")
        try:
            if len(bytes.fromhex(salt)) != 16 or len(bytes.fromhex(password_hash)) != 32:
                raise ValueError
        except ValueError as error:
            raise ValueError(f"Invalid password hash for teacher: {username}") from error

        teachers[username] = {
            "username": username,
            "salt": salt,
            "password_hash": password_hash,
        }
    return teachers
