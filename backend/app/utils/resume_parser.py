import re
import pdfplumber
from docx import Document
import spacy
from rapidfuzz import fuzz

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group() if match else None

def extract_name(text):
    doc = nlp(text[:1000])  # Only check first 1000 chars for name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text, skill_keywords=None):
    if skill_keywords is None:
        skill_keywords = ["Python", "React", "JavaScript", "SQL", "Flask", "Tailwind", "Vite", "spaCy", "NLP"]
    found = []
    for skill in skill_keywords:
        if fuzz.partial_ratio(skill.lower(), text.lower()) > 80:
            found.append(skill)
    return list(set(found))

def parse_resume(file_path, file_extension):
    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_extension in [".docx"]:
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

    return {
        "raw_text": text,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }