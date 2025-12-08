// frontend/types/backend.d.ts
declare module '../../../backend/lib/notion_client' {
  export function add_to_waitlist(email: string, name?: string, telegram?: string): Promise<string | null>;
}
declare module '../../../backend/lib/telegram_alert' {
  export function send_alert_to_admin(text: string): Promise<void>;
}
