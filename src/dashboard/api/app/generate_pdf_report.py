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

from .data_types import styles_map
from app import postcode_gdf, world_gdf

matplotlib.use('agg')  # Set the backend to 'agg' for non-GUI use

# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

def pdf_report(pdf_data, topic):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    doc.title = 'ICS Report'
    story = []

    # Logo
    story.append(add_logo())
    story.append(Spacer(1, 20))

    # Title
    story.append(add_title("Shape of Impact"))
    story.append(Spacer(1, 12))

    story.append(add_subtitle("<b>Project Background</b>"))

    story.append(add_text(pdf_data["background_text"]["about"]))
    story.append(Spacer(1, 12))

    if topic is None:
        topic_subtitle_text = "<u><b>Topic</b> - All Topics</u>"
        description_text = pdf_data["background_text"]["all_topics_description"]
        narrative_text = "All topics selected"
    else:
        topic_subtitle_text = f"<u><b>Topic:</b> {pdf_data['topic'][0].get('topic_name')} - <b>Topic Group:</b> {pdf_data['topic'][0].get('topic_group')}</u>"
        description_text = pdf_data["topic"][0].get("description")
        narrative_text = pdf_data["topic"][0].get("narrative")
    story.append(add_subtitle(topic_subtitle_text, center=True))
    story.append(Spacer(1, 12))

    story.append(add_subtitle("Description"))
    story.append(add_text(description_text))

    story.append(add_subtitle("Narrative"))
    story.append(add_text(narrative_text))
    story.append(Spacer(1, 12))

    story.append(add_funder_info(pdf_data))
    story.append(Spacer(1, 24))

    story.append(add_uoa_info(pdf_data))
    story.append(Spacer(1, 24))

    story.append(add_institutions_info(pdf_data))
    story.append(Spacer(1, 24))

    story.append(add_beneficiaries_info(pdf_data))
    story.append(Spacer(1, 24))

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

def add_logo():
    logo = Path(__file__).resolve().parent.joinpath('img/logo_ics.jpg')
    logo_img = Image(logo, 15*cm, 1*cm)
    return logo_img

def add_title(title_text):
    title = Paragraph(title_text, styles_map["title"])
    return title

def add_subtitle(subtitle_text, center=False):
    if not center:
        return Paragraph(subtitle_text, styles_map["subtitle"])
    return Paragraph(subtitle_text, styles_map["subtitle_center"])

def add_text(text, footnote=False):
    if footnote is False:
        return Paragraph(text, styles_map["body"])
    else:
        return Paragraph(text, styles_map["footnote"])


def add_funder_info(pdf_data):
    title = add_subtitle(f"<u>{pdf_data['background_text']['label_top_left_box']}</u>", center=True)
    # funder_story.append(Spacer(1, 12))
    if pdf_data["topic"] is None:
        footnote_text = "<b>Figure 1. Top 20 funders for all topics<b>"
    else:
        footnote_text = f"<b>Figure 1. Top 20 funders of topic {pdf_data['topic'][0]['topic_name']}</b>"
    footnote = add_text(footnote_text, footnote=True)
    table_and_graph = create_bar_graph(pdf_data["ics_data"]["funders_counts"], "funder_count", "funder", "Funders")
    funder_table = Table([[title], [table_and_graph], [footnote]], colWidths=[15*cm])
    funder_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    return funder_table

def add_uoa_info(pdf_data):
    title = add_subtitle(f"<u>{pdf_data['background_text']['label_bottom_left_box']}</u>", center=True)
    if pdf_data["topic"] is None:
        footnote_text = "<b>Figure 2. Top units of assessment to which impact case studies in all topics were submitted.<b>"
    else:
        footnote_text = f"<b>Figure 2. Top units of assessment to which impact case studies in topic {pdf_data['topic'][0]['topic_name']} were submitted.</b>"
    footnote = add_text(footnote_text, footnote=True)
    uoa_table_and_graph = create_uoa_bar_chart(pdf_data["ics_data"]["uoa_counts"])
    uoa_table = Table([[title], [uoa_table_and_graph], [footnote]], colWidths=[15*cm])
    uoa_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    return uoa_table

def add_institutions_info(pdf_data):
    pass

def add_beneficiaries_info(pdf_data):
    pass

def add_final_footnote():
    pass


def create_bar_graph(data, value, label, chart_title):
    # Sort the data by values in descending order
    sorted_data = sorted(data, key=lambda x: x[value], reverse=True)

    # Extract the labels and values for the top 20 elements
    top_labels = [item[label].strip() for item in sorted_data[:20]]
    top_values = [item[value] for item in sorted_data[:20]]

    # # If there are more than 20 elements, calculate the sum of the remaining values
    # This is moved to lower down (others in graph is masking shown values because it's too high.)
    # if len(data) > 20:
    #     others_sum = sum(item[value] for item in sorted_data[20:])
    #     top_labels.append('Others')
    #     top_values.append(others_sum)

    # Create a light blue bar graph with black text
    fig, ax = plt.subplots()
    bars = ax.bar(top_labels, top_values, color='lightblue', edgecolor='black')

    ax.set_xlabel('')
    ax.set_ylabel('ICS Count')
    ax.set_title(f'Top 20 {chart_title}' if len(data) > 20 else f'All {chart_title}')
    ax.set_xticks([])
    ax.set_xticklabels([])

    # Add labels inside/outside the bars based on label length
    for bar, label in zip(bars, top_labels):
        x_pos = bar.get_x() + bar.get_width() / 2
        max_label_length = 52
        truncated_label = label[:max_label_length] + '...' if len(label) > max_label_length else label
        y_pos = 0.5
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


def create_uoa_bar_chart(data_list):
    # Extract unique assessment_panel values
    assessment_panels = sorted(set(item['assessment_panel'] for item in data_list))
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

    # Add labels inside/outside the bars based on label length
    for bar, label in zip(bars, names):
        x_pos = bar.get_x() + bar.get_width() / 2
        max_label_length = 52
        truncated_label = label[:max_label_length] + '...' if len(label) > max_label_length else label
        y_pos = 0.5
        rotation = 90

        ax.text(x_pos, y_pos, truncated_label, ha='center', va='bottom', rotation=rotation, fontsize=8)

    # Customize the plot
    ax.set_xlabel('Assessment Panel Name')
    ax.set_ylabel('ICS Count')
    ax.set_title('UOA Count by Assessment Panel')
    ax.set_xticks([])
    ax.set_xticklabels([])
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
        table_data.append([i["name"] if len(i["name"]) < 28 else i["name"][:28] + "...", i["assessment_panel"], i["assessment_group"], i["uoa_count"]])

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
    table = Table(table_data, colWidths=[4.5*cm, 1*cm, 1.5*cm, 1*cm], rowHeights=[0.5*cm for x in range(num_rows)])
    table.setStyle(table_style)
    table_and_graph = Table([[img, table]])
    table_and_graph.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    
    return table_and_graph

