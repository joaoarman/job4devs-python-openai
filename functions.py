import os
import re
from  PyPDF2 import *
import pdfplumber
import fitz
from datetime import datetime
from deep_translator import GoogleTranslator
import unicodedata
from pdfminer.high_level import extract_text
from ai import gptClient, gptModel, PROMPT

UPLOADS_FOLDER = 'uploads'

# ---------------------------------------------------------------------
# -------------------- Functionality 1: CHECK TEXT --------------------
# ---------------------------------------------------------------------
def saveFile(file):
    fileName = file.filename
    filePath = os.path.join(UPLOADS_FOLDER, fileName)
    file.save(filePath)


def getFilePath(filename):
    filePath = os.path.join(UPLOADS_FOLDER, filename)
    return filePath

def removeFile(filePath):
    os.remove(filePath)


def getText_pypdf2(filePath):
    text = ""
    with open(filePath, 'rb') as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.replace("\n", "<br>") + "<br><br>"

    return text


def getText_pdfPumbler(filePath):
    text = ""
    with pdfplumber.open(filePath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.replace("\n", "<br>") + "<br><br>"

    return text


def getText_pdfMiner(filePath):
    text = extract_text(filePath)
    if text:
        text = text.replace("\n", "<br>") + "<br><br>"

    return text


def getText_pyMuPDF(filePath):
    text = ""
    pdf_document = fitz.open(filePath)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text = page.get_text("text") 
        if page_text:
            text += page_text.replace("\n", "<br>") + "<br><br>"
    pdf_document.close()
    
    return text



# ---------------------------------------------------------------------
# -------------------- Functionality 2: AI ANALYSIS -------------------
# ---------------------------------------------------------------------
def getGPTResponse(message):
    gptResponse = gptClient.chat.completions.create(
        model=gptModel,
        messages=[{"role": "user", "content": message}]
    )
    return gptResponse.choices[0].message.content


def getGenAIResponse(message):
    response = genaiModel.generate_content(message)
    return response.candidates[0].content.parts[0].text


def getAnalysusResults(curriculumContent, jobDescription):

    prompt = PROMPT.format(curriculumContent=curriculumContent, jobDescription=jobDescription)

    gptResponse = getGPTResponse(prompt)
    # genaiResponse = getGenAIResponse(prompt)

    return gptResponse



# ---------------------------------------------------------------------
# ----------------- Functionality 3: CREATE CURRICULUM ----------------
# ---------------------------------------------------------------------
def format_date(date_str):
    # Verifica se a data não é vazia e formata
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    return ''


def translate_pt_to_us(text):
    translated_text = GoogleTranslator(source='pt', target='en').translate(text)
    return translated_text


# ----- BR
def formatProjects(projetctNames, projectLinks, projectDescriptions):
    projects = {}
    for i in range(len(projetctNames)):
        projects[i] = {
            'projectName': projetctNames[i],
            'projectLink': projectLinks[i],
            'projectDescription': projectDescriptions[i]
        }
    return projects


def formatExperiences(companyNames, companyPositions, companyStartDates, companyEndDates, stillWorking, companyDescriptions):
    experiences = {}
    for i in range(len(companyNames) -1, -1, -1):

        experiences[i] = {
            'companyName': companyNames[i],
            'companyPosition': companyPositions[i],
            'companyStartDate': format_date(companyStartDates[i]),
            'companyEndDate': 'Atual' if stillWorking[i] == 'on' else format_date(companyEndDates[i]),
            'companyDescription': companyDescriptions[i]
        }
        
    return experiences


def formatEducations(institutions, courses, edutaionStartDates, educationEndDates, stillStudying, educationDescriptions):
    educations = {}

    for i in range(len(institutions)):
        educations[i] = {
            'institution': institutions[i],
            'course': courses[i],
            'educationStartDate': format_date(edutaionStartDates[i]),
            'educationEndDate': 'Cursando' if stillStudying[i] == 'on' else format_date(educationEndDates[i]),
            'educationDescription': educationDescriptions[i]
        }
    return educations


# ----- US
def formatProjectsUS(projetctNames, projectLinks, projectDescriptions):
    projects = {}
    for i in range(len(projetctNames)):
        projects[i] = {
            'projectName': projetctNames[i],
            'projectLink': projectLinks[i],
            'projectDescription': translate_pt_to_us(projectDescriptions[i])
        }
    return projects


def formatExperiencesUS(companyNames, companyPositions, companyStartDates, companyEndDates, stillWorking, companyDescriptions):
    experiences = {}
    for i in range(len(companyNames) -1, -1, -1):

        experiences[i] = {
            'companyName': companyNames[i],
            'companyPosition': translate_pt_to_us(companyPositions[i]),
            'companyStartDate': format_date(companyStartDates[i]),
            'companyEndDate': translate_pt_to_us('Atual') if stillWorking[i] == 'on' else format_date(companyEndDates[i]),
            'companyDescription': translate_pt_to_us(companyDescriptions[i])
        }
        
    return experiences


def formatEducationsUS(institutions, courses, edutaionStartDates, educationEndDates, stillStudying, educationDescriptions):
    educations = {}

    for i in range(len(institutions)):
        educations[i] = {
            'institution': translate_pt_to_us(institutions[i]),
            'course': translate_pt_to_us(courses[i]),
            'educationStartDate': format_date(edutaionStartDates[i]),
            'educationEndDate': translate_pt_to_us('Cursando') if stillStudying[i] == 'on' else format_date(educationEndDates[i]),
            'educationDescription': translate_pt_to_us(educationDescriptions[i])
        }
    return educations


    




