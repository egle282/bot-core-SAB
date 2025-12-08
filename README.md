# 🧠 SaveAs Pro — Your AI-Powered Second Brain in Telegram

> **Сохраняйте знания → Ищите по смыслу → Спрашивайте ИИ**  
> Полный аналог @SaveAsBot с AI-усилением (RAG, семантический поиск, авто-аннотация), командной работой и early-bird монетизацией.  
> ✅ Готов к продаже (SaaS / white-label / enterprise)  
> ✅ Работает локально на Mac (Ollama + SQLite)  
> ✅ 100% open-core (AGPL-3.0)

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/saveas_pro_bot)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?logo=vercel)](https://saveas.pro)
[![License](https://img.shields.io/badge/License-AGPL--3.0-orange)](LICENSE)

---

## 🚀 Демо

| Функция | Скриншот |
|--------|----------|
| `/save` + AI-аннотация | ![save](https://saveas.pro/assets/demo-save.png) |
| `/ask` (RAG по вашим заметкам) | ![ask](https://saveas.pro/assets/demo-ask.png) |
| Telegram Mini App | ![miniapp](https://saveas.pro/assets/demo-miniapp.png) |

▶️ [Смотреть 58-секундное демо-видео](https://saveas.pro/demo.mp4)

---

## 📦 Что включено

| Компонент | Технологии | Состояние |
|----------|------------|-----------|
| **Telegram Bot** | `aiogram 3.x`, Python 3.11+ | ✅ Готов |
| **Web Backend (API)** | `FastAPI`, `SQLModel`, `pgvector` (опционально) | ✅ Готов |
| **AI-ядро** | `Ollama` (локально), `nomic-embed-text`, `llama3.2:1b` | ✅ Работает на Mac |
| **Mini App** | `Next.js 14`, `Tailwind CSS`, `Vercel` | ✅ Деплоится за 1 клик |
| **Автоматизация** | Waitlist → Notion → Telegram alert | ✅ Настроено |
| **Монетизация** | Early-bird QR, Telegram Stars | ✅ Готово |

---

## 🖥️ Быстрый старт (macOS 12.7.6)

> ✅ Проверено на **macOS 12.7.6** + **VS Code 1.85.2**

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/saveas-pro/bot-core.git
cd bot-core
