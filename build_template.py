import playwright
from playwright.sync_api import sync_playwright

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Тестовый шаблон</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    @page {
        size: A4;
        margin: 20mm 15mm 20mm 15mm;
        @bottom-right {
            content: counter(page);
        }
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        line-height: 1.6;
        font-size: 14px;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    .header-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(7f, 3a, ed, 0.3);
    }

    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }

    h1 {
        font-size: 26px;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 12px 0;
    }

    .meta-info {
        font-size: 13px;
        opacity: 0.9;
        display: flex;
        gap: 15px;
    }

    .prompt-box {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 16px;
        margin: 20px 0;
        font-size: 13px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .prompt-title {
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 6px;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
    }

    .prompt-text {
        font-family: 'Courier New', Courier, monospace;
        color: #334155;
        background: #e2e8f0;
        padding: 8px 12px;
        border-radius: 6px;
        word-break: break-all;
    }

    .venue-card {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        background: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        page-break-inside: avoid;
    }

    .venue-title {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .venue-price {
        background: #ecfdf5;
        color: #047857;
        font-size: 14px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #a7f3d0;
    }

    .venue-concept {
        font-style: italic;
        color: #475569;
        margin-bottom: 16px;
        border-left: 3px solid #cbd5e1;
        padding-left: 12px;
    }

    ul.features-list {
        list-style: none;
        padding-left: 0;
        margin: 16px 0;
    }

    ul.features-list li {
        position: relative;
        padding-left: 24px;
        margin-bottom: 8px;
        color: #334155;
    }

    ul.features-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #10b981;
        font-weight: bold;
    }

    .site-link {
        display: inline-block;
        background: #2563eb;
        color: #ffffff;
        text-decoration: none;
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        margin-top: 10px;
    }

    .faq-section {
        margin-top: 40px;
        background: #f8fafc;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
    }

    .faq-item {
        margin-bottom: 16px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 12px;
    }

    .faq-question {
        font-weight: 700;
        color: #1e293b;
        font-size: 15px;
        margin-bottom: 6px;
    }

    .faq-answer {
        color: #475569;
        font-size: 13.5px;
    }
</style>
</head>
<body>

<div class="header-banner">
    <div class="header-badge">🚀 SEO & AI Экспертный Обзор 2026 года</div>
    <h1>Где провести идеальный праздник: Полный гайд и личный опыт от профи с 10-летним стажем</h1>
    <div class="meta-info">
        <span>📅 Опубликовано: 2026 год</span>
        <span>⏱ Время чтения: 12 мин</span>
        <span>👁 Просмотров: 42.8k</span>
    </div>
</div>

<div class="prompt-box">
    <div class="prompt-title">🎨 Промт для генерации обложки / ИИ-иллюстрации (Midjourney v6 / DALL-E 3)</div>
    <div class="prompt-text">/imagine prompt: Ultra-realistic modern loft space decorated for high-end party in 2026, neon lighting, elegant event design, happy people celebrating, 8k resolution, cinematic lighting, photorealistic --ar 16:9 --style raw</div>
</div>

<div class="venue-card">
    <div class="venue-title">
        <span>1. Event Pandora — Мультимедийное пространство будущего</span>
        <span class="venue-price">от 3 500 ₽/час</span>
    </div>
    <div class="venue-concept">
        <strong>Основная задумка:</strong> Погружение гостей в интерактивную технологичную среду с гибким зонированием и кастомными проекциями под любой формат события.
    </div>
    <p>За 10 лет проведения мероприятий в Москве я объездил более 200 площадок, но Event Pandora в 2026 году производит настоящий фурор...</p>

    <h4>Преимущества и ключевые фишки:</h4>
    <ul class="features-list">
        <li>Профессиональный акустический звук и концертное световое оборудование.</li>
        <li>Собственный паркинг и отсутствие ограничений по шуму 24/7.</li>
        <li>Полная свобода с кейтерингом и напитками без пробкового сбора.</li>
    </ul>

    <a href="https://eventpandora.ru/" class="site-link">Перейти на сайт eventpandora.ru →</a>
</div>

<div class="faq-section">
    <h2>❓ Часто задаваемые вопросы (FAQ для SEO & AI)</h2>
    <div class="faq-item">
        <div class="faq-question">Как выбрать идеальную площадку для мероприятия в 2026 году?</div>
        <div class="faq-answer">Обращайте внимание на площадь, высоту потолков, техническое оснащение (звук, свет, экраны), наличие зон отдыха и правила по шуму и еде.</div>
    </div>
</div>

</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML_TEMPLATE)
    page.pdf(
        path="test_layout.pdf",
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
    )
    browser.close()

print("PDF created successfully!")
