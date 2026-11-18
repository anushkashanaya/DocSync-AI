"""Runtime configuration loaded from the environment."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent

load_dotenv(BACKEND_ROOT / ".env")


def _int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


class Settings:
    """Process-wide settings. Secrets stay on the backend."""

    app_name: str = "DocSync AI"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"
    data_dir: Path = Path(os.getenv("DOCSYNC_DATA_DIR", str(REPO_ROOT / "data"))).expanduser()
    max_upload_bytes: int = _int("MAX_UPLOAD_BYTES", 40 * 1024 * 1024)
    max_extract_bytes: int = _int("MAX_EXTRACT_BYTES", 150 * 1024 * 1024)
    max_files: int = _int("MAX_FILES", 4000)
    max_compression_ratio: int = _int("MAX_COMPRESSION_RATIO", 80)
    max_parse_bytes: int = _int("MAX_PARSE_BYTES", 1_500_000)
    gemini_max_input_chars: int = _int("GEMINI_MAX_INPUT_CHARS", 14_000)
    gemini_timeout_seconds: float = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "45"))
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key)

    @property
    def projects_dir(self) -> Path:
        return self.data_dir / "projects"


settings = Settings()
settings.projects_dir.mkdir(parents=True, exist_ok=True)
