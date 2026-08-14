"""
Endpoints API Яндекс Метрики.

Все URL проекта хранятся в одном месте.
"""

# Logs API

CREATE_LOG_REQUEST = (
    "management/v1/counter/{counter_id}/logrequests"
)

GET_LOG_REQUEST = (
    "management/v1/counter/{counter_id}/logrequest/{request_id}"
)

DOWNLOAD_LOG_PART = (
    "management/v1/counter/{counter_id}"
    "/logrequest/{request_id}"
    "/part/{part}/download"
)

CLEAN_LOG_REQUEST = (
    "management/v1/counter/{counter_id}"
    "/logrequest/{request_id}/clean"
)

ESTIMATE_LOG_REQUEST = (
    "management/v1/counter/{counter_id}"
    "/logrequests/evaluate"
)