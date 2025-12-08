'use client';

import { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, name }),
      });
      
      if (res.ok) {
        setStatus("success");
        setEmail("");
        setName("");
      } else {
        throw new Error("Ошибка");
      }
    } catch (e) {
      setStatus("error");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-16">
        <header className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            SaveAs Pro
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Ваш ИИ-ассистент знаний — прямо в Telegram. Сохраняйте, ищите по смыслу, спрашивайте.
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <div className="text-6xl mb-6">🧠</div>
            <h2 className="text-3xl font-bold mb-6">Получите ранний доступ</h2>
            
            {status === "success" ? (
              <div className="bg-green-50 text-green-700 p-4 rounded-lg mb-6">
                ✅ Спасибо! Проверьте почту — инструкция уже в пути.
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Ваш email"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  required
                />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Имя (опционально)"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <button
                  type="submit"
                  disabled={status === "loading"}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition disabled:opacity-75"
                >
                  {status === "loading" ? "Отправка..." : "В waitlist →"}
                </button>
              </form>
            )}

            <p className="text-gray-500 text-sm mt-6">
              Первые 100 получат **пожизненную скидку 30%**. Без спама.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: "🔖", title: "Сохраняйте всё", desc: "Ссылки, текст, фото, PDF — одним кликом" },
              { icon: "🔍", title: "Ищите по смыслу", desc: "Не «LLM», а «как работают языковые модели»" },
              { icon: "🤖", title: "Спрашивайте ИИ", desc: "/ask Что я думал про RAG в прошлом месяце?" }
            ].map((item, i) => (
              <div key={i} className="text-center">
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="font-bold text-lg mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
