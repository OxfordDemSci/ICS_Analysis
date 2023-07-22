import io
from pathlib import Path
from flask import make_response
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib

matplotlib.use('agg')  # Set the backend to 'agg' for non-GUI use

# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

def pdf_report(pdf_data, topic):
    print(pdf_data["background_text"])
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    doc.title = 'ICS Report'
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

    subtitle_style = ParagraphStyle(
        'Heading3',
        parent=getSampleStyleSheet()['Heading3'],
        alignment=TA_LEFT,
        fontName='Helvetica',  # Replace with your desired font name
        fontSize=18,
        underlineColor='black',
        underlineWidth=1)
    sub_title_text = "Project Background"

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
    sub_title_text = "<b>Project Background</b>"
    subtitle = Paragraph(sub_title_text, subtitle_style)
    story.append(subtitle)

    body_text_style = ParagraphStyle(
        'BodyStyle',
        parent=getSampleStyleSheet()["Normal"],
        alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=12,
    )
    background_text = pdf_data["background_text"]["about"]
    background_info = Paragraph(background_text, body_text_style)
    story.append(background_info)
    story.append(Spacer(1, 12))

    if topic is None:
        topic_subtitle_text = "<u><b>Topic</b> - All Topics</u>"
        description_text = pdf_data["background_text"]["all_topics_description"]
        narrative_text = "All topics selected"

    else:
        topic_subtitle_text = f"<u><b>Topic:</b> {pdf_data['topic'][0].get('topic_name')} - <b>Topic Group:</b> {pdf_data['topic'][0].get('topic_group')}</u>"
        description_text = pdf_data["topic"][0].get("description")
        narrative_text = pdf_data["topic"][0].get("narrative")
    topic_subtitle = Paragraph(topic_subtitle_text, subtitle_style_center)
    story.append(topic_subtitle)
    story.append(Spacer(1, 12))

    description_subtitle = Paragraph("Description", subtitle_style)
    story.append(description_subtitle)
    description = Paragraph(description_text, body_text_style)
    story.append(description)

    narrative_subtitile = Paragraph("Narrative", subtitle_style)
    story.append(narrative_subtitile)
    narrative = Paragraph(narrative_text, body_text_style)
    story.append(narrative)
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<u>{pdf_data['background_text']['label_top_left_box']}</u>", subtitle_style_center))
    story.append(Spacer(1, 12))
    table_and_graph = create_bar_graph(pdf_data["ics_data"]["funders_counts"], "funder_count", "funder", "Funders")
    story.append(table_and_graph)
    story.append(Spacer(1, 24))

    story.append(Paragraph(f"<u>{pdf_data['background_text']['label_bottom_left_box']}</u>", subtitle_style_center))
    story.append(Spacer(1, 12))
    uoa_table_and_graph = create_stacked_bar_chart(pdf_data["ics_data"]["uoa_counts"])
    story.append(uoa_table_and_graph)

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response


def create_bar_graph(data, value, label, chart_title):
    # Sort the data by values in descending order
    sorted_data = sorted(data, key=lambda x: x[value], reverse=True)

    # Extract the labels and values for the top 20 elements
    top_labels = [item[label].strip() for item in sorted_data[:20]]
    top_values = [item[value] for item in sorted_data[:20]]

    # # If there are more than 20 elements, calculate the sum of the remaining values
    # if len(data) > 20:
    #     others_sum = sum(item[value] for item in sorted_data[20:])
    #     top_labels.append('Others')
    #     top_values.append(others_sum)

    # Create a light blue bar graph with black text
    fig, ax = plt.subplots()
    bars = ax.bar(top_labels, top_values, color='lightblue', edgecolor='black')

    ax.set_xlabel('')
    ax.set_ylabel('Counts')
    ax.set_title(f'Top 20 {chart_title}' if len(data) > 20 else f'All {chart_title}')
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add labels inside/outside the bars based on label length
    for bar, label in zip(bars, top_labels):
        x_pos = bar.get_x() + bar.get_width() / 2
        max_label_length = 52
        truncated_label = label[:max_label_length] + '...' if len(label) > max_label_length else label
        y_pos = 1
        rotation = 90

        ax.text(x_pos, y_pos, truncated_label, ha='center', va='bottom', rotation=rotation, fontsize=8)


    # Save the bar graph as an image in memory
    buffer = io.BytesIO()
    canvas = FigureCanvas(plt.gcf())
    canvas.print_png(buffer)
    plt.close(fig)

    # Add the image to the story list
    img = Image(buffer, width=14*cm, height=10*cm)
    
    # If there are more than 20 elements, calculate the sum of the remaining values
    if len(data) > 20:
        others_sum = sum(item[value] for item in sorted_data[20:])
        top_labels.append('Others')
        top_values.append(others_sum)
    # Create the table
    table_data = [[chart_title, 'Count']]
    for top_label, top_value in zip(top_labels, top_values):
        table_data.append([top_label.strip() if len(top_label) < 26 else top_label.strip()[:26] + '...', top_value])

    # Set table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),  # Header background
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),       # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),      # Gridlines
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ])

    num_rows = len(top_labels) + 1  # Include the header row
    for row in range(1, num_rows, 2):
        table_style.add('BACKGROUND', (0, row), (-1, row), (0.9, 0.9, 0.9))

    # Create the table and apply the style
    table = Table(table_data, colWidths=[5*cm, 1*cm], rowHeights=[0.5*cm for x in range(num_rows)])
    table.setStyle(table_style)
    table_and_graph = Table([[img, table]])
    table_and_graph.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    return table_and_graph


