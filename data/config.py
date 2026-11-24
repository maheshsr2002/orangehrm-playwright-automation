import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    load_dotenv()


class Config:
    """
    Configuration Layer: Isolates confidential credentials and environment variables.
    All confidential credentials are read strictly from .env.
    """
    BASE_URL: str = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com").rstrip("/")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "")

    BROWSER: str = os.getenv("BROWSER", "chromium").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    SLOW_MO: int = int(os.getenv("SLOW_MO", "1000"))
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "45000"))
    NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))

    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() in ("true", "1", "yes")
    VIDEO_RECORDING: str = os.getenv("VIDEO_RECORDING", "retain-on-failure")

    DATA_DIR: Path = PROJECT_ROOT / "data"
    PAYLOADS_DIR: Path = DATA_DIR / "payloads"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"
    SCREENSHOTS_DIR: Path = REPORTS_DIR / "screenshots"
    VIDEOS_DIR: Path = REPORTS_DIR / "videos"

    @classmethod
    def validate(cls):
        """Validates that confidential credentials are provided."""
        if not cls.ADMIN_USERNAME:
            raise ValueError("CRITICAL: ADMIN_USERNAME is missing from confidential .env file!")
        if not cls.ADMIN_PASSWORD:
            raise ValueError("CRITICAL: ADMIN_PASSWORD is missing from confidential .env file!")

    @classmethod
    def get_masked_info(cls) -> dict:
        return {
            "BASE_URL": cls.BASE_URL,
            "ADMIN_USERNAME": cls.ADMIN_USERNAME[:2] + "****" if cls.ADMIN_USERNAME else "UNSET",
            "ADMIN_PASSWORD": "********" if cls.ADMIN_PASSWORD else "UNSET",
            "BROWSER": cls.BROWSER,
            "HEADLESS": cls.HEADLESS,
            "SLOW_MO": cls.SLOW_MO
        }
