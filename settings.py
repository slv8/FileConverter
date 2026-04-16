import os
from pathlib import Path
from logging.config import dictConfig

_SECOND = 1
_MINUTE = _SECOND * 60

# General
PROJECT = "converter"
STAGING_MODE = os.getenv("STAGING_MODE", default="False").lower() in ('true',) # todo: move parse bool to utils
SITE_HOST = os.getenv("SITE_HOST", default="localhost:8000")
SITE_SCHEME: str = os.getenv("SITE_SCHEME", default="http")
SITE_URL = f"{SITE_SCHEME}://{SITE_HOST}"

# Database
DB_URI = "postgresql+asyncpg://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}".format(
    dbuser=os.getenv("DB_USER", default="user"),
    dbpassword=os.getenv("DB_PASSWORD", default="password"),
    dbhost=os.getenv("DB_HOST", default="localhost"),
    dbport=os.getenv("DB_PORT", default=5432),  # consider adding pgbouncer
    dbname=os.getenv("DB_NAME", default=PROJECT),
)

# Files
FILES_STORAGE_PATH = Path(os.getenv("FILES_STORAGE_DIR", default="uploads")).resolve()
FILES_STORAGE_PATH.mkdir(exist_ok=True)
FILES_UPLOAD_CHUNK_SIZE = os.getenv("FILES_UPLOAD_CHUNK_SIZE", default=1024 * 1024 * 10)

# Conversion
CONVERSION_TIMEOUT = float(os.getenv("CONVERSION_TIMEOUT", default=30 * _MINUTE))
CONVERSION_SCRIPT_PATH = Path(os.getenv("CONVERSION_SCRIPT_PATH", default=".scripts/convert.sh"))
if not CONVERSION_SCRIPT_PATH.exists():
    raise RuntimeError("Conversion script is not found")
CONVERSION_SCRIPT_SUCCESS_RETURN_CODE = 0

# Logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["default"],
        "level": "INFO",
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
if STAGING_MODE:
    LOGGING_CONFIG["root"]["level"] = "DEBUG"
    LOGGING_CONFIG["loggers"]["uvicorn"]["level"] = "DEBUG"
    LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = "DEBUG"
    LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = "DEBUG"
dictConfig(LOGGING_CONFIG)
