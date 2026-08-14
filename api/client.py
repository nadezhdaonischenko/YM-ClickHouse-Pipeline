"""
HTTP-клиент проекта.

Все запросы к API выполняются только через этот модуль.
"""

from typing import Any

import requests

from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)

def get(
    url: str,
    **kwargs: Any,
) -> requests.Response:
    """
    Выполняет GET-запрос.

    Parameters
    ----------
    url : str
        URL запроса.

    kwargs
        Дополнительные параметры requests.get().

    Returns
    -------
    requests.Response
    """

    logger.debug("GET %s", url)

    response = requests.get(
        url,
        timeout=settings.HTTP_TIMEOUT,
        **kwargs,
    )

    logger.debug("Response: %s", response.status_code)

    response.raise_for_status()

    return response


def post(
    url: str,
    **kwargs: Any,
) -> requests.Response:
    """
    Выполняет POST-запрос.

    Parameters
    ----------
    url : str
        URL запроса.

    kwargs
        Дополнительные параметры requests.post().

    Returns
    -------
    requests.Response
    """

    logger.debug("POST %s", url)

    response = requests.post(
        url,
        timeout=settings.HTTP_TIMEOUT,
        **kwargs,
    )

    logger.debug("Response: %s", response.status_code)

    response.raise_for_status()

    return response