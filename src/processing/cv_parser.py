import re

import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = " ".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )
    return text


def extract_technologies_from_cv(text, keywords):
    found = sorted(
        {
            kw
            for kw in keywords
            if re.search(r"\b" + re.escape(kw) + r"\b", text, re.IGNORECASE)
        }
    )
    return found


if __name__ == "__main__":
    from src.config import TECH_KEYWORDS

    cv_text = extract_text_from_pdf("data/in/SOFTWARE_ENGINEER_Tom_PAYET.pdf")
    techs = extract_technologies_from_cv(cv_text, TECH_KEYWORDS)
    print("✅ Technologies found in CV:", techs)
