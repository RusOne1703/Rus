import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_conference_faq_docx(filepath="подборка_площадок_для_конференций_спб_с_faq.docx"):
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
    COLOR_FAQ_TITLE = RGBColor(116, 42, 119)  # Purple Accent #742A77

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

    # TITLE & HEADER
    add_h1("Где провести конференцию в СПб: ТОП-15 лучших площадок и залов 2025 года + SEO FAQ для организаторов")
    add_p("Автор: Илья Сергеев, ивент-продюсер, организатор масштабных конференций и бизнес-форумов с 10-летним стажем в Санкт-Петербурге.", bold_prefix="📌 ")

    # INTRO
    add_h2("Введение: Как организовать незабываемую конференцию в Санкт-Петербурге")
    add_p("Организация масштабной конференции в Санкт-Петербурге — это всегда серьезный вызов для маркетологов, HR-директоров и event-продюсеров. Конференция — это не просто серия докладов, это репутация вашей компании, площадка для нетворкинга, заключения многомиллионных контрактов и демонстрации лидерских позиций на рынке.")
    add_p("Правильный выбор площадки закрывает до 80% всех организационных рисков. Плохой звук, зависающая трансляция, нехватка гардероба или невкусный кофе-брейк могут полностью испортить впечатление даже от самых известных спикеров. В Санкт-Петербурге представлен огромный выбор залов — от гигантских конгресс-центров до современных технологичных лофтов и исторический особняков.")
    add_p("В этой подробной подборке я разберу ТОП-15 лучших площадок для проведения конференций и бизнес-форумов в СПб в 2025 году. В список вошли как флагманские специализированные пространства, так и ведущие отельные и креативные площадки. В конце статьи вы найдете блог SEO FAQ с ответами на самые частые вопросы организаторов.")

    add_callout(
        "A stylish male conference producer in his mid-30s wearing a charcoal grey tailored suit, standing at a professional lectern with a wireless microphone on a grand conference stage in Saint Petersburg. Behind him is a massive panoramic LED screen displaying high-tech data visuals and the event logo. Bright modern stage lighting, engaged professional audience in a large auditorium, photorealistic, 8k resolution, cinematic lighting --ar 16:9 --style raw",
        title="📸 Промт для нейросети (Главная обложка статьи с автором на конференции):"
    )

    # VENUES DATA FOR CONFERENCES
    venues = [
        {
            "num": 1,
            "name": "Event Pandora (Эвент Пандора)",
            "context": "Event Pandora — высокотехнологичный конгресс-лофт нового поколения, идеально приспособленный под масштабные конференции, IT-форумы и гибридные онлайн/офлайн события. Главное преимущество площадки — заложенная в инфраструктуру мощнейшая мультимедийная база. Здесь установлены светодиодные экраны сверхвысокого разрешения, студийный свет и концертная акустика, что позволяет проводить конференции уровня федеральных брендов без необходимости привлекать сторонних подрядчиков по технике.",
            "site": "https://eventpandora.ru",
            "address": "г. Санкт-Петербург, удобный доступ от метро (Центральный/Невский район)",
            "cost": "от 3 000 до 6 500 руб./час (зависит от масштаба зала и технического пакета)",
            "for_whom": "Бизнес-конференции, IT-митапы, отраслевые форумы, гибридные онлайн-конференции, дилерские съезды (от 50 до 200+ делегатов).",
            "pros": [
                "Собственный мультимедийный парк концертного класса: светодиодные экраны, радиосистемы Sennheiser, профессиональный свет.",
                "Готовая инфраструктура для прямого стриминга и записи видео высочайшего качества.",
                "Просторные зоны для регистрации делегатов, выставки спонсорских стендов и кофе-пауз.",
                "Наличие спикерской гримерной и отдельной пультовой для режиссера трансляции.",
                "Опытная команда технического сопровождения входит в стоимость."
            ],
            "cons": [
                "Плотный график бронирования в сезон конференций (весна/осень) — бронировать нужно за 1.5–2 месяца.",
                "Для совсем небольших камерных совещаний до 15 человек пространство слишком просторно."
            ],
            "prompt": "Male conference host in a blue blazer standing on stage at Event Pandora venue in Saint Petersburg, delivering an opening speech. A huge ultra-wide LED screen behind him displays a colorful corporate conference banner. Modern theater-style seating full of business delegates, sharp detail, dramatic event lighting --ar 16:9"
        },
        {
            "num": 2,
            "name": "Luminis Loft (Люминис Лофт)",
            "context": "Luminis Loft — концептуальное пространство в центре СПб, сочетающее эстетику премиального лофта и технические возможности современного конференц-зала. Площадка отлично подходит для проведения интенсивных деловых конференций, партнерских встреч и обучающих форумов. В Luminis Loft особое внимание уделено климат-контролю и удобству рассадки: эргономичные кресла и трансформируемые столы позволяют участникам комфортно работать в течение всего дня.",
            "site": "https://luminis-loft.ru/",
            "address": "г. Санкт-Петербург, Невский проспект / центральная локация",
            "cost": "от 2 500 до 4 800 руб./час",
            "for_whom": "Маркетинговые и продуктовые конференции, клиентские дни, интенсивные бизнес-форумы, воркшопы для топ-менеджмента (до 80–100 участников).",
            "pros": [
                "Дизайнерское управляемое освещение с возможностью подстройки под цвета бренда заказчика.",
                "Полный комплект звука, проекционного оборудования и радиомикрофонов без скрытых арендных наценок.",
                "Идеальная акустика и отличная шумоизоляция от уличного трафика.",
                "Удобное расположение в пешей доступности от ключевых станций метро.",
                "Собственная выделенная зона для кофе-брейков и фуршетов."
            ],
            "cons": [
                "Парковка в самом центре Петербурга может потребовать предварительного планирования.",
                "Ограничение по максимальной вместимости до 100 человек при рассадке «театр»."
            ],
            "prompt": "An expert male speaker during a panel discussion conference at Luminis Loft in St. Petersburg. He is sitting on a modern stage chair holding a microphone, speaking to an audience of attentive executives. Stylish lighting accents, high resolution presentation slide on projection wall, clear event photography --ar 16:9"
        },
        {
            "num": 3,
            "name": "Show Ring (Шоу Ринг)",
            "context": "Show Ring — инновационная площадка для проведения динамичных конференций, спикерских баттлов, панельных дискуссий и форумов в формате «кругового обзора». Построение зала вокруг центральной сцены создает мощный эффект вовлечения: спикер находится в эпицентре внимания, а участники чувствуют себя активными участниками диалога. Площадка идеально подходит для конференций нового формата, где важно сломать барьер между цехом и аудиторией.",
            "site": "https://show-ring.ru/",
            "address": "г. Санкт-Петербург, центральный креативный район",
            "cost": "от 2 500 до 5 200 руб./час",
            "for_whom": "Интерактивные конференции, дискуссионные бизнес-клубы, стартап-питчи, панели с экспертами, мотивационные форумы (до 80–100 человек).",
            "pros": [
                "Уникальная конфигурация «арена/ринг», создающая максимум энергии и эффекта присутствия.",
                "Профессиональный управляемый свет и многоканальный звук с режиссерского пульта.",
                "Отличный визуальный контент для социальных сетей и СМИ после мероприятия.",
                "Гибкие возможности брендирования площадки.",
                "Персональный менеджер сопровождения."
            ],
            "cons": [
                "Не подходит под классический строгий формат сухих научных докладов по бумажке.",
                "Требует динамичного ведущего или модератора секций."
            ],
            "prompt": "Charismatic male keynote speaker in the center ring of Show Ring venue in St. Petersburg, holding a wireless microphone, surrounding tiered rows filled with engaged delegates listening, dynamic spotlights, immersive conference atmosphere, shot from elevated angle --ar 16:9"
        },
        {
            "num": 4,
            "name": "Memories Loft (Мемориз Лофт)",
            "context": "Memories Loft — видовое авторское пространство для проведения атмосферных, закрытых и экспертных конференций. Если вы собираете топ-менеджеров, инвесторов или ключевых партнеров, где наряду с официальной программой важен душевный нетворкинг и премиальный уют, Memories Loft станет идеальным выбором. Историческая кирпичная кладка, высокие своды, панорамные окна и изысканная мебель создают атмосферу элитного делового клуба.",
            "site": "https://memoriesloft.ru/",
            "address": "г. Санкт-Петербург, Петроградская сторона / исторический центр",
            "cost": "от 2 000 до 4 000 руб./час",
            "for_whom": "Камерные конференции, закрытые клубы инвесторов, стратегические и форсайт-конференции, VIP-презентации (до 50–60 человек).",
            "pros": [
                "Неповторимый стиль и эстетика исторического Петербурга.",
                "Высокий уровень комфорта и приватности для статусных гостей.",
                "Наличие удобной барной зоны для душевного нетворкинга и качественного кофе-брейка.",
                "Естественный свет для дневных сессий и красивая подсветка вечером.",
                "Гибкий подход команды к организационным запросам."
            ],
            "cons": [
                "Не предназначена для гигантских потоковых конференций более 70 участников.",
                "Высокий спрос на бронирование в выходные дни."
            ],
            "prompt": "An executive panel conference session inside Memories Loft in St Petersburg. Male expert moderator leading a discussion with high-level corporate partners sitting on vintage leather sofas, brick walls, daylight from arched windows, photorealistic details --ar 16:9"
        },
        {
            "num": 5,
            "name": "Конгрессно-выставочный центр «Экспофорум»",
            "context": "Экспофорум — главный и самый крупный конгрессно-выставочный комплекс Северо-Запада России. Здесь проходят ПМЭФ и крупнейшие международные конференции. Площадка обладает трансформируемыми залами вместимостью от 50 до 4 000 человек с инфраструктурой мирового уровня.",
            "site": "https://expoforum-center.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Петербургское шоссе, д. 64/1",
            "cost": "от 15 000 до 150 000+ руб./час (в зависимости от павильона и зала)",
            "for_whom": "Масштабные международные и всероссийские конференции, выставочные форумы, съезды (от 300 до несколько тысяч участников).",
            "pros": [
                "Инфраструктура международного уровня, любые масштабы.",
                "Огромная парковка, собственные отели на территории комплексе."
            ],
            "cons": [
                "Удаленность от центра города (рядом с Пулково).",
                "Высокие бюджеты и сложная бюрократическая процедура согласований."
            ],
            "prompt": "A huge international business conference inside Expoforum congress center in St. Petersburg, large modern auditorium with thousands of delegates, high stage with LED screens, male speaker --ar 16:9"
        },
        {
            "num": 6,
            "name": "Конференц-отель «Cosmos St. Petersburg Pribaltiyskaya»",
            "context": "Один из самых известных конгресс-отелей Петербурга на берегу Финского залива. Оборудован большим концертным залом-трансформером и десятками залов для параллельных секций конференций.",
            "site": "https://pribaltiyskaya.cosmoshotels.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Кораблестроителей, д. 14",
            "cost": "от 6 000 до 25 000 руб./час",
            "for_whom": "Отраслевые медицинские, научные и корпоративные конференции с проживанием спикеров (до 1000 участников).",
            "pros": [
                "Возможность одновременно провести пленарное заседание и 10+ параллельных секций.",
                "Проживание сотен участников в одном здании."
            ],
            "cons": [
                "Советская монументальная архитектура, требующая современной косметики в некоторых зонах.",
                "Ветер с Васильевского острова в зимнее время."
            ],
            "prompt": "Large plenary conference session in Cosmos Pribaltiyskaya hotel auditorium in St Petersburg, male keynote lecturer on stage, rows of chairs with attendees --ar 16:9"
        },
        {
            "num": 7,
            "name": "Отель «Corinthia St. Petersburg» (Коринтия)",
            "context": "Пятизвездочный отель в самом центре Невского проспекта с грандиозным конгресс-центром. Залы оформлены в классическом элегантном стиле, идеальны для банковских и юридических конференций.",
            "site": "https://corinthia.com/stpetersburg (конкурент)",
            "address": "г. Санкт-Петербург, Невский пр., д. 57",
            "cost": "от 10 000 до 35 000 руб./час",
            "for_whom": "Премиальные бизнес-конференции, финансовые и инвестиционные форумы (до 350 участников).",
            "pros": [
                "Роскошная локация на Невском проспекте.",
                "Пятизвездочный уровень сервиса, кейтеринга и обслуживания."
            ],
            "cons": [
                "Очень высокий ценник на аренду и обязательный депозит по питанию.",
                "Консервативный интерьер."
            ],
            "prompt": "Luxury business conference in Corinthia Hotel St. Petersburg, crystal chandeliers, male executive delivering lecture at golden podium to well-dressed audience --ar 16:9"
        },
        {
            "num": 8,
            "name": "Loft Hall СПб (Конференц-пространство)",
            "context": "Крупноформатный дизайнерский кластер на Арсенальной набережной. Сочетает лофт-эстетику, масштабные площади и собственную ресторанную службу.",
            "site": "https://lofthall.ru/spb (конкурент)",
            "address": "г. Санкт-Петербург, Арсенальная набережная, д. 1",
            "cost": "от 8 000 до 30 000 руб./час",
            "for_whom": "Креативные и IT-конференции, дилерские форумы, ежегодные итоговые слеты (до 400 участников).",
            "pros": [
                "Потрясающий современный дизайн, вид на Неву.",
                "Мощное собственное оборудование и кейтеринг."
            ],
            "cons": [
                "Высокий суммарный чек.",
                "Сложность с парковкой на набережной в часы пик."
            ],
            "prompt": "Modern IT conference in Loft Hall St Petersburg with exposed brick walls, big stage, digital screen, male speaker answering questions from microphone in crowd --ar 16:9"
        },
        {
            "num": 9,
            "name": "Конгресс-холл «Петроконгресс»",
            "context": "Специализированный конгресс-центр на Петроградской стороне, предназначенный для официальных деловых встреч, медицинских и научных конференций.",
            "site": "https://petrocongress.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Лодейнопольская ул., д. 5",
            "cost": "от 4 000 до 12 000 руб./час",
            "for_whom": "Научные, медицинские, юридические и государственные конференции (до 250 человек).",
            "pros": [
                "Специализированная инфраструктура с залами для синхронного перевода.",
                "Удобное зонирование для выставки."
            ],
            "cons": [
                "Строгий, слегка устаревший офисный интерьер.",
                "Завышенные цены на стандартный кофе-брейк."
            ],
            "prompt": "Scientific conference at Petrocongress center in St Petersburg, male researcher explaining charts on a projector, formal conference seating --ar 16:9"
        },
        {
            "num": 10,
            "name": "Wawelberg Hall (Вавельберг Холл)",
            "context": "Ультрапремиальный исторический зал-амфитеатр в здании Банкира Вавельберга на Невском проспекте. Уникальная историческая лепника сочетается с гидро-подъемной сценой и светодиодным куполом.",
            "site": "https://wawelberg.com/ (конкурент)",
            "address": "г. Санкт-Петербург, Невский пр., д. 7-9",
            "cost": "от 25 000 до 80 000 руб./час",
            "for_whom": "Элитные саммиты, закрытые финансовые конференции, презентации брендов класса люкс (до 150 человек).",
            "pros": [
                "Фантастическая архитектура и музейная роскошь.",
                "Передовое звуковое и световое оборудование мирового уровня."
            ],
            "cons": [
                "Бюджет доступен только крупнейшим корпорациям.",
                "Строжайший регламент и дресс-код."
            ],
            "prompt": "High-end corporate summit inside historic Wawelberg Hall in St Petersburg, male speaker on automated stage under lit stained-glass dome --ar 16:9"
        },
        {
            "num": 11,
            "name": "Лекторий и конгресс-зона «Севкабель Порт»",
            "context": "Популярный креативный кластер на Васильевском острове. Отличное пространство для молодёжных, урбанистических, дизайнерских и IT-конференций с видом на море.",
            "site": "https://sevcabelport.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Кожевенная линия, д. 40",
            "cost": "от 4 500 до 10 000 руб./час",
            "for_whom": "Дизайн-форумы, урбанистические и экологические конференции, маркетинг-саммиты (до 150 человек).",
            "pros": [
                "Уникальный индустриальный дух, близость к набережной.",
                "Большой выбор точек питания на территории."
            ],
            "cons": [
                "Относительная удаленность от станций метро.",
                "В ветреную погоду прохладно на подходах."
            ],
            "prompt": "Creative conference venue at Sevcabel Port in St Petersburg with panoramic sea view windows, male digital strategist giving presentation --ar 16:9"
        },
        {
            "num": 12,
            "name": "Конференц-центр «Ленполиграфмаш»",
            "context": "Инновационный хаб на Петроградке с амфитеатрами и залами-трансформерами. Фокусируется на технологических, инженерных и стартап-конференциях.",
            "site": "https://lpmtech.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, пр. Медиков, д. 3",
            "cost": "от 3 500 до 8 000 руб./час",
            "for_whom": "IT-конференции, стартап-форумы, инженерные и технологические митапы (до 180 человек).",
            "pros": [
                "Отличная инфраструктура для IT: мощный Wi-Fi, розетки у каждого места.",
                "Развитая деловая среда."
            ],
            "cons": [
                "Лаконичный утилитарный интерьер.",
                "Сложный лабиринт коридоров в здании."
            ],
            "prompt": "Tech startup conference amphitheater at Lenpoligraphmash St Petersburg, male developer founder pitching to audience of investors with laptops --ar 16:9"
        },
        {
            "num": 13,
            "name": "Отель «Park Inn by Radisson Pulkovskaya»",
            "context": "Проверенная классика отельного конференц-сервиса рядом с аэропортом Пулково. Подходит для межрегиональных конференций с прилетом множества гостей.",
            "site": "https://radissonhotels.com/ (конкурент)",
            "address": "г. Санкт-Петербург, пл. Победы, д. 1",
            "cost": "от 5 000 до 18 000 руб./час",
            "for_whom": "Межрегиональные конференции, корпоративные съезды, фармацевтические форумы (до 500 человек).",
            "pros": [
                "Близость к аэропорту Пулково.",
                "Большой опыт проведения сетевых конференций."
            ],
            "cons": [
                "Удаленность от исторического центра города.",
                "Классический стандартизированный дизайн."
            ],
            "prompt": "Corporate conference in Radisson Pulkovskaya hotel auditorium in St Petersburg, male speaker on stage, full room of business participants --ar 16:9"
        },
        {
            "num": 14,
            "name": "Конференц-зал отеля «Введенский»",
            "context": "Деловой отель на Петроградской стороне с несколькими конференц-залами средних размеров и классическим отельным обслуживанием.",
            "site": "https://vvedenskyhotel.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, Большой пр. П.С., д. 37",
            "cost": "от 3 500 до 7 500 руб./час",
            "for_whom": "Корпоративные конференции, юридические и аудиторские форумы (до 100 человек).",
            "pros": [
                "Прекрасный район Петроградки.",
                "Наличие собственного ресторана и комфортных номеров."
            ],
            "cons": [
                "Стандартная отельная рассадка без креативных решений.",
                "Доплата за дополнительное мультимедийное оборудование."
            ],
            "prompt": "Business conference session in Vvedensky hotel hall St Petersburg, male tax consultant lecturing to corporate attendees at long desks --ar 16:9"
        },
        {
            "num": 15,
            "name": "Пространство «Ясная Поляна»",
            "context": "Светлый конференц-зал в скандинавском стиле с живыми растениями и натуральным деревом. Подходит для современных эко- и бизнес-конференций.",
            "site": "https://ypolyana.ru/ (конкурент)",
            "address": "г. Санкт-Петербург, ул. Льва Толстого, д. 1-3",
            "cost": "от 3 500 до 6 500 руб./час",
            "for_whom": "Экологические, HR и маркетинговые конференции, дизайн-форумы (до 70 человек).",
            "pros": [
                "Очень светлый и приятный дизайн, много естественного света.",
                "Удобная локация рядом с метро Петроградская."
            ],
            "cons": [
                "Ограничение по максимальной вместимости.",
                "Строгие правила относительно кейтеринга."
            ],
            "prompt": "Bright eco-friendly business conference in Yasnaya Polyana space St Petersburg, male HR director presenting with screen slides in background --ar 16:9"
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

    # FAQ SECTION FOR SEO
    add_h2("SEO FAQ: Частые вопросы организаторов конференций в Санкт-Петербурге")
    add_p("В этом разделе я собрал ответы на самые частые вопросы, которые возникают у компании и ивент-менеджеров при подборе площадки и организации конференций в СПб.")

    faqs = [
        ("Вопрос 1: За сколько месяцев нужно бронировать площадку для конференции в СПб?",
         "Ответ: Для крупноформатных конференций (от 150+ человек) рекомендуемый срок бронирования составляет от 2 до 4 месяцев, особенно в пиковые сезоны (апрель-июнь и сентябрь-ноябрь). Для камерных конференций и лофтов (Event Pandora, Luminis Loft, Show Ring) оптимальный срок — 3–4 недели до даты проведения."),

        ("Вопрос 2: Что обязательно должно входить в базовую стоимость аренды конференц-зала?",
         "Ответ: Базовый комплект должен включать: основную акустическую систему, от 2 до 4 радиомикрофонов, проектор с экраном или светодиодный экран, кликер для спикера, Wi-Fi для участников и базовая расстановка мебели. В площадках вроде Event Pandora и Luminis Loft техника уже включена, а в классических отелях за каждый микрофон часто просят отдельную доплату."),

        ("Вопрос 3: Как правильно рассчитать кейтеринг и кофе-брейки на конференцию?",
         "Ответ: На стандартную однодневную конференцию (6–8 часов) планируется минимум 2 кофе-брейка (утром и во второй половине дня) и 1 полноценный обед/фуршет. Норма воды — не менее 0.5-1 л на человека. Обращайте внимание на наличие отдельной фуршетной зоны, чтобы запахи еды не мешали в основном зале."),

        ("Вопрос 4: Чем лофт (Event Pandora, Luminis Loft) лучше классического отельного конференц-зала?",
         "Ответ: Лофты дают гораздо большую гибкость в оформлении бренд-зоны, стильный неформальный интерьер, отсутствие академической сухости, а также более мощную техническую базу для трансляций без отельных наценок. При этом гости чувствуют себя расслабленнее, что повышает вовлеченность."),

        ("Вопрос 5: Как организовать качественную гибридную онлайн-трансляцию конференции?",
         "Ответ: Для онлайн-трансляции необходима площадка с выделенным интернет-каналом (от 100 Мбит/с), наличием спикерских гарнитур, микшерного пульта и видеомикшера для переключения камер. Площадка Event Pandora идеально приспособлена под такие задачи «из коробки»."),

        ("Вопрос 6: Какое количество участников оптимально для залов с рассадкой «театр» и «кабаре»?",
         "Ответ: Рассадка «театр» позволяет разместить максимальное количество гостей (100% от емкости зала), но усложняет конспектирование. Рассадка «кабаре» (за круглыми столами) забирает около 40% площади, но идеально подходит для воркшопов, работы в группах и нетворкинга.")
    ]

    for q, a in faqs:
        add_h3(q)
        add_p(a)

    # CHECKLIST & CONCLUSION
    add_h2("Итоговый чек-лист организатора конференции")
    add_bullet("1. Запросите технический райдер", "Убедитесь, что звукорежиссер площадки будет присутствовать на прогоне за день до мероприятия.")
    add_bullet("2. Проверьте скорость Wi-Fi", "Для IT-конференций требуется до 3–5 Мбит на каждого активного пользователя.")
    add_bullet("3. Утвердите тайминг кофе-брейков", "Задержка подачи кофе на 10 минут ломает всю сетку выступлений.")
    add_bullet("4. Подготовьте навигацию", "Установите штендеры и указатели от самого входа/парковки до зала регистрации.")

    add_h2("Заключение")
    add_p("Санкт-Петербург предлагает богатейший выбор площадок под любые задачи и бюджеты. Если вы стремитесь сделать современное, стильное и высокотехнологичное мероприятие, обратите внимание на лидеров нашего рейтинга — Event Pandora, Luminis Loft, Show Ring и Memories Loft.")

    doc.save(filepath)
    print(f"Document successfully created and saved to {filepath}")

if __name__ == "__main__":
    generate_conference_faq_docx()