def create_stacked_bar_chart(data_list):
    # Extract unique assessment_panel values
    assessment_panels = sorted(set(item['assessment_panel'] for item in data_list))
    print(assessment_panels)
    # Group data by assessment_panel and create subgroups for each name with uoa_count
    data_dict = {}
    for item in data_list:
        assessment_panel = item['assessment_panel']
        name = item['name']
        uoa_count = item['uoa_count']

        if assessment_panel not in data_dict:
            data_dict[assessment_panel] = {}
        data_dict[assessment_panel][name] = uoa_count

    # Prepare data for stacked bar chart
    names = [item['name'] for item in data_list]
    data = [item["uoa_count"] for item in data_list]
    colors_map = {"A": '#f77f00', "B": '#ffcc29', "C": '#008bf8', "D": '#af19ff'}
    leg_colors = [colors_map[x["assessment_panel"]] for x in data_list]

    fig, ax = plt.subplots()
    bars = ax.bar(names, data, color=leg_colors, edgecolor='black')

    ax.set_xlabel('')
    ax.set_ylabel('Counts')
    ax.set_title('UOA Counts')
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add labels inside/outside the bars based on label length
    for bar, label in zip(bars, names):
        x_pos = bar.get_x() + bar.get_width() / 2
        max_label_length = 52
        truncated_label = label[:max_label_length] + '...' if len(label) > max_label_length else label
        y_pos = 0.5
        rotation = 90

        ax.text(x_pos, y_pos, truncated_label, ha='center', va='bottom', rotation=rotation, fontsize=8)

    # Customize the plot
    ax.set_xlabel('Name')
    ax.set_ylabel('UOA Count')
    ax.set_title('UOA Count by Assessment Panel')
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=class_) for class_, color in colors_map.items()]
    legend = ax.legend(handles=legend_handles, title="Assessment Panel", fontsize='small')
    legend.set_title(legend.get_title().get_text(), prop={'size': 'x-small'})


    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Save the plot as a PDF file
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Add the image to the ReportLab story
    img = Image(buffer, width=12*cm, height=8*cm)

    # Create the table
    table_data = [["UOA", "Panel", "Group", 'Count']]
    for i in data_list:
        table_data.append([i["name"] if len(i["name"]) < 26 else i["name"][:26] + "...", i["assessment_panel"], i["assessment_group"], i["uoa_count"]])

    # Set table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),       # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),      # Gridlines
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ])

    num_rows = len(data_list) + 1  # Include the header row
    for row in range(1, num_rows, 2):
        table_style.add('BACKGROUND', (0, row), (-1, row), (0.9, 0.9, 0.9))

    # Create the table and apply the style
    table = Table(table_data, colWidths=[5*cm, 1*cm, 1*cm, 1*cm], rowHeights=[0.5*cm for x in range(num_rows)])
    table.setStyle(table_style)
    table_and_graph = Table([[img, table]])
    table_and_graph.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    
    return table_and_graph

