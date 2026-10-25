# 🧠 SaveAs Pro — Your AI-Powered Second Brain in Telegram

> **Сохраняйте знания → Ищите по смыслу → Спрашивайте ИИ**  
> Персональный AI-ассистент базы знаний в Telegram с RAG, семантическим поиском, авто-аннотацией и локальной приватностью.
>
> ✅ **100% Приватно:** работает локально на Mac/Linux (Ollama + SQLite)  
> ✅ **AI-Powered:** авто-аннотация, векторизация и RAG-ответы по вашим заметкам  
> ✅ **Telegram Mini App:** лендинг и Waitlist на Next.js 14  
> ✅ **Docker-ready:** запуск одной командой `docker compose up -d`

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/saveas_pro_bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Next.js: 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)

---

## 📦 Архитектура и возможности

| Компонент | Стек / Технологии | Назначение |
| --- | --- | --- |
| **Telegram Bot** | `aiogram 3.x`, Python 3.11+ | Сохранение заметок (`/save`), семантический поиск (`/search`), RAG-диалог (`/ask`) |
| **Web API** | `FastAPI`, `SQLModel`, `Uvicorn` | REST API для интеграций и веб-форм |
| **AI Ядро** | `Ollama` (`nomic-embed-text`, `llama3.2:1b`) | Локальная векторизация текста и генерация ответов |
| **Mini App / Web** | `Next.js 14`, `React 18`, `Tailwind CSS` | Telegram Mini App и интерфейс регистрации |
| **База данных** | `SQLite` (по умолчанию) / `pgvector` | Хранение заметок и векторных эмбеддингов |

---

## ⚡ Быстрый старт (Локально)

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/egle282/bot-core-SAB.git
cd bot-core-SAB
```

### 2. Запустите автоматическую установку

Скрипт создаст виртуальное окружение, установит зависимости и скачает модели Ollama:

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Настройте конфигурацию `.env`

Укажите ваш токен Telegram бота, полученный у [@BotFather](https://t.me/BotFather):

```bash
# Отредактируйте .env
TELEGRAM_BOT_TOKEN="123456789:ABCdef..."
```

### 4. Запустите Ollama (если еще не запущена)

```bash
ollama run llama3.2:1b
ollama pull nomic-embed-text
```

### 5. Запустите Telegram-бота

```bash
source venv/bin/activate
python backend/main.py
```

### 6. Запустите Web API (опционально)

```bash
source venv/bin/activate
uvicorn backend.api.main:app --reload --port 8000
```

---

## 🐳 Запуск через Docker Compose

Для развертывания полного стека с PostgreSQL (pgvector) и Redis:

```bash
cp .env.example .env
# укажите TELEGRAM_BOT_TOKEN в .env
docker compose up -d --build
```

---

## 💡 Основные команды Telegram-бота

- `/start` — приветствие и краткий тур по возможностям.
- `/save <текст>` — сохраняет заметку, генерирует AI-резюме и векторный эмбеддинг. Также можно переслать боту любое сообщение или фото с подписью `/save`.
- `/search <запрос>` — гибридный поиск: точное текстовое совпадение + поиск по смыслу через эмбеддинги.
- `/ask <вопрос>` — RAG-ответ искусственного интеллекта строго на базе ваших сохраненных заметок.
- `early` — генерация персонального QR-кода раннего доступа.

---

## 📁 Структура проекта

```text
├── backend/
│   ├── api/             # FastAPI сервер и маршруты
│   ├── handlers/        # Aiogram роутеры команд (/start, /save, /search, /ask, /early)
│   ├── lib/             # Интеграции (Notion, Telegram Alerts, Analytics)
│   ├── services/        # AI сервисы (summary, embeddings, RAG)
│   ├── models.py        # SQLModel модели базы данных
│   ├── main.py          # Точка входа Telegram-бота
│   └── requirements.txt # Python зависимости
├── frontend/            # Next.js 14 Mini App
├── docker-compose.yml   # Docker Compose конфигурация
├── setup.sh             # Скрипт быстрой автоматической настройки
├── .env.example         # Шаблон переменных окружения
└── ROADMAP_GITHUB_RELEASE.md # Дорожная карта разработки
```

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).
