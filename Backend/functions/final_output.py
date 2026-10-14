import re
import os
import unicodedata

from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def clean_markdown(text):
    """Remove basic Markdown formatting and normalize text."""

    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def normalize_pdf_text(text):
    """
    Normalize Unicode characters for ReportLab's built-in fonts.
    Preserve common punctuation by replacing problematic characters
    with readable ASCII equivalents.
    """

    replacements = {
        "\u2010": "-",   # Hyphen
        "\u2011": "-",   # Non-breaking hyphen
        "\u2012": "-",   # Figure dash
        "\u2013": "-",   # En dash
        "\u2014": "-",   # Em dash
        "\u2212": "-",   # Minus sign
        "\u2018": "'",   # Left single quotation mark
        "\u2019": "'",   # Right single quotation mark
        "\u201c": '"',   # Left double quotation mark
        "\u201d": '"',   # Right double quotation mark
        "\u2026": "...", # Ellipsis
        "\u00a0": " ",   # Non-breaking space
        "\u2022": "-",   # Bullet
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Convert remaining characters to ASCII where possible.
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", errors="replace").decode("ascii")

    return text


def export_to_pdf(config_id, improved_draft, output_path):
    """Convert the final improved draft into a PDF."""

    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    styles["Normal"].fontSize = 10
    styles["Normal"].leading = 15
    styles["Title"].fontSize = 16
    styles["Title"].leading = 22

    content = [
        Paragraph(
            "Clinical Study Report (CSR) - Final Draft",
            styles["Title"]
        ),
        Spacer(1, 20)
    ]

    paragraphs = improved_draft.split("\n")

    for para in paragraphs:
        para = para.strip()

        if not para:
            continue

        para = normalize_pdf_text(para)

        # Escape characters that ReportLab interprets as XML markup.
        para = escape(para)

        content.append(Paragraph(para, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    print(f"PDF generated successfully: {output_path}")

    return output_path
