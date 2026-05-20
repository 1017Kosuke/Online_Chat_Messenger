import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSWORD_FILE = os.path.join(BASE_DIR, "storage", "passwords.txt")


def password_writer(room_name, password, key):
    os.makedirs(os.path.dirname(PASSWORD_FILE), exist_ok=True)

    with open(PASSWORD_FILE, "a") as f:
        f.write(f"{room_name}:{password}:{key}\n")