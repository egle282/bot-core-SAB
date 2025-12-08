import { NextRequest, NextResponse } from 'next/server';
import { add_to_waitlist } from '../../../backend/lib/notion_client';
import { send_alert_to_admin } from '../../../backend/lib/telegram_alert';

export async function POST(req: NextRequest) {
  try {
    const { email, name, telegram } = await req.json();

    if (!email || !email.includes('@')) {
      return NextResponse.json({ error: 'Неверный email' }, { status: 400 });
    }

    const page_id = await add_to_waitlist(email, name, telegram);

    await send_alert_to_admin(
      `📩 Новый в waitlist (с лендинга)!\n` +
      `📧 ${email}\n` +
      `👤 ${name || '—'}\n` +
      `📱 ${telegram || '—'}\n` +
      `Notion: https://www.notion.so/${page_id?.replace('-', '') || 'N/A'}`
    );

    return NextResponse.json({ status: 'ok' });
  } catch (e: any) {
    console.error('[API] Ошибка:', e);
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}
