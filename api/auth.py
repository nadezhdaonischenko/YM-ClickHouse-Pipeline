"""
Вспомогательные функции для работы с API Яндекс Метрики.
"""

from config import settings


def build_headers(token: str) -> dict:
    """
    Формирует HTTP-заголовки для авторизации.

    Parameters
    ----------
    token : str
        OAuth-токен.

    Returns
    -------
    dict
    """

    return {
        "Authorization": f"OAuth {token}"
    }


def build_url(endpoint: str) -> str:
    """
    Формирует полный URL API Яндекс Метрики.

    Parameters
    ----------
    endpoint : str
        Endpoint без HOST.

    Returns
    -------
    str
    """

    endpoint = endpoint.lstrip("/")

    return f"{settings.YANDEX_METRIKA_HOST}/{endpoint}"