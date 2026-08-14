"""
Схема данных Яндекс Метрики.

Единый источник информации для всего проекта.

Для каждого поля хранится:
- поле Logs API;
- имя столбца в ClickHouse;
- тип ClickHouse.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldSchema:
    """
    Описание одного поля Logs API.
    """

    metrika_name: str
    column_name: str
    clickhouse_type: str


# Visits

VISIT_SCHEMA: list[FieldSchema] = [

    # IDs

    FieldSchema(
        "ym:s:visitID",
        "visit_id",
        "UInt64",
    ),

    FieldSchema(
        "ym:s:counterID",
        "counter_id",
        "UInt32",
    ),

    FieldSchema(
        "ym:s:clientID",
        "client_id",
        "UInt64",
    ),

    # Date

    FieldSchema(
        "ym:s:date",
        "date",
        "Date",
    ),

    FieldSchema(
        "ym:s:dateTime",
        "date_time",
        "DateTime",
    ),

    # Visit

    FieldSchema(
        "ym:s:startURL",
        "start_url",
        "String",
    ),

    FieldSchema(
        "ym:s:endURL",
        "end_url",
        "String",
    ),

    FieldSchema(
        "ym:s:pageViews",
        "page_views",
        "Int32",
    ),

    FieldSchema(
        "ym:s:visitDuration",
        "visit_duration",
        "UInt32",
    ),

    FieldSchema(
        "ym:s:bounce",
        "is_bounce",
        "UInt8",
    ),

    FieldSchema(
        "ym:s:isNewUser",
        "new_user",
        "UInt8",
    ),

    # Network

    FieldSchema(
        "ym:s:ipAddress",
        "ip_address",
        "String",
    ),

    FieldSchema(
        "ym:s:networkType",
        "network_type",
        "String",
    ),

    # Geography

    FieldSchema(
        "ym:s:regionCountry",
        "region_country",
        "String",
    ),

    FieldSchema(
        "ym:s:regionCity",
        "region_city",
        "String",
    ),

    # Traffic source
    # Используем lastsign — последнюю значимую атрибуцию.

    FieldSchema(
        "ym:s:lastsignTrafficSource",
        "traffic_source",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignSearchEngineRoot",
        "search_engine_root",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignSearchEngine",
        "search_engine",
        "String",
    ),

    FieldSchema(
        "ym:s:referer",
        "referer",
        "String",
    ),

    # UTM

    FieldSchema(
        "ym:s:lastsignUTMSource",
        "utm_source",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignUTMMedium",
        "utm_medium",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignUTMCampaign",
        "utm_campaign",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignUTMContent",
        "utm_content",
        "String",
    ),

    FieldSchema(
        "ym:s:lastsignUTMTerm",
        "utm_term",
        "String",
    ),

    # Device

    FieldSchema(
        "ym:s:deviceCategory",
        "device_category",
        "String",
    ),

    FieldSchema(
        "ym:s:mobilePhone",
        "mobile_phone",
        "String",
    ),

    FieldSchema(
        "ym:s:mobilePhoneModel",
        "mobile_phone_model",
        "String",
    ),

    # Operating system

    FieldSchema(
        "ym:s:operatingSystemRoot",
        "operating_system_root",
        "String",
    ),

    FieldSchema(
        "ym:s:operatingSystem",
        "operating_system",
        "String",
    ),

    # Browser

    FieldSchema(
        "ym:s:browser",
        "browser",
        "String",
    ),

    FieldSchema(
        "ym:s:browserMajorVersion",
        "browser_major_version",
        "UInt16",
    ),

    FieldSchema(
        "ym:s:browserMinorVersion",
        "browser_minor_version",
        "UInt16",
    ),

    # Browser / JS

    FieldSchema(
        "ym:s:cookieEnabled",
        "cookie_enabled",
        "UInt8",
    ),

    FieldSchema(
        "ym:s:javascriptEnabled",
        "javascript_enabled",
        "UInt8",
    ),

    # Screen

    FieldSchema(
        "ym:s:screenColors",
        "screen_colors",
        "UInt8",
    ),

    FieldSchema(
        "ym:s:screenWidth",
        "screen_width",
        "UInt16",
    ),

    FieldSchema(
        "ym:s:screenHeight",
        "screen_height",
        "UInt16",
    ),

    FieldSchema(
        "ym:s:windowClientWidth",
        "window_client_width",
        "UInt16",
    ),

    FieldSchema(
        "ym:s:windowClientHeight",
        "window_client_height",
        "UInt16",
    ),
]


# Fields for Logs API

VISIT_FIELDS = [
    field.metrika_name
    for field in VISIT_SCHEMA
]


# ClickHouse columns

CLICKHOUSE_COLUMNS = [
    field.column_name
    for field in VISIT_SCHEMA
]