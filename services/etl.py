"""
ETL-процесс загрузки данных из Яндекс Метрики в ClickHouse.
"""

from __future__ import annotations

import time

from api.logs_api import (
    clean,
    create_requests,
    create_task,
    download_part,
    update_status,
)
from api.models import LogsRequest
from config import settings
from services.clickhouse_writer import write_tsv
from database.connection import (
    database_connect,
    get_visit_stats,
)
from utils.logger import get_logger


logger = get_logger(__name__)


def run_etl(request: LogsRequest) -> None:
    """
    Запускает полный ETL-процесс.

    Parameters
    ----------
    request : LogsRequest
        Параметры выгрузки Logs API.
    """

    logger.info("Starting ETL process.")

    tasks = create_requests(request)

    logger.info(
        "Created %s task(s).",
        len(tasks),
    )

    for index, task in enumerate(tasks, start=1):

        logger.info(
            "Processing task %s of %s.",
            index,
            len(tasks),
        )

        task = create_task(task)

        start_time = time.time()

        while not task.is_processed:

            if (
                time.time() - start_time
                > settings.MAX_WAIT_TIME
            ):
                raise TimeoutError(
                    f"Request {task.request_id} processing timeout."
                )

            logger.debug(
                "Waiting for request %s. Current status: %s",
                task.request_id,
                task.status,
            )

            time.sleep(settings.POLL_INTERVAL)

            task = update_status(task)

        logger.info(
            "Task %s processed. Parts: %s",
            task.request_id,
            task.size,
        )

        for part in range(task.size):

            logger.info(
                "Downloading part %s of %s.",
                part + 1,
                task.size,
            )

            tsv = download_part(
                task=task,
                part=part,
            )

            write_tsv(tsv)

        clean(task)

        logger.info(
            "Task %s completed.",
            task.request_id,
        )

    db = database_connect()
    stats = get_visit_stats(db)

    logger.info(
        "Visit statistics: total_rows=%s, unique_visits=%s, duplicates=%s",
        stats["total_rows"],
        stats["unique_visits"],
        stats["duplicates"],
    )

    logger.info(
        "ETL process completed successfully."
    )