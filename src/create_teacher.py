"""Add an assigned teacher account to teachers.json."""

import getpass
import json

from auth import TEACHERS_FILE, hash_password, load_teachers


def main() -> None:
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty.")

    password = getpass.getpass("Teacher password (at least 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Password must be at least 12 characters.")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    teachers = load_teachers()
    if username in teachers:
        raise SystemExit(f"Teacher account already exists: {username}")

    salt, password_hash = hash_password(password)
    teachers[username] = {
        "username": username,
        "salt": salt,
        "password_hash": password_hash,
    }
    TEACHERS_FILE.write_text(
        json.dumps({"teachers": list(teachers.values())}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Added teacher account: {username}")


if __name__ == "__main__":
    main()
