from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

doc = SimpleDocTemplate("test.pdf", pagesize=A4)
styles = getSampleStyleSheet()
style = ParagraphStyle(
    'Normal',
    fontName='DejaVuSans',
    fontSize=12,
    leading=15
)

story = [Paragraph("Привет, мир! Тестирование генерации PDF на русском языке.", style)]
doc.build(story)
print("PDF test built successfully!")
