import re
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def clean_markdown(text):
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'-\s+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def export_to_pdf(config_id, improved_draft, output_path):
    """
    Converts final improved draft into PDF
    """

    doc = SimpleDocTemplate(
        output_path,   # ✅ FIXED: use full path
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    content = []

    title = Paragraph(
        "Clinical Study Report (CSR) - Final Draft",
        styles["Title"]
    )
    content.append(title)
    content.append(Spacer(1, 20))

    paragraphs = improved_draft.split("\n")

    for para in paragraphs:
        if para.strip():
            content.append(Paragraph(para, styles["Normal"]))
            content.append(Spacer(1, 10))

    doc.build(content)

    print(f"PDF generated successfully: {output_path}")

    return output_path