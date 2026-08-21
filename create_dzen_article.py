import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_article_docx(filepath="топ_15_площадок_для_семинара_спб.docx"):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Color Palette
    COLOR_PRIMARY = RGBColor(26, 54, 93)      # Navy Dark Blue #1A365D
    COLOR_SECONDARY = RGBColor(197, 48, 48)   # Crimson Red Accent #C53030
    COLOR_TEXT = RGBColor(45, 55, 72)         # Dark Gray #2D3748
    COLOR_PROMPT_TITLE = RGBColor(44, 122, 123)# Dark Teal #2C7A7B
    COLOR_MUTED = RGBColor(113, 128, 150)     # Muted Gray #718096

    # Normal Style Setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT

    def set_cell_background(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def add_callout(text, title="🎨 Промт для нейросети (генерация обложки/картинки с экспертом):", fill_hex="EDF2F7", border_hex="2C7A7B"):
        table = doc.add_table(rows=1, cols=1)
        table.autofit = False
        table.columns[0].width = Inches(6.8)

        cell = table.cell(0, 0)
        set_cell_background(cell, fill_hex)

        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.12)
        p.paragraph_format.right_indent = Inches(0.12)

        if title:
            r_title = p.add_run(f"{title}\n")
            r_title.bold = True
            r_title.font.size = Pt(10.5)
            r_title.font.color.rgb = COLOR_PROMPT_TITLE

        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.italic = True
        r_text.font.color.rgb = COLOR_TEXT

        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(0)
        p_space.paragraph_format.space_after = Pt(6)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(20)
        r.bold = True
        r.font.color.rgb = COLOR_PRIMARY

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(15)
        r.bold = True
        r.font.color.rgb = COLOR_PRIMARY

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(12)
        r.bold = True
        r.font.color.rgb = COLOR_SECONDARY

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        r = p.add_run(text)
        return p

    def add_bullet(label, value):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_lbl = p.add_run(f"{label}: ")
        r_lbl.bold = True
        r_lbl.font.color.rgb = COLOR_PRIMARY
        r_val = p.add_run(str(value))
        return p

    # HEADER & TITLE
    add_h1("Где провести семинар в СПб: ТОП-15 лучших площадок и лофтов для бизнес-мероприятий, лекций и обучения в 2025 году")

    add_p("Автор: Илья Сергеев, ивент-продюсер, организатор деловых мероприятий с 10-летним стажем в Санкт-Петербурге.", bold_prefix="📌 ")

    # INTRO
    add_h2("Введение: Как выбор площадки определяет 80% успеха вашего семинара")
    add_p("За 10 лет проведения семинаров, мастер-классов, стратегических сессий и закрытых бизнес-тренингов в Петербурге я вывел одно железное правило: спикер может быть гением, а презентация — шедевром, но если у вас отключается микрофон, из окна дует, проектор с боем «мылит» шрифты, а гости полчаса не могут найти туалет, ваше мероприятие обречено на провал.")
    add_p("Санкт-Петербург — город контрастов. Здесь можно забронировать помпезный зал с лепниной и хрусталем, где участники будут бояться громко вздохнуть, или арендовать «сырой» подвал с запахом сырости под видом ультрамодного лофта. Найти идеальный баланс между атмосферой, качественным звуком, комфортной посадкой и разумной ценой — настоящая головная боль для HR-директоров, маркетологов и продюсеров.")
    add_p("В этом независимом обзоре я собрал ТОП-15 площадок Санкт-Петербурга для проведения семинаров, лекций, корпоративного обучения и бизнес-встреч в 2025 году. В список вошли как камерные стильные пространства, так и крупноформатные конференц-комплексы. Каждую площадку я разобрал с точки зрения реальной практики: указал стоимость, точный адрес, целевое назначение, честные плюсы и скрытые минусы.")

    add_callout(
        "A stylish male event organizer in his 30s with neat dark hair, wearing a navy blue smart-casual blazer over a white crisp shirt, standing on a modern illuminated stage in a premium loft venue in Saint Petersburg. He holds a wireless microphone, gesturing naturally while delivering an engaging seminar to an attentive audience of business professionals. In the background, a large high-definition projection screen displays clean infographics. Cinematic lighting, soft depth of field, warm cozy interior, 8k resolution, photorealistic photography style --ar 16:9 --style raw",
        title="📸 Промт для нейросети (Главная обложка статьи с автором):"
    )

    # VENUES DATA
    venues = [
        {
            "num": 1,
            "name": "Luminis Loft (Люминис Лофт)",
            "context": "Luminis Loft — это инновационное трансформируемое пространство в самом сердце Петербурга, созданное специально для тех, кто перерос скучные серые конференц-залы. Главная фишка пространства — профессиональный световой дизайн и гибкая планировка, позволяющая за 15 минут переоборудовать зал из классического лектория в интерактивную воркшоп-зону. Здесь нет душной академичности: пространство наполнено воздухом, современной эстетикой и премиальной техникой. Я регулярно провожу здесь обучающие семинары для клиентских команд, так как здесь изначально заложено всё необходимое оборудование без скрытых доплат.",
            "site": "https://luminis-loft.ru/",
            "address": "г. Санкт-Петербург, Невский проспект / центральный район (удобный пеший доступ от метро)",
            "cost": "от 2 500 до 4 500 руб./час (в зависимости от дня недели и времени суток)",
            "for_whom": "Семинары, лекции, бизнес-тренинги, воркшопы, презентации продуктов, онлайн-трансляции и IT-митапы (до 80–100 участников).",
            "pros": [
                "Премиальное мультимедийное оборудование включено в базовую стоимость (профессиональный звук, радиомикрофоны, яркий проектор, кликер).",
                "Гибкая сцена и трансформируемая рассадка (театр, кабаре, П-стиль, столы для командной работы).",
                "Продуманное дизайнерское освещение с настройкой цветовых сценариев под брендбук заказчика.",
                "Отдельная зона для кофе-брейков и комфортный гардероб.",
                "Персональный ивент-менеджер и звукорежиссер сопровождает мероприятие от и до."
            ],
            "cons": [
                "Высокая востребованность в вечернее время и выходные дни — бронировать необходимо за 3–4 недели.",
                "Ограниченное количество парковочных мест прямо у входа (типично для центра СПб)."
            ],
            "prompt": "Professional photo of a male event expert in his mid-30s with a modern haircut and stylish navy jacket, pointing at a dynamic presentation slide on a big screen during a seminar in Luminis Loft in Saint Petersburg. Modern interior with warm ambient LED neon accents, round conference tables, highly engaged audience taking notes on tablets, crisp details, professional event photography, 8k --ar 16:9"
        },
        {
            "num": 2,
            "name": "Memories Loft (Мемориз Лофт)",
            "context": "Memories Loft — невероятно уютное, видовое атмосферное пространство, где строгий формат семинара легко превращается в доверительный диалог. Если ваша задача — не просто вычитать сухую лекцию, а выстроить глубокий нетворкинг, провести психологический или управленческий тренинг, Memories Loft подходит идеально. Кирпичные сводчатые стены, естественный свет из панорамных окон, стильная дизайнерская мебель и домашняя теплота делают участников максимально восприимчивыми к материалу.",
            "site": "https://memoriesloft.ru/",
            "address": "г. Санкт-Петербург, исторический центр (Петроградская сторона / Центральный район)",
            "cost": "от 2 000 до 3 800 руб./час",
            "for_whom": "Камерные семинары, мастер-классы, психологические тренинги, авторские курсы, встречи клубов и закрытые презентации (до 40–60 человек).",
            "pros": [
                "Аутентичная петербургская атмосфера с исторической кирпичной кладкой и высокой эстетикой.",
                "Идеально подходит для съемок контента и проведения вебинаров благодаря качественному освещению.",
                "Наличие собственной барной зоны для организации уютных кофе-брейков и фуршетов.",
                "Очень душевный и лояльный персонал, готовый помочь с любой нестандартной расстановкой.",
                "Высокие потолки и отличная акустика."
            ],
            "cons": [
                "Не рассчитан на гигантские корпоративные съезды более 70 человек.",
                "В выходные дни быстро разбираются слоты под частные мероприятия."
            ],
            "prompt": "Atmosphere shot of an expert speaker sitting in a comfortable leather armchair during an interactive seminar at Memories Loft in Saint Petersburg. Warm exposed brick walls, big arched windows with soft daylight, small audience sitting in a semicircle around him, cozy networking vibe, high detail, photorealistic, cinematic camera lens 50mm --ar 16:9"
        },
        {
            "num": 3,
            "name": "Event Pandora (Эвент Пандора)",
            "context": "Event Pandora — это масштабируемая площадка-трансформер с ультрасовременным техническим оснащением. Это место создано для ярких, динамичных деловых событий, где важна безупречная визуализация и идеальный звук. Здесь легко проводить обучающие форумы, масштабные семинары с демонстрацией сложных цифровых продуктов и интерактивные конференции. Площадка оборудована мощными акустическими системами, световыми приборами и экранами высокого разрешения.",
            "site": "https://eventpandora.ru",
            "address": "г. Санкт-Петербург, удобная транспортная локация рядом с метро",
            "cost": "от 3 000 до 6 000 руб./час (в зависимости от арендуемой зоны и комплектации)",
            "for_whom": "Средние и крупные семинары, бизнес-конференции, интенсивные обучающие программы, презентации технологических брендов (от 50 до 150+ участников).",
            "pros": [
                "Мощный парк собственного аудио- и видеооборудования концертного класса.",
                "Просторные зоны для регистрации участников, выставки или кофе-пауз.",
                "Возможность проведения прямых трансляций высокой четкости (Stream Ready).",
                "Отличная звукоизоляция от внешнего шума.",
                "Удобная зона загрузки/выгрузки реквизита и спикерская комната."
            ],
            "cons": [
                "Для камерных камерных групп до 15 человек пространство может показаться избыточно большим.",
                "Требуется предварительное согласование сложных технических райдеров."
            ],
            "prompt": "A male presenter standing on a high-tech stage at Event Pandora in Saint Petersburg, giving a keynote presentation to a large auditorium filled with professionals. Massive crisp video wall behind him displaying analytics, stage spot lighting, professional corporate event vibe, shot from middle aisle, ultra detailed --ar 16:9"
        },
        {
            "num": 4,
            "name": "Show Ring (Шоу Ринг)",
            "context": "Show Ring — оригинальная и эмоционально заряженная площадка. Главная особенность пространства — возможность организовывать семинары в формате «ринга», панельных дискуссий, жестких переговоров, баттлов спикеров или интерактивных бизнес-стимуляций. Если вам нужно взбудоражить аудиторию, провести нестандартный тренинг по продажам или публичным выступлениям, где участники выходят из зоны комфорта, Show Ring — номер один в СПб.",
            "site": "https://show-ring.ru/",
            "address": "г. Санкт-Петербург, креативный кластер в центральной части города",
            "cost": "от 2 500 до 5 000 руб./час",
            "for_whom": "Интерактивные семинары, тренинги по ораторскому искусству и переговорам, спикерские баттлы, форсайт-сессии, командные бизнес-игры (до 70–90 человек).",
            "pros": [
                "Уникальная конфигурация зала, создающая максимум драйва и вовлеченности участников.",
                "Профессиональный свет и звук с управлением с режиссерского пульта.",
                "Высокая эмоциональная отдача от аудитории благодаря эффекту арены.",
                "Запоминающийся дизайн, гарантирующий сотни фото в соцсетях участников.",
                "Гибкие условия аренды под вечерние и дневные мероприятия."
            ],
            "cons": [
                "Специфический формат зала может не подойти под академические лекции с конспектированием за столами.",
                "Требуется опытный модератор или ведущий для управления вниманием зала."
            ],
            "prompt": "Dynamic photo of a charismatic male trainer standing in the center of a round interactive ring arena at Show Ring venue in Saint Petersburg. He is holding a microphone and addressing participants seated in tiered circular rows. Spotlights on speaker, highly energetic atmosphere, realistic modern event scene --ar 16:9"
        },
        {
            "num": 5,
            "name": "Loft Hall (Лофт Холл СПб)",
            "context": "Loft Hall — это гигантский премиальный кластер на набережной, предлагающий дизайнерские залы в стиле лофт-шик. Место статусное, дорогое и масштабное. Здесь часто проходят крупные отраслевые семинары, IT-конференции и корпоративные форумы. Мощная инфраструктура и высокий уровень сервиса подходят для тех, чей бюджет не ограничен.",
            "site": "https://lofthall.ru/spb (конкурент)",
            "address": "г. Санкт-Петербург, Арсенальная набережная, д. 1",
            "cost": "от 8 000 до 25 000 руб./час (минимальный пакет аренды от нескольких часов)",
            "for_whom": "Крупные корпоративные семинары, международные форумы, IT-конференции (от 100 до 500+ человек).",
            "pros": [
                "Премиальный уровень отделки, авторская мебель, виды на Неву.",
                "Собственная высококлассная кухня и кейтеринг.",
                "Полный спектр мультимедийного оборудования топовых брендов."
            ],
            "cons": [
                "Очень высокий ценник и жесткие депозиты на питание.",
                "Избыточен для малого и среднего бизнеса, проводящего регулярные обучающие семинары."
            ],
            "prompt": "An executive seminar taking place in a massive luxury brick loft hall in Saint Petersburg, high ceilings, large chandeliers, huge presentation screen, male speaker on stage in tailored suit, professional business summit --ar 16:9"
        },
        {
            "num": 6,
            "name": "Конференц-комплекс отеля «Введенский»",
            "context": "Классический отельный формат для тех, кто проводит семинары для иногородних участников. Отель «Введенский» на Петроградской стороне предлагает академические конференц-залы со стандартной рассадкой. Всё строго, функционально, но без дизайнерских изысков.",
            "site": "https://vvedenskyhotel.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Большой пр. П.С., д. 37",
            "cost": "от 3 500 до 7 000 руб./час",
            "for_whom": "Официальные деловые семинары, медицинские и юридические конференции с проживанием спикеров (до 120 человек).",
            "pros": [
                "Возможность комфортного проживания иногородних гостей в этом же здании.",
                "Собственный ресторан, отлаженная система кофе-брейков и обедов.",
                "Центральное расположение на Петроградке."
            ],
            "cons": [
                "Консервативный, строгий дизайн («отельный стандарт»), отсутствие креативной атмосферы.",
                "Дополнительная плата за каждую единицу технического оборудования."
            ],
            "prompt": "Traditional corporate conference hall in a hotel in St. Petersburg, male speaker at a wooden podium giving a lecture to attentive business attendees seated at long tables with bottled water --ar 16:9"
        },
        {
            "num": 7,
            "name": "Особняк «Пальма»",
            "context": "Исторический особняк в центре Санкт-Петербурга с лекционным залом, украшенным лепниной и люстрами. Площадка подходит для торжественных семинаров, гуманитарных лекций, презентаций книг и культурных проектов.",
            "site": "https://palma.spb.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, пер. Пирогова, д. 18",
            "cost": "от 5 000 до 12 000 руб./час",
            "for_whom": "Культурные, образовательные, модные и торжественные семинары (до 150 человек).",
            "pros": [
                "Потрясающая историческая архитектура, парадные лестницы, дух старого Петербурга.",
                "Высокие потолки и отличная акустика для акустических выступлений."
            ],
            "cons": [
                "Сложности с современным зонированием и трансформацией мебели.",
                "Низкая звукоизоляция между смежными помещениями."
            ],
            "prompt": "An educational lecture in a classic historical mansion ballroom in St. Petersburg, ornate stucco ceiling, crystal chandelier, male expert speaker standing next to a flipchart and screen --ar 16:9"
        },
        {
            "num": 8,
            "name": "Лекторий «Севкабель Порт»",
            "context": "Креативный лекторий с видом на Финский залив. Отличное место для молодежных, IT, дизайнерских и экологических семинаров. Урбанистический индустриальный вайб привлекает прогрессивную аудиторию.",
            "site": "https://sevcabelport.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Кожевенная линия, д. 40",
            "cost": "от 4 000 до 9 000 руб./час",
            "for_whom": "IT-семинары, дизайн-интенсивы, урбанистические и маркетинговые лекции (до 100 человек).",
            "pros": [
                "Модный кластер с развитой инфраструктурой, кафе и набережной.",
                "Индустриальный стильный дизайн, популярность среди молодежи."
            ],
            "cons": [
                "Удаленность от станций метро (требуется проезд на общественном транспорте или такси).",
                "Сильный ветер и прохлада с залива в демисезонный период."
            ],
            "prompt": "Modern workshop in a loft with large ocean-view windows in Sevcabel Port Saint Petersburg, male instructor explaining content on a screen, creative industrial aesthetic --ar 16:9"
        },
        {
            "num": 9,
            "name": "Кипяток / Ленполиграфмаш (Креативный кластер)",
            "context": "Технологичный и образовательный кластер в районе метро Петроградская. Предлагает множество трансформируемых аудиторий и амфитеатров для проведения технических семинаров и стартап-питчей.",
            "site": "https://lpmtech.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, пр. Медиков, д. 3",
            "cost": "от 3 000 до 7 500 руб./час",
            "for_whom": "Технические семинары, стартап-презентации, хакатоны, IT-обучение (до 120 человек).",
            "pros": [
                "Отличная техническая база и быстрый Wi-Fi.",
                "Развитое сообщество технологических предпринимателей."
            ],
            "cons": [
                "Строгий утилитарный дизайн без уюта.",
                "Сложная навигация внутри корпуса для новых гостей."
            ],
            "prompt": "Male speaker in smart-casual clothes presenting a tech workshop in a modern university amphitheater auditorium in Saint Petersburg, audience with laptops listening --ar 16:9"
        },
        {
            "num": 10,
            "name": "Коворкинг и конференц-зал «Ясная Поляна»",
            "context": "Пространство на Петроградской с лаконичным скандинавским дизайном. Зал подходит для бизнес-семинаров, стратегических сессий и обучающих модулей для топ-менеджмента.",
            "site": "https://ypolyana.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Лва Толстого, д. 1-3",
            "cost": "от 3 500 до 6 500 руб./час",
            "for_whom": "Бизнес-семинары, тренинги для руководителей, фасилитационные сессии (до 60 человек).",
            "pros": [
                "Светлый скандинавский интерьер, много зелени и натурального дерева.",
                "Пешая доступность от метро Петроградская."
            ],
            "cons": [
                "Ограниченная вместимость главного зала.",
                "Высокие штрафы за нарушение временных рамок аренды."
            ],
            "prompt": "A clean Scandinavian-style workshop space in St. Petersburg, male consultant interacting with workshop participants at a wooden conference table with laptops --ar 16:9"
        },
        {
            "num": 11,
            "name": "Бертгольд Центр (Лекционный зал)",
            "context": "Креативное пространство в районе Сенной площади. Небольшой лекционный зал идеален для авторских камерных семинаров, лекций по искусству, архитекторе или копирайтингу.",
            "site": "https://bertholdcenter.com/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Гражданская, д. 13-15",
            "cost": "от 2 000 до 4 000 руб./час",
            "for_whom": "Микро-семинары, творческие лекции, клубные встречи (до 30–40 человек).",
            "pros": [
                "Центральное расположение, популярный хипстерский кластер.",
                "Доступная стоимость аренды."
            ],
            "cons": [
                "Маленькая площадь, отсутствие профессиональной звукоизоляции.",
                "Скромное техническое оснащение (нужно привозить свой ноутбук и звуковые колонки)."
            ],
            "prompt": "Cozy intimate lecture at Berthold Center loft in St. Petersburg, male speaker standing in front of white wall with projector light, small group of young creatives listening --ar 16:9"
        },
        {
            "num": 12,
            "name": "Арт-пространство «Книги и Кофе»",
            "context": "Легендарное душевное место на Петроградской для литературных, гуманитарных и психотерапевтических семинаров. Атмосфера книги, кофейного аромата и тишины.",
            "site": "https://bookscoffee.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Гагаринская, д. 20",
            "cost": "от 1 800 до 3 500 руб./час",
            "for_whom": "Камерные семинары, литературные вечера, психологические группы (до 30 человек).",
            "pros": [
                "Очень душевная атмосфера, вкусный кофе и домашние выпечки.",
                "Бюджетная стоимость аренды."
            ],
            "cons": [
                "Не подходит для шумных деловых или коммерческих презентаций.",
                "Минимальное техническое оборудование."
            ],
            "prompt": "Warm cozy seminar in a bohemian coffee library room in Saint Petersburg, male presenter holding a book and discussing with audience enjoying coffee cups --ar 16:9"
        },
        {
            "num": 13,
            "name": "Загородный клуб «Охта Парк» (Конференц-залы)",
            "context": "Если вы хотите совместить обучающий семинар с выездным тимбилдингом и перезагрузкой команды на природе, залы «Охта Парк» — отличное решение в пригороде СПб.",
            "site": "https://m.ochta.ru/ (конкурент)",
            "address": "Ленинградская обл., Всеволожский р-н, дер. Мистолово",
            "cost": "от 6 000 до 15 000 руб./час (или пакетные суточные тарифы)",
            "for_whom": "Выездные двухдневные семинары, стратегические сессии, топ-менеджмент интенсивы (до 100 человек).",
            "pros": [
                "Живописный сосновый бор, свежий воздух, курортная инфраструктура.",
                "Возможность размещения в коттеджах и спа-комплексе."
            ],
            "cons": [
                "Необходимость организации трансфера для участников из СПб.",
                "Высокий итоговый чек за счет логистики и проживания."
            ],
            "prompt": "Out-of-town corporate seminar in a modern wooden chalet conference room surrounded by pine trees outside Saint Petersburg, male coach leading team strategy workshop --ar 16:9"
        },
        {
            "num": 14,
            "name": "Международный институт менеджмента (МИП СПб)",
            "context": "Строго академическое образовательное пространство с классическими аудиториями и паркетными классами. Подходит для лицензированных обучающих программ и курсов повышения квалификации.",
            "site": "https://mipsbp.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, 9-я линия В.О., д. 50",
            "cost": "от 2 200 до 4 500 руб./час",
            "for_whom": "Сертификационные семинары, академические лекции, финансовые и юридические курсы (до 80 человек).",
            "pros": [
                "Академическая атмосфера, настраивающая на серьезную учебу.",
                "Удобная классическая мебель с партами и досками."
            ],
            "cons": [
                "Отсутствие современности, устаревший интерьер.",
                "Строгий пропускной режим на входе."
            ],
            "prompt": "Academic seminar in a traditional university lecture classroom in Vasilyevsky Island St. Petersburg, male professor writing key formulas on white board --ar 16:9"
        },
        {
            "num": 15,
            "name": "Конференц-зал «Астория»",
            "context": "Самый премиальный и статусный формат напротив Исаакиевского собора. Служит для VIP-семинаров, закрытых встреч инвесторов и презентаций для топ-менеджмента транснациональных корпораций.",
            "site": "https://astoria.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Большая Морская, д. 39",
            "cost": "от 12 000 до 35 000 руб./час",
            "for_whom": "VIP-семинары, закрытые бизнес-саммиты, финансовые клубы (до 50 человек).",
            "pros": [
                "Максимальный статус, безупречный мировой уровень сервиса.",
                "Вид на Исаакиевский собор, высочайший комфорт."
            ],
            "cons": [
                "Экстремально высокий бюджет.",
                "Жесткий дресс-код и регламент проведения."
            ],
            "prompt": "Exclusive VIP seminar in a luxurious hotel ballroom in Astoria Hotel Saint Petersburg with view of St Isaac's Cathedral, male expert speaker delivering keynote to business executives --ar 16:9"
        }
    ]

    for v in venues:
        add_h2(f"{v['num']}. {v['name']}")
        add_p(v['context'])

        add_bullet("Сайт", v['site'])
        add_bullet("Адрес", v['address'])
        add_bullet("Стоимость аренды", v['cost'])
        add_bullet("Для кого подходит", v['for_whom'])

        add_h3("Плюсы площадки:")
        for pro in v['pros']:
            add_bullet("✔", pro)

        add_h3("Минусы площадки:")
        for con in v['cons']:
            add_bullet("✖", con)

        add_callout(v['prompt'])

    # CHECKLIST & SUMMARY
    add_h2("Практический чек-лист: Как выбрать площадку для семинара в СПб и не прогореть")
    add_p("Опираясь на свой 10-летний опыт, рекомендую проверять площадку по следующим 6 критическим критериям перед внесением предоплаты:")

    add_bullet("1. Технический аудит звука и света", "Никогда не верьте на слово фразе «у нас всё есть». Обязательно протестируйте микрофон и проектор лично со своего ноутбука. В таких площадках, как Luminis Loft или Event Pandora, техника уже настроена под ключ, но в исторический локациях часто бывают сюрпризы.")
    add_bullet("2. Запас по вместимости и гибкость рассадки", "Если у вас планируется 40 участников, выбирайте зал на 50–60 мест. Аудитория не должна сидеть «плечом к плечу», людям нужен воздух и место для записей.")
    add_bullet("3. Логистика кофе-брейка", "Зона питания не должна находиться в том же пятачке, где сидят слушатели. Идеально, если под кофе-паузу выделена отдельная барная стойка или холл (как в Memories Loft).")
    add_bullet("4. Климат-контроль и вентиляция", "Через 45 минут интенсивной лекции в непроветриваемом зале аудитория начнет засыпать. Убедитесь в наличии мощного приточно-вытяжного кондиционирования.")
    add_bullet("5. Транспортная доступность", "В Питере критически важно наличие метро в 7–10 минутах пешком или удобной парковки, иначе 20% участников опоздают из-за пробок.")
    add_bullet("6. Эмоциональный формат события", "Для драйва и баттлов выбирайте Show Ring, для уютного нетворкинга — Memories Loft, для технологичного обучающего интенсива — Luminis Loft или Event Pandora.")

    add_h2("Заключение и выводы")
    add_p("Успех любого семинара в Санкт-Петербурге состоит из трех слагаемых: сильный экспертный контент, вовлеченная аудитория и правильно подобранная атмосфера. Не бойтесь отходить от унылых офисных стен — современная аудитория ценит стиль, комфорт и качественную визуалку.")
    add_p("Если вы планируете яркий, запоминающийся семинар в 2025 году, советую присмотреться к площадкам из начала нашего списка (Luminis Loft, Memories Loft, Event Pandora, Show Ring) — они дают идеальное соотношение цены, высокого сервиса и технологической готовности.")

    doc.save(filepath)
    print(f"Document successfully created and saved to {filepath}")

if __name__ == "__main__":
    generate_article_docx()
