#!/usr/bin/env bash
# ==============================================================================
# SaveAs Pro — Setup & Quickstart Script (macOS / Linux)
# ==============================================================================
set -euo pipefail

echo "🧠 === SaveAs Pro Initial Setup ==="

# 1. Проверка .env файла
if [ ! -f ".env" ]; then
    echo "📋 Создаём .env из .env.example..."
    cp .env.example .env
    echo "⚠️ Пожалуйста, настройте TELEGRAM_BOT_TOKEN в файле .env!"
else
    echo "✅ Файл .env уже существует."
fi

# 2. Проверка Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "❌ Python не найден. Пожалуйста, установите Python 3.11+"
    exit 1
fi

echo "🐍 Используем Python: $($PYTHON_BIN --version)"

# 3. Настройка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения venv..."
    $PYTHON_BIN -m venv venv
fi

echo "📦 Активация окружения и установка Python зависимостей..."
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# 4. Проверка моделей Ollama
if command -v ollama >/dev/null 2>&1; then
    echo "🦙 Ollama обнаружена. Проверка и загрузка моделей..."
    ollama pull nomic-embed-text || echo "⚠️ Не удалось загрузить nomic-embed-text, проверьте запущен ли ollama serve"
    ollama pull llama3.2:1b || echo "⚠️ Не удалось загрузить llama3.2:1b, проверьте запущен ли ollama serve"
else
    echo "ℹ️ Ollama не найдена. Если вы планируете локальный AI, установите с https://ollama.ai"
fi

# 5. Настройка Frontend (при наличии Node.js)
if command -v npm >/dev/null 2>&1; then
    if [ -d "frontend" ]; then
        echo "⚛️ Установка зависимостей фронтенда..."
        cd frontend && npm install && cd ..
    fi
fi

echo "=================================================="
echo "🎉 Настройка завершена успешно!"
echo "Для запуска бота:"
echo "  source venv/bin/activate"
echo "  python backend/main.py"
echo ""
echo "Для запуска веб-API:"
echo "  source venv/bin/activate"
echo "  uvicorn backend.api.main:app --reload --port 8000"
echo "=================================================="
