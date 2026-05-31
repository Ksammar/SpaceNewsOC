# SpaceNews Aggregator

Агрегатор новостей космонавтики. Автоматически собирает новости из RSS-лент, распределяет по трём категориям (Россия, Наука, Частный космос).

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
cd frontend && npm install
```

### 2. Настройка

```bash
cp .env.example .env
```

### 3. Запуск бэкенда

```bash
python main.py
```

### 4. Запуск фронтенда (в отдельном терминале)

```bash
cd frontend && npm run dev
```

### 5. Запуск парсера вручную

```bash
python -m app.services.parser
```

### 6. Автоматический парсинг

```bash
python scheduler.py
```

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/news` | Список новостей (page, category) |
| GET | `/api/news/{id}` | Детали новости |
| GET | `/api/sources` | Список источников |
| POST | `/api/parser/run` | Запуск парсера |
| GET | `/api/parser/status` | Статус парсера |
| GET | `/health` | Проверка здоровья |

## Deploy

```bash
docker compose up --build
```
