import logging
from funcs import funcs

logging.basicConfig(level=logging.DEBUG)
for func in funcs:
    logging.info(f"Executing function: {func.__name__}")
    if func.__doc__:
        logging.info(func.__doc__)
    try:
        func()
        logging.info(f"Function '{func.__name__}' completed successfully!")
    except Exception as exc:
        logging.error(f"Function '{func.__name__}' exited with an exception:")
        logging.error(f"{exc.__class__.__name__}: {exc}")
    finally:
        print()
