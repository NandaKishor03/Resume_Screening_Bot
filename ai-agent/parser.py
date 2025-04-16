import PyPDF2
from docx import Document
import os
import re

def clean_text(text):
    """Clean extracted text by removing extra whitespaces and newlines."""
    return re.sub(r'\s+', ' ', text).strip()

def parse_pdf(file_path):
    """Extract text from PDF file."""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return clean_text(text)
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def parse_docx(file_path):
    """Extract text from DOCX file."""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error parsing DOCX: {str(e)}")

def parse_file(file_path):
    """Determine file type and parse accordingly."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return parse_pdf(file_path)
    elif file_extension == '.docx':
        return parse_docx(file_path)
    else:
        raise Exception("Unsupported file format")