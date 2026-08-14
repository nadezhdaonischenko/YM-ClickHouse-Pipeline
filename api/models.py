"""
Модели данных для работы с API Яндекс Метрики, описывают ответы и объекты API.
"""

from __future__ import annotations

from dataclasses import dataclass

from api.constants import STATUS_PROCESSED


# Logs API Request

@dataclass(slots=True)
class LogsRequest:
    """
    Запрос на получение данных через Logs API.
    """

    counter_id: int
    token: str
    start_date: str
    end_date: str
    source: str
    fields: list[str]


# Logs API Task

@dataclass(slots=True)
class LogsTask:
    """
    Задача Logs API.
    """

    logs_request: LogsRequest
    date1: str
    date2: str
    status: str
    request_id: int | None = None
    size: int = 0

    @property
    def counter_id(self) -> int:
        return self.logs_request.counter_id

    @property
    def token(self) -> str:
        return self.logs_request.token

    @property
    def source(self) -> str:
        return self.logs_request.source

    @property
    def fields(self) -> list[str]:
        return self.logs_request.fields

    @property
    def is_processed(self) -> bool:
        """
        Возвращает True, если задача обработана.
        """
        return self.status == STATUS_PROCESSED


# Estimate

@dataclass(slots=True)
class EstimateResponse:
    """
    Ответ метода evaluate().
    """

    possible: bool
    max_possible_day_quantity: int
    estimated_rows: int | None = None
