# utils.py
# This module contains utility functions for extracting text from files

import io
import re
import PyPDF2
from docx import Document

def extract_text_from_file(uploaded_file):
    """
    Extract text from various file formats (txt, pdf, docx)
    """
    if uploaded_file is None:
        return ""
        
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    try:
        if file_extension == "txt":
            # For text files, read directly
            return uploaded_file.getvalue().decode("utf-8")
            
        elif file_extension == "pdf":
            # For PDF files, use PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif file_extension == "docx":
            # For DOCX files, use python-docx
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return "\n".join(text)
            
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def remove_bullet_points_from_sections(resume_text):
    """
    Remove bullet points from Skills and Experience sections in the resume
    """
    if not resume_text:
        return resume_text
        
    # Split the resume into lines for processing
    lines = resume_text.split('\n')
    processed_lines = []
    
    # Track if we're currently in a Skills or Experience section
    in_target_section = False
    current_section = None
    
    for line in lines:
        # Detect section headers (common formats)
        if re.search(r'^(SKILLS|TECHNICAL SKILLS|EXPERTISE|CORE COMPETENCIES|KEY SKILLS)', line.strip().upper()):
            in_target_section = True
            current_section = "SKILLS"
            processed_lines.append(line)
        elif re.search(r'^(EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY)', line.strip().upper()):
            in_target_section = True
            current_section = "EXPERIENCE"
            processed_lines.append(line)
        elif re.search(r'^(EDUCATION|PROJECTS|ACHIEVEMENTS|CERTIFICATIONS|LANGUAGES|INTERESTS)', line.strip().upper()):
            # Exiting a target section
            in_target_section = False
            current_section = None
            processed_lines.append(line)
        else:
            # Process lines within target sections
            if in_target_section:
                # Remove bullet points and any leading whitespace after the bullet
                processed_line = re.sub(r'^[\s]*[•\-\*\+◦◘○◙♦❖⬧➢➤➔➧►❯❱]+\s*', '', line)
                processed_lines.append(processed_line)
            else:
                # Keep other lines unchanged
                processed_lines.append(line)
    
    # Rejoin the lines to form the processed resume
    return '\n'.join(processed_lines)
