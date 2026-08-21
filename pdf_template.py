import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Cyrillic Fonts (Liberation Sans)
FONT_REGULAR = 'LiberationSans'
FONT_BOLD = 'LiberationSans-Bold'
FONT_ITALIC = 'LiberationSans-Italic'
FONT_BOLDITALIC = 'LiberationSans-BoldItalic'

pdfmetrics.registerFont(TTFont(FONT_REGULAR, '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont(FONT_ITALIC, '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'))
pdfmetrics.registerFont(TTFont(FONT_BOLDITALIC, '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf'))

def make_pdf(filename, title, topic_category, date_str, author_str, blocks):
    """
    blocks is a list of dicts/tuples describing elements:
    - ('h1', text)
    - ('h2', text)
    - ('p', text)
    - ('quote', text)
    - ('prompt', title, text)
    - ('list', [items])
    - ('card', title, content_dict) # site_name, site_url, price, concept, advantages
    - ('faq', [(q, a), ...])
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=40,
        bottomMargin=46
    )

    # Styles
    styles = getSampleStyleSheet()

    # Palette
    PRIMARY = colors.HexColor('#1E293B')   # Dark Slate
    ACCENT = colors.HexColor('#2563EB')    # Electric Blue
    ACCENT_LIGHT = colors.HexColor('#EFF6FF') # Soft Blue Tint
    BG_CARD = colors.HexColor('#F8FAFC')   # Light Gray
    BORDER_COLOR = colors.HexColor('#E2E8F0')
    TEXT_MAIN = colors.HexColor('#334155')
    MUTED = colors.HexColor('#64748B')
    PROMPT_BG = colors.HexColor('#F1F5F9')
    PROMPT_BORDER = colors.HexColor('#94A3B8')

    title_style = ParagraphStyle(
        'DocTitle',
        fontName=FONT_BOLD,
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=12,
        textColor=MUTED,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        fontName=FONT_BOLD,
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        fontName=FONT_BOLD,
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    p_style = ParagraphStyle(
        'P',
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=14,
        textColor=TEXT_MAIN,
        spaceAfter=8
    )

    quote_style = ParagraphStyle(
        'Quote',
        fontName=FONT_ITALIC,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=4,
        spaceAfter=6
    )

    list_item_style = ParagraphStyle(
        'ListItem',
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13.5,
        textColor=TEXT_MAIN,
        leftIndent=15,
        spaceAfter=4
    )

    prompt_title_style = ParagraphStyle(
        'PromptTitle',
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#475569')
    )

    prompt_body_style = ParagraphStyle(
        'PromptBody',
        fontName=FONT_ITALIC,
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    card_label_style = ParagraphStyle(
        'CardLabel',
        fontName=FONT_BOLD,
        fontSize=9,
        leading=12.5,
        textColor=PRIMARY
    )

    card_val_style = ParagraphStyle(
        'CardVal',
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13,
        textColor=TEXT_MAIN
    )

    faq_q_style = ParagraphStyle(
        'FaqQ',
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=13.5,
        textColor=ACCENT,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    faq_a_style = ParagraphStyle(
        'FaqA',
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13,
        textColor=TEXT_MAIN,
        spaceAfter=6
    )

    story = []

    # Title & Header
    story.append(Paragraph(f"<font color='{ACCENT.hexval()}'><b>[2026 SEO EXPERT & USER REVIEW]</b></font><br/>{title}", title_style))
    story.append(Paragraph(f"<b>Тематика:</b> {topic_category} | <b>Автор:</b> {author_str} (10+ лет в Event) | <b>Дата:</b> {date_str}", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceBefore=0, spaceAfter=10))

    for block in blocks:
        b_type = block[0]
        if b_type == 'h1':
            story.append(Paragraph(block[1], h1_style))
        elif b_type == 'h2':
            story.append(Paragraph(block[1], h2_style))
        elif b_type == 'p':
            story.append(Paragraph(block[1], p_style))
        elif b_type == 'quote':
            # Quote callout table
            q_p = Paragraph(f"« {block[1]} »", quote_style)
            t = Table([[q_p]], colWidths=[520])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), ACCENT_LIGHT),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LINELEFT', (0,0), (0,0), 3.5, ACCENT),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
        elif b_type == 'prompt':
            p_title = Paragraph(f"<b>🎨 AI IMAGE PROMPT (Midjourney v6 / SORA 2026):</b> {block[1]}", prompt_title_style)
            p_body = Paragraph(block[2], prompt_body_style)
            t = Table([[p_title], [p_body]], colWidths=[520])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), PROMPT_BG),
                ('BOX', (0,0), (-1,-1), 0.5, PROMPT_BORDER),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
        elif b_type == 'list':
            for item in block[1]:
                story.append(Paragraph(f"• {item}", list_item_style))
            story.append(Spacer(1, 4))
        elif b_type == 'card':
            # Content dict: site_name, site_url, price, concept, advantages
            c_data = block[1]
            rows = [
                [Paragraph("<b>Сервис / Площадка:</b>", card_label_style), Paragraph(f"<b><font color='{ACCENT.hexval()}'>{c_data['site_name']}</font></b> (<a href='{c_data['site_url']}'>{c_data['site_url']}</a>)", card_val_style)],
                [Paragraph("<b>Основная задумка:</b>", card_label_style), Paragraph(c_data['concept'], card_val_style)],
                [Paragraph("<b>Ориентир по цене:</b>", card_label_style), Paragraph(c_data['price'], card_val_style)],
            ]

            adv_text = "<br/>".join([f"✓ {adv}" for adv in c_data['advantages']])
            rows.append([Paragraph("<b>Ключевые плюсы:</b>", card_label_style), Paragraph(adv_text, card_val_style)])

            t = Table(rows, colWidths=[120, 400])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
                ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
                ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(KeepTogether([t, Spacer(1, 8)]))
        elif b_type == 'faq':
            story.append(Paragraph("<b>Часто задаваемые вопросы (SEO FAQ 2026)</b>", h2_style))
            for q, a in block[1]:
                story.append(Paragraph(f"<b>В: {q}</b>", faq_q_style))
                story.append(Paragraph(f"<b>О:</b> {a}", faq_a_style))
            story.append(Spacer(1, 6))

    doc.build(story)

if __name__ == '__main__':
    test_blocks = [
        ('h1', 'Личный опыт: Как мы организовали идеальный ивент в 2026 году'),
        ('p', 'В этом детальном разборе я поделюсь своим личным 10-летним опытом проведения мероприятий любого масштаба.'),
        ('quote', 'Главный секрет 2026 года — отказаться от банальных ресторанов в пользу трансформируемых лофтов с иммерсивным шоу.'),
        ('prompt', 'Главный зал лофта', 'Cinematic photo, modern loft event hall in Moscow, high ceilings, neon atmospheric lighting, happy people celebrating, 8k resolution, photorealistic, --ar 16:9'),
        ('h2', 'Обзор рекомендуемой площадки'),
        ('card', {
            'site_name': 'Event Pandora',
            'site_url': 'https://eventpandora.ru/',
            'price': 'от 3 500 руб/час в будни, от 5 000 руб/час в выходные',
            'concept': 'Универсальный технологичный лофт с трансформируемой зоной и встроенным мультимедиа.',
            'advantages': [
                'Собственная звуковая и световая система концертного уровня',
                'Без пробкового сбора (можно со своей едой и напитками)',
                'Удобная локация в центре с парковкой'
            ]
        }),
        ('h2', 'Ключевые этапы подбора'),
        ('list', [
            'Определение формата и тайминга',
            'Бронирование локации за 2-3 недели',
            'Согласование интерактивной программы и кейтеринга'
        ]),
        ('faq', [
            ('Сколько стоит аренда лофта в Москве?', 'Средняя стоимость аренды варьируется от 2 500 до 8 000 руб/час в зависимости от формата и дня недели.'),
            ('Можно ли приносить свой алкоголь?', 'Да, на большинстве площадок, таких как Pandora и Memories Loft, нет пробкового сбора.')
        ])
    ]
    make_pdf("test_out.pdf", "Тестовая статья для SEO 2026", "Тестирование", "Декабрь 2026", "Алексей Ивент-Эксперт", test_blocks)
    print("test_out.pdf successfully created!")
