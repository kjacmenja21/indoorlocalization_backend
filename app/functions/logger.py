from logging.config import dictConfig

from app.config import GeneralConfig


def setup_logger() -> None:
    config = GeneralConfig()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "hypercorn_like": {
                    "format": "[%(asctime)s] [%(levelname)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "hypercorn_like",
                    "level": "INFO",
                },
            },
            "loggers": {
                "fastapi": {  # FastAPI application logs
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "hypercorn.error": {  # Hypercorn error logs
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "hypercorn.access": {  # Hypercorn access logs
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "root": {  # Root logger
                "handlers": ["console"],
                "level": "INFO",
            },
        }
    )
