import logging

INITIALIZED_LOGGERS = {}


def get_logger(name: str, file: str = None, level: int = logging.INFO) -> logging.Logger:
    """Create logger.

    Args:
        name: logger name.
            If function called multiple times same name or
            name which starts with same prefix then will be
            returned initialized logger from the first call.
        file: file to use for storing logs.
            Default is `None`.
        level: logging level.
            Default is `logging.INFO`.

    Returns:
        logging.Logger object.
    """
    logger = logging.getLogger(name)
    if name in INITIALIZED_LOGGERS:
        return logger

    # handle hierarchical names
    # e.g., logger "a" is initialized, then logger "a.b" will skip the
    # initialization since it is a child of "a".
    for logger_name in INITIALIZED_LOGGERS:
        if name.startswith(logger_name):
            return logger

    stream_handler = logging.StreamHandler()
    handlers = [stream_handler]

    # only rank 0 will add a FileHandler
    if file is not None or file:
        file_handler = logging.FileHandler(file, "w")
        handlers.append(file_handler)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    for handler in handlers:
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    logger.setLevel(level)
    INITIALIZED_LOGGERS[name] = True
    return logger
