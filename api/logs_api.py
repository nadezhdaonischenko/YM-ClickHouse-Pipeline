"""
Работа с Logs API Яндекс Метрики.

Содержит функции:
- оценка объема данных;
- разбиение периода на задачи;
- создание задач;
- проверка статуса;
- скачивание данных;
- очистка задач.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from api.auth import build_headers, build_url
from api.client import get, post
from api.constants import (
    STATUS_NEW,
)
from api.decorators import retry_api_connector
from api.endpoints import (
    CREATE_LOG_REQUEST,
    ESTIMATE_LOG_REQUEST,
    GET_LOG_REQUEST,
    DOWNLOAD_LOG_PART,
    CLEAN_LOG_REQUEST,
)
from api.models import (
    EstimateResponse,
    LogsRequest,
    LogsTask,
)
from config import settings
from utils.logger import get_logger


logger = get_logger(__name__)


@retry_api_connector()
def get_estimation(
    request: LogsRequest,
) -> EstimateResponse:
    """
    Выполняет evaluate() Logs API.

    Parameters
    ----------
    request : LogsRequest

    Returns
    -------
    EstimateResponse
    """

    url = build_url(
        ESTIMATE_LOG_REQUEST.format(
            counter_id=request.counter_id,
        )
    )

    headers = build_headers(request.token)

    params = {
        "date1": request.start_date,
        "date2": request.end_date,
        "source": request.source,
        "fields":  ",".join(request.fields),
    }

    response = get(
        url,
        headers=headers,
        params=params,
    )

    data = response.json()["log_request_evaluation"]

    logger.debug(
        "Estimate received for counter %s",
        request.counter_id,
    )

    return EstimateResponse(
        possible=data["possible"],
        max_possible_day_quantity=data.get(
            "max_possible_day_quantity",
            0,
        ),
        estimated_rows=data.get(
            "estimated_rows",
        ),
    )

def create_requests(
    request: LogsRequest,
) -> list[LogsTask]:
    """
    Разбивает период на несколько задач,
    если Logs API не позволяет получить
    данные одним запросом.
    """

    start = datetime.strptime(
        request.start_date,
        settings.DATE_FORMAT,
    )

    end = datetime.strptime(
        request.end_date,
        settings.DATE_FORMAT,
    )

    if start > end:
        raise ValueError(
            "start_date must be earlier than end_date."
        )

    estimation = get_estimation(request)

    if estimation.possible:

        return [
            LogsTask(
                logs_request=request,
                date1=request.start_date,
                date2=request.end_date,
                status=STATUS_NEW,
            )
        ]

    if estimation.max_possible_day_quantity == 0:

        raise RuntimeError(
            "Logs API returned max_possible_day_quantity = 0."
        )

    total_days = (end - start).days

    requests_count = (
        total_days //
        estimation.max_possible_day_quantity
    ) + 1

    days_per_request = (
        total_days //
        requests_count
    ) + 1

    tasks: list[LogsTask] = []

    for index in range(requests_count):

        date1 = start + timedelta(
            days=index * days_per_request
        )

        date2 = min(
            end,
            start + timedelta(
                days=(index + 1)
                * days_per_request
                - 1
            ),
        )

        tasks.append(
            LogsTask(
                logs_request=request,
                date1=date1.strftime(
                    settings.DATE_FORMAT
                ),
                date2=date2.strftime(
                    settings.DATE_FORMAT
                ),
                status=STATUS_NEW,
            )
        )

    logger.info(
        "Created %s Logs API task(s).",
        len(tasks),
    )

    return tasks

@retry_api_connector()
def create_task(task: LogsTask) -> LogsTask:
    """
    Создает задачу Logs API.

    Parameters
    ----------
    task : LogsTask
        Задача для создания в Logs API.

    Returns
    -------
    LogsTask
        Обновленная задача с request_id и статусом.
    """

    url = build_url(
        CREATE_LOG_REQUEST.format(
            counter_id=task.counter_id,
        )
    )

    headers = build_headers(task.token)

    params = {
        "date1": task.date1,
        "date2": task.date2,
        "source": task.source,
        "fields": ",".join(
            sorted(
                task.fields,
                key=str.lower,
            )
        ),
    }
    
    logger.info(
        "Creating Logs API task for counter %s (%s - %s).",
        task.counter_id,
        task.date1,
        task.date2,
    )

    response = post(
        url,
        headers=headers,
        params=params,
    )

    data = response.json()

    log_request = data["log_request"]

    task.request_id = log_request["request_id"]
    task.status = log_request["status"]

    logger.info(
        "Logs API task created successfully. "
        "Request ID: %s, Status: %s",
        task.request_id,
        task.status,
    )

    return task

@retry_api_connector(max_tries=3)
def update_status(task: LogsTask) -> LogsTask:
    """
    Обновляет статус задачи Logs API.

    Parameters
    ----------
    task : LogsTask
        Задача Logs API.

    Returns
    -------
    LogsTask
        Обновленная задача.
    """

    if task.request_id is None:
        raise ValueError(
            "LogsTask.request_id is not specified."
        )

    url = build_url(
        GET_LOG_REQUEST.format(
            counter_id=task.counter_id,
            request_id=task.request_id,
        )
    )

    headers = build_headers(task.token)

    logger.debug(
        "Checking status of request %s.",
        task.request_id,
    )

    response = get(
        url,
        headers=headers,
    )

    data = response.json()

    log_request = data["log_request"]

    task.status = log_request["status"]

    if task.is_processed:

        task.size = len(
            log_request.get("parts", [])
        )

        logger.info(
            "Request %s processed. Parts: %s",
            task.request_id,
            task.size,
        )

    else:

        logger.debug(
            "Request %s status: %s",
            task.request_id,
            task.status,
        )

    return task

@retry_api_connector()
def download_part(
    task: LogsTask,
    part: int,
) -> str:
    """
    Скачивает одну часть данных Logs API.

    Parameters
    ----------
    task : LogsTask
        Задача Logs API.

    part : int
        Номер части.

    Returns
    -------
    str
        TSV-данные.
    """

    if task.request_id is None:
        raise ValueError(
            "LogsTask.request_id is not specified."
        )

    url = build_url(
        DOWNLOAD_LOG_PART.format(
            counter_id=task.counter_id,
            request_id=task.request_id,
            part=part,
        )
    )

    headers = build_headers(task.token)

    logger.info(
        "Downloading part %s of %s (request %s).",
        part + 1,
        task.size,
        task.request_id,
    )

    response = get(
        url,
        headers=headers,
    )

    logger.info(
        "Part %s downloaded successfully.",
        part + 1,
    )

    return response.text

@retry_api_connector()
def clean(task: LogsTask) -> None:
    """
    Удаляет задачу Logs API.

    Parameters
    ----------
    task : LogsTask
        Задача Logs API.
    """

    if task.request_id is None:
        raise ValueError(
            "LogsTask.request_id is not specified."
        )

    url = build_url(
        CLEAN_LOG_REQUEST.format(
            counter_id=task.counter_id,
            request_id=task.request_id,
        )
    )

    headers = build_headers(task.token)

    logger.info(
        "Cleaning request %s.",
        task.request_id,
    )

    post(
        url,
        headers=headers,
    )

    logger.info(
        "Request %s removed.",
        task.request_id,
    )