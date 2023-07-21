import io
from pathlib import Path
from flask import make_response
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

def pdf_report(pdf_data):
    print(pdf_data)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    story = []
    logo = Path(__file__).resolve().parent.joinpath('img/logo_ics.jpg')
    logo_img = Image(logo, 15*cm, 1*cm)
    story.append(logo_img)
    story.append(Spacer(1, 20))

    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',  # Replace with your desired font name
        fontSize=24,
    )
    title_text = "Shape of Impact"
    title = Paragraph(title_text, title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    sub_title_style = ParagraphStyle(
        'Heading3',
        parent=getSampleStyleSheet()['Heading3'],
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',  # Replace with your desired font name
        fontSize=18,
        underlineWidth=1)
    sub_title_text = "Project Background"
    sub_title = Paragraph(sub_title_text, sub_title_style)
    story.append(sub_title)
    story.append(Spacer(1, 12))


    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

