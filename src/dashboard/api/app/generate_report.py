from pathlib import Path

from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io

IMG_DIR = Path(__file__).resolve().parent.joinpath('img')

def report_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Prepare the images
    images = [x for x in IMG_DIR.iterdir() if x.name.endswith('.png')]
    image_data = []
    image_list = [Image(image_path) for image_path in images]
    image_width = 100  # Adjust the image width as needed
    for image_path in images:
        with open(image_path, 'rb') as f:
            image_data.append(f.read())  # Store image file data in the list

    # Prepare the title and text
    title = "REF Dashboard Report"
    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum nec aliquam turpis. 
    Sed commodo, risus eu viverra varius, lectus justo dignissim sapien, sit amet feugiat odio ante in quam. 
    Sed pharetra arcu in mi varius fringilla. Morbi consequat bibendum venenatis. Vivamus ut ex vel elit 
    venenatis tincidunt eget non lectus. Nullam eget vulputate purus."""

    # Create the PDF content
    story = []
    for image in image_list:
        story.append(image)
    story.append(Spacer(0, 10))

    styles = getSampleStyleSheet()
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(0, 10))
    story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(0, 20))

    # Create the bar graphs using matplotlib
    fig, axs = plt.subplots(1, 2, figsize=(8, 4))
    axs[0].bar(['A', 'B', 'C', 'D'], [10, 5, 20, 8], color='blue')
    axs[0].set_title('Bar Graph 1')
    axs[1].bar(['X', 'Y', 'Z'], [15, 7, 12], color='green')
    axs[1].set_title('Bar Graph 2')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph1_image_data = buf.read()  # Store graph image data in a variable
    buf.close()

    plt.close(fig)


   # Build the PDF
    story = []
    for img_data in image_data:
        img = Image(io.BytesIO(img_data))
        img.drawHeight = image_width * img.drawHeight / img.drawWidth
        img.drawWidth = image_width
        story.append(img)

    # ... Continue adding other content as before ...

    # Create and add the graph image
    graph1_image = Image(io.BytesIO(graph1_image_data))
    graph1_image.drawWidth = 250
    graph1_image.drawHeight = 150
    story.append(graph1_image)

    doc.build(story)

    # Set up the response to return the PDF
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response