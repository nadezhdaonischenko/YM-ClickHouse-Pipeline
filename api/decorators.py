"""
Декораторы проекта.
"""

import functools
import time
from collections.abc import Callable

import requests

from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


def retry_api_connector(
    max_tries: int | None = None,
    delay: int | None = None,
    retry_status_codes: tuple[int, ...] = (
        429,
        500,
        502,
        503,
        504,
    ),
):
    """
    Повторяет выполнение функции при временных ошибках API.

    Parameters
    ----------
    max_tries : int | None
        Максимальное количество попыток.

    delay : int | None
        Задержка между попытками.

    retry_status_codes : tuple[int]
        HTTP-коды, при которых выполнять повтор.
    """

    max_tries = max_tries or settings.API_MAX_RETRIES
    delay = delay or settings.API_RETRY_DELAY

    def decorator(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(1, max_tries + 1):

                try:

                    return func(*args, **kwargs)

                except requests.exceptions.HTTPError as exc:

                    status_code = (
                        exc.response.status_code
                        if exc.response
                        else None
                    )

                    if status_code not in retry_status_codes:
                        raise

                    last_exception = exc

                    logger.warning(
                        "%s(): HTTP %s (%s/%s)",
                        func.__name__,
                        status_code,
                        attempt,
                        max_tries,
                    )

                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                ) as exc:

                    last_exception = exc

                    logger.warning(
                        "%s(): %s (%s/%s)",
                        func.__name__,
                        type(exc).__name__,
                        attempt,
                        max_tries,
                    )

                except Exception:
                    raise

                if attempt < max_tries:

                    logger.info(
                        "Retry after %s sec...",
                        delay,
                    )

                    time.sleep(delay)

            logger.exception(
                "%s() failed after %s attempts.",
                func.__name__,
                max_tries,
            )

            raise last_exception

        return wrapper

    return decorator