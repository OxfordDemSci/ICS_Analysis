from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',  # Replace with your desired font name
        fontSize=24,
    )


subtitle_style = ParagraphStyle(
        'Heading3',
        parent=getSampleStyleSheet()['Heading3'],
        alignment=TA_LEFT,
        fontName='Helvetica',  # Replace with your desired font name
        fontSize=18,
        underlineColor='black',
        underlineWidth=1)

body_text_style = ParagraphStyle(
        'BodyStyle',
        parent=getSampleStyleSheet()["Normal"],
        alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=12,
    )

subtitle_style_center = ParagraphStyle(
        'Heading3',
        parent=getSampleStyleSheet()['Heading3'],
        alignment=TA_CENTER,
        fontName='Helvetica',  # Replace with your desired font name
        fontSize=18,
        underlineColor='black',
        underlineGap=2,
        underlineWidth=1,
        )

small_centered_style = ParagraphStyle(
    'SmallCentered',
    parent=getSampleStyleSheet()['Normal'],  # You can replace 'Normal' with any other style name from the style sheet
    fontSize=8,  # Adjust the font size as needed
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)


styles_map = {
    "title": title_style,
    "subtitle": subtitle_style,
    "subtitle_center": subtitle_style_center,
    "body": body_text_style,
    "footnote": small_centered_style,
}