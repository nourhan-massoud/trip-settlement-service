import os

from dotenv import load_dotenv


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_int(name: str, default: int) -> int:
    raw = _env(name)
    if raw == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc


def _env_bool(name: str, default: bool) -> bool:
    raw = _env(name).lower()
    if raw == "":
        return default
    if raw in ("1", "true", "yes"):
        return True
    if raw in ("0", "false", "no"):
        return False
    raise ValueError(f"{name} must be true or false")


class Config:
    def __init__(self) -> None:
        load_dotenv()

        self.mysql_host = _env("MYSQL_HOST", "127.0.0.1")
        self.mysql_port = _env_int("MYSQL_PORT", 3306)
        self.mysql_user = _env("MYSQL_USER")
        self.mysql_password = _env("MYSQL_PASSWORD")
        self.mysql_database = _env("MYSQL_DATABASE")
        self.app_port = _env_int("APP_PORT", 8000)
        self.flask_debug = _env_bool("FLASK_DEBUG", False)

        if not self.mysql_user:
            raise ValueError("Missing config: MYSQL_USER")
        if not self.mysql_database:
            raise ValueError("Missing config: MYSQL_DATABASE")
        if self.mysql_port < 1 or self.mysql_port > 65535:
            raise ValueError("MYSQL_PORT must be between 1 and 65535")
