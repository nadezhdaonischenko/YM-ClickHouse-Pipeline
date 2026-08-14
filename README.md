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

Заполнить файлы:

```text
.env
.env.airflow
```

Шаблоны файлов находятся в проекте.

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
