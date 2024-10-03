import re
import spacy
from pdfminer.high_level import extract_text
from docx import Document
from geotext import GeoText  # For location parsing using city names
from datetime import datetime


nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_contact_info(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return {"email": email[0] if email else None, "phone": phone[0] if phone else None}

def extract_experience(text):
    """
    Extract total experience in years or months.
    Handles both "years of experience" as well as "start-end date" formats.
    """
    # Handle formats like "5 years" or "6 months"
    years_exp = re.findall(r'(\d+)\s+years?', text)
    months_exp = re.findall(r'(\d+)\s+months?', text)

    # Calculate total experience from both years and months
    total_experience = sum(map(int, years_exp)) + sum(map(lambda x: int(x) / 12, months_exp))

    # If specific dates are mentioned, try to calculate the difference in years
    date_patterns = re.findall(r'(\w+\s+\d{4})', text)
    if len(date_patterns) >= 2:
        try:
            start_date = datetime.strptime(date_patterns[0], '%B %Y')
            end_date = datetime.strptime(date_patterns[1], '%B %Y')
            delta = end_date - start_date
            total_experience = max(total_experience, delta.days // 365)
        except ValueError:
            pass  # In case of wrong date format

    return total_experience

def extract_education(text):
    """
    Extract education levels like 10th, 12th, Bachelor, Master, and other courses.
    Also extracts percentage for 10th and 12th if mentioned.
    """
    education = {}
    
    # Extract 10th and 12th percentages (if available)
    tenth = re.search(r'(10th|tenth|ssc)\s*[:\-]?\s*(\d{1,2}[\.,]?\d*%)', text, re.IGNORECASE)
    twelfth = re.search(r'(12th|twelfth|hsc)\s*[:\-]?\s*(\d{1,2}[\.,]?\d*%)', text, re.IGNORECASE)
    
    if tenth:
        education['10th'] = tenth.group(2)
    if twelfth:
        education['12th'] = twelfth.group(2)

    # Extract highest degrees and any additional courses
    degrees = ['Bachelor', 'Master', 'PhD', 'BSc', 'MSc', 'MBA']
    additional_courses = re.findall(r'(certification|course in|training in)\s+(.*?)(?:\n|,)', text, re.IGNORECASE)

    for degree in degrees:
        if re.search(degree, text, re.IGNORECASE):
            education['Highest Degree'] = degree
            break
    else:
        education['Highest Degree'] = "Unknown"

    education['Courses'] = additional_courses if additional_courses else []

    return education

def extract_companies_and_job_titles(text):
    """
    Extract companies worked for and corresponding job titles.
    Handles formats like "Worked at [Company] as [Job Title]"
    """
    companies = re.findall(r'(worked at|experience with|at)\s+(.*?)\s+(as|role|position)\s+(.*?)\.', text, re.IGNORECASE)
    extracted = [{"Company": match[1], "Job Title": match[3]} for match in companies]
    return extracted

def extract_certifications(text):
    certs = re.findall(r'(Certified|Certification|Certifications)\s+(.*?)\s*(?=\n|\.)', text, re.IGNORECASE)
    return [cert[1].strip() for cert in certs] if certs else []

def extract_location(text):
    """
    Use geographic name recognition (GeoText) to extract cities and countries from the resume text.
    """
    places = GeoText(text)
    cities = places.cities if places.cities else ["Unknown"]
    countries = places.countries if places.countries else []
    
    return {"City": cities[0] if cities else "Unknown", "Country": countries[0] if countries else "Unknown"}

def extract_employer_name(text):
    """
    Try to extract the employer's name from the top of the resume.
    We assume that the employer's name appears in the first 50 lines and is formatted as 'Name:'
    """
    lines = text.splitlines()[:50]  # Focus on the top 50 lines
    name_pattern = re.search(r'(Name)\s*[:\-]?\s*(\w+)', "\n".join(lines), re.IGNORECASE)
    return name_pattern.group(2) if name_pattern else None



def extract_skills(text):
    """
    Extract a broad range of skills from both IT and non-IT fields.
    Skills might be explicitly mentioned in a 'Skills' section, or within job descriptions.
    """
    # Predefined IT/non-IT skill keywords, properly escaped
    it_skills = ['Python', 'Java', 'React', 'JavaScript', 'SQL', 'C\+\+', 'HTML', 'CSS', 'AWS', 'Docker', 'Kubernetes', 'Node\.js']
    non_it_skills = ['Communication', 'Leadership', 'Project Management', 'Teamwork', 'Sales', 'Customer Service']

    # Extract skills from text
    skills_section = re.search(r'Skills\s*[:\-]?\s*(.*?)(?=\n\n|Experience|Education)', text, re.IGNORECASE | re.DOTALL)
    skills_found = []

    if skills_section:
        # Look for predefined IT and non-IT skills in the skills section
        for skill in it_skills + non_it_skills:
            if re.search(skill, skills_section.group(1), re.IGNORECASE):
                skills_found.append(skill)
    else:
        # If there's no explicit skills section, search in the whole text
        for skill in it_skills + non_it_skills:
            if re.search(skill, text, re.IGNORECASE):
                skills_found.append(skill)

    return list(set(skills_found))  # Return unique skills


# def parse_resume(file_path):
#     """
#     Parse a resume to extract various details like name, experience, education, skills, companies, etc.
#     """
#     if file_path.endswith(".pdf"):
#         text = extract_text_from_pdf(file_path)
#     elif file_path.endswith(".docx"):
#         text = extract_text_from_docx(file_path)
    
#     doc = nlp(text)
#     entities = {
#         "Name": "",
#         "Skills": [],
#         "Experience": 0,
#         "Email": "",
#         "Phone": "",
#         "Education": {},
#         "Companies Worked": [],
#         "Certifications": [],
#         "Location": {},
#         "Job Title": "",
#         "Employer Name": ""
#     }

#     # Extract name (first PERSON entity or employer name at the top)
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             entities["Name"] = ent.text
#             break

#     # Extract skills
#     entities["Skills"] = extract_skills(text)

#     # Extract contact info
#     contact_info = extract_contact_info(text)
#     entities["Email"] = contact_info["email"]
#     entities["Phone"] = contact_info["phone"]

#     # Extract experience
#     entities["Experience"] = extract_experience(text)

#     # Extract education level
#     entities["Education"] = extract_education(text)

#     # Extract companies worked for and job titles
#     entities["Companies Worked"] = extract_companies_and_job_titles(text)

#     # Extract certifications
#     entities["Certifications"] = extract_certifications(text)

#     # Extract location
#     entities["Location"] = extract_location(text)

#     # Extract employer name (from the top of the resume)
#     entities["Employer Name"] = extract_employer_name(text)

#     return entities




from pyresparser import ResumeParser
import os

def parse_resume(file_path):
    """
    Use Pyresparser to parse the resume and extract details like name, email, phone, skills, education, experience, etc.
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")
    
    # Use Pyresparser to extract information
    resume_data = ResumeParser(file_path).get_extracted_data()

    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    # Prepare the entities in the format we want
    entities = {
        "Name": resume_data.get("name", ""),
        "Email": resume_data.get("email", ""),
        "Phone": resume_data.get("mobile_number", ""),
        "Experience": resume_data.get("total_experience", 0),  # in years
        "Skills": resume_data.get("skills", extract_skills(text)),
        "Education": resume_data.get("education", extract_education(text)),
        "Designation": resume_data.get("designation", ""),
        "Companies Worked": resume_data.get("company_names", extract_companies_and_job_titles(text)),
        "Certifications": resume_data.get("certifications", extract_certifications(text)),
        "Location": resume_data.get("location", extract_location(text)),
        "Languages": resume_data.get("languages", [])
    }

    return entities
