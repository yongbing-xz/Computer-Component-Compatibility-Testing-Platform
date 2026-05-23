import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JWT_KEY_FILE = os.path.join(DATA_DIR, ".jwt-key")


class Settings:
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    DEMO_USER: str = "demo"
    DEMO_PASSWORD: str = "123456"

    @property
    def JWT_SECRET_KEY(self) -> str:
        if os.path.exists(JWT_KEY_FILE):
            with open(JWT_KEY_FILE, "r") as f:
                key = f.read().strip()
                if key:
                    return key
        key = secrets.token_hex(32)
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(JWT_KEY_FILE, "w") as f:
            f.write(key)
        return key


settings = Settings()
