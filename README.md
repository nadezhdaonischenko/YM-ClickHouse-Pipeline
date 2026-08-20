# 📊 Yandex Metrika → ClickHouse ETL

ETL-проект для выгрузки данных из **Yandex Metrika Logs API** и загрузки их в **ClickHouse**.

Поддерживаются:

- 🔹 ручной запуск через `main.py`;
- 🔹 автоматическая ежедневная загрузка через **Apache Airflow**;
- 🔄 повторные запросы при временных ошибках API;
- ⚙️ обработка и нормализация данных;
- 🗄️ миграции ClickHouse через **Alembic**;
- ♻️ версионирование записей через `ReplacingMergeTree`.

---

## 🏗️ Архитектура

```text
Yandex Metrika
      │
      ▼
   Logs API
      │
      ▼
     ETL
      │
      ▼
 ClickHouse
      ▲
      │
   Airflow
```

---

## 🛠️ Стек

- 🐍 Python 3.12
- 📈 Yandex Metrika Logs API
- 🗄️ ClickHouse
- 🐼 pandas
- 🌐 requests
- 🔌 clickhouse-connect
- ✈️ Apache Airflow 3.0.6
- 🐘 PostgreSQL 16
- 🐳 Docker
- 🔧 Alembic
- 🔄 BPMN 2.0

---

## 📁 Структура проекта

```text
yandex_metrika_clickhouse/
│
├── api/                    # Работа с Yandex Metrika API
├── config/                 # Настройки и схема данных
├── dags/                   # Airflow DAG
├── database/               # ClickHouse и Alembic migrations
├── services/               # ETL и загрузка в ClickHouse
├── utils/                  # Логирование
│
├── main.py                 # Ручной запуск ETL
├── docker-compose.yml      # Airflow + PostgreSQL
├── Dockerfile.airflow
├── requirements.txt
├── alembic.ini
├── .env
└── .env.airflow
```

---

## ⚙️ Настройка

Перед запуском необходимо заполнить два файла конфигурации:

- `.env` — для локального запуска;
- `.env.airflow` — для запуска проекта в Docker / Airflow.

### `.env`

```env

# Yandex Metrika
YANDEX_METRIKA_TOKEN=your_yandex_metrika_token
COUNTER_ID=your_counter_id

# Период для ручного запуска через main.py
START_DATE=YYYY-MM-DD
END_DATE=YYYY-MM-DD
SOURCE=visits

# ClickHouse
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_DATABASE=database_name
CLICKHOUSE_USER=user_name
CLICKHOUSE_PASSWORD=your_clickhouse_password

# HTTP
HTTP_TIMEOUT=30 # Таймаут HTTP-запросов (сек.)
API_MAX_RETRIES=3 # Количество повторных попыток
API_RETRY_DELAY=5 # Задержка между повторными попытками (сек.)

# ETL
POLL_INTERVAL=5 # Интервал проверки статуса задачи Logs API (сек.)
MAX_WAIT_TIME=1800 # Максимальное время ожидания обработки задачи (сек.)
CHUNK_SIZE=10000 # Размер пакета при записи в ClickHouse

# Logging
LOG_LEVEL=INFO
```

### `.env.airflow`

```env

# Yandex Metrika

YANDEX_METRIKA_TOKEN=your_yandex_metrika_token
COUNTER_ID=your_counter_id

# Эти даты используются только при ручном запуске main.py
# Airflow определяет даты загрузки самостоятельно.

START_DATE=YYYY-MM-DD
END_DATE=YYYY-MM-DD
SOURCE=visits

# ClickHouse
# При запуске из Docker используется host.docker.internal

CLICKHOUSE_HOST=host.docker.internal
CLICKHOUSE_PORT=8123
CLICKHOUSE_DATABASE=metrika
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your_clickhouse_password

# HTTP
HTTP_TIMEOUT=30 # Таймаут HTTP-запросов (сек.)
API_MAX_RETRIES=3 # Количество повторных попыток
API_RETRY_DELAY=5 # Задержка между повторными попытками (сек.)

# ETL
POLL_INTERVAL=5 # Интервал проверки статуса задачи Logs API (сек.)
MAX_WAIT_TIME=1800 # Максимальное время ожидания обработки задачи (сек.)
CHUNK_SIZE=10000 # Размер пакета при записи в ClickHouse

# Logging
LOG_LEVEL=INFO

# Airflow
AIRFLOW__API__AUTH__JWT_SECRET=your_random_secret_1
AIRFLOW__WEBSERVER__SECRET_KEY=your_random_secret_2

```

После заполнения конфигурации можно запускать проект.

---

## 🚀 Ручной запуск

Установить зависимости:

```bash
pip install -r requirements.txt
```

Применить миграции:

```bash
alembic upgrade head
```

Запустить ETL:

```bash
python main.py
```

Параметры периода загрузки задаются в `.env`.

---

## ✈️ Airflow

Запустить контейнеры:

```bash
docker compose up -d
```

Проверить состояние:

```bash
docker compose ps
```

Airflow Web UI:

```text
http://localhost:8080
```

Основной DAG:

```text
yandex_metrika_daily
```

Расписание:

```text
06:00 ежедневно
```

DAG использует `catchup=True`, поэтому пропущенные запуски за предыдущие даты будут обработаны после восстановления работы Airflow.

---

## 🗄️ ClickHouse

Основная таблица:

```text
metrika.visit
```

Используется:

```text
ReplacingMergeTree(version)
```

Для получения актуального состояния данных используется представление:

```text
metrika.visit_current
```

---

## 🔄 Миграции

Применить миграции:

```bash
alembic upgrade head
```

Текущая версия:

```bash
alembic current
```

История миграций:

```bash
alembic history
```

---

## 📐 Схема данных

Единый источник описания полей:

```text
config/schema.py
```

На его основе формируются:

- `VISIT_FIELDS` — поля для Yandex Metrika Logs API;
- `CLICKHOUSE_COLUMNS` — колонки ClickHouse.

---

## 📝 Логи

Логи сохраняются в:

```text
logs/yandex_metrika.log
```

---

## 🔍 Управление Airflow

Список DAG:

```bash
docker exec airflow-scheduler airflow dags list
```

Запуски DAG:

```bash
docker exec airflow-scheduler airflow dags list-runs yandex_metrika_daily
```

Ручной запуск:

```bash
docker exec airflow-scheduler airflow dags trigger yandex_metrika_daily
```

---

## 🔄 BPMN

BPMN 2.0 схема ETL-процесса загрузки данных из Яндекс Метрики в ClickHouse.

![BPMN ETL Pipeline](/etl_pipeline.bpmn.png)
