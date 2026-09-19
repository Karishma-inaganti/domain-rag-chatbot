from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted,
)
from reportlab.lib.units import inch


INPUT_FILE = "project_report.md"
OUTPUT_FILE = "Domain_Specific_RAG_Chatbot_Report.pdf"


styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    spaceAfter=20,
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontSize=14,
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15,
    spaceAfter=8,
)

code_style = ParagraphStyle(
    "CodeStyle",
    parent=styles["Code"],
    fontSize=8,
    leading=10,
)


def convert_markdown_to_pdf():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    document = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    story = []

    for line in lines:
        line = line.rstrip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        if line.startswith("# "):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))

        elif line.startswith("## "):
            text = line[3:].strip()
            story.append(Paragraph(text, heading_style))

        elif line.startswith("### "):
            text = line[4:].strip()
            story.append(Paragraph(text, heading_style))

        elif line.startswith("```"):
            continue

        elif line.startswith("- "):
            text = "• " + line[2:].strip()
            story.append(Paragraph(text, body_style))

        elif line.startswith("> "):
            text = line[2:].strip()
            story.append(
                Paragraph(
                    f"<i>{text}</i>",
                    body_style,
                )
            )

        else:
            text = line.replace("&", "&amp;")
            story.append(Paragraph(text, body_style))

    document.build(story)

    print(f"PDF created successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    convert_markdown_to_pdf()