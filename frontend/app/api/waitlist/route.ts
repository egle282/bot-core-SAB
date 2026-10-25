import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { email, name, telegram } = body;

    if (!email || typeof email !== 'string' || !email.includes('@')) {
      return NextResponse.json({ error: 'Неверный email адрес' }, { status: 400 });
    }

    // Проксируем запрос в Python FastAPI backend
    const response = await fetch(`${BACKEND_URL}/api/waitlist`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, name: name || '', telegram: telegram || '' }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || errorData.error || 'Ошибка добавления в waitlist' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (e: any) {
    console.error('[API Proxy] Ошибка при обращении к бэкенду:', e);
    return NextResponse.json(
      { error: 'Внутренняя ошибка сервера или бэкенд недоступен' },
      { status: 500 }
    );
  }
}
