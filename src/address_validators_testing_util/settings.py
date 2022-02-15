ERROR_LOG_FILENAME = "address_validators_testing_util-errors.log"
VALIDATION_ERROR_LOG_FILENAME = "validation_error.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s:%(name)s:%(asctime)s.%(msecs)03d:%(process)d:%(thread)d:%(module)s:%(funcName)s:%(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console_output": {
            "level": "DEBUG",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "logfile": {
            "level": "INFO",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 262144,
            "backupCount": 3
        },
        "validation_error": {
            "level": "CRITICAL",
            "filename": VALIDATION_ERROR_LOG_FILENAME,
            "formatter": "default",
            "class": "logging.FileHandler",
        },
    },
    "loggers": {
        "address_validators_testing_util": {
            "level": "DEBUG",
            "handlers": ["console_output", "logfile", "validation_error"],
        }
    },
}
