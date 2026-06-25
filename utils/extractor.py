import pdfplumber
import pytesseract
import fitz
from PIL import Image
import os
import io
import platform


if platform.system() == "Windows":
    local_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(local_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = local_tesseract_path


def extract_text_from_pdf_text_layer(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        text += f"\nText-layer extraction error: {e}"

    return text.strip()


def extract_text_from_pdf_ocr(file_path):
    text = ""

    try:
        pdf_document = fitz.open(file_path)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            pix = page.get_pixmap(dpi=200)

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            page_text = pytesseract.image_to_string(image)

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        text += f"\nOCR extraction error: {e}"

    return text.strip()


def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        return f"Image OCR error: {e}"


def calculate_extraction_confidence(text):
    if not text:
        return {
            "confidence": "Low",
            "score": 0,
            "message": "No readable text extracted."
        }

    character_count = len(text)
    word_count = len(text.split())

    if character_count > 500 and word_count > 80:
        return {
            "confidence": "High",
            "score": 90,
            "message": "Strong text extraction quality."
        }

    elif character_count > 150 and word_count > 25:
        return {
            "confidence": "Medium",
            "score": 60,
            "message": "Partial text extraction. Manual review may be needed."
        }

    else:
        return {
            "confidence": "Low",
            "score": 30,
            "message": "Low extraction quality. Document may be scanned, unclear, or poorly formatted."
        }


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf_text_layer(file_path)

        if len(text.strip()) < 50:
            text = extract_text_from_pdf_ocr(file_path)

        return text

    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    else:
        return ""