from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os
import pdfkit
from functions import *

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta'  # Substitua pela sua chave secreta real

@app.route('/')
def home():
    return render_template('home.html')


# ---------------------------------------------------------------------
# -------------------- Functionality 1: CHECK TEXT --------------------
# ---------------------------------------------------------------------
@app.route('/checkText')
def checkText():
    return render_template('/checkText/checkText.html')

@app.route('/checkText/result', methods=['POST'])  
def checkTextResult():

    file = request.files['curriculumFile']
    filename = file.filename

    saveFile(file)
    filePath = getFilePath(filename)

    extractedTexts = []

    text1 = getText_pdfMiner(filePath)
    extractedTexts.append(text1)

    text2 = getText_pyMuPDF(filePath)
    extractedTexts.append(text2)

    text3 = getText_pdfPumbler(filePath)
    extractedTexts.append(text3)

    # text4 = getText_pypdf2(filePath)
    # extractedTexts.append(text4)
    
    removeFile(filePath)
    
    return render_template('/checkText/checkText-result.html', extractedTexts=extractedTexts)


# ---------------------------------------------------------------------
# -------------------- Functionality 2: AI Analysis -------------------
# ---------------------------------------------------------------------
@app.route('/aiAnalysis')
def aiAnalysis():
    return render_template('/aiAnalysis/aiAnalysis.html')

@app.route('/aiAnalysis/checkSession', methods=['POST'])
def aiAnalysisCheckSession():

    file = request.files['curriculumFile']
    filename = file.filename

    saveFile(file)
    filePath = getFilePath(filename)

    curriculumContent = getText_pdfMiner(filePath)
    jobDescription = request.form['jobDescription']

    removeFile(filePath)

    response = getAnalysusResults(curriculumContent, jobDescription)

    percentageMatch = re.search(r'\d+%', response)

    """ 62%
    67%
    54%
    62%
    68%
    62%
    78%
    67%
    62%
    77% """


    if percentageMatch:
        percentage = percentageMatch.group() 
        suggestion = response[percentageMatch.end():].strip()
    
    result = [percentage, suggestion]

    session['analysis_result'] = result

    # return render_template('/aiAnalysis/aiAnalysis-result.html', result=result)
    return redirect(url_for('aiAnalysisResult'))


@app.route('/aiAnalysis/result')
def aiAnalysisResult():
    result = session.get('analysis_result')
    if not result:
        # Redireciona de volta para a página de análise se não houver resultado
        return redirect(url_for('aiAnalysis'))
    
    # Opcionalmente, remova o resultado da sessão para evitar recargas futuras
    session.pop('analysis_result', None)
    
    return render_template('/aiAnalysis/aiAnalysis-result.html', result=result)



# ---------------------------------------------------------------------
# ----------------- Functionality 3: Create Curriculum ----------------
# ---------------------------------------------------------------------
@app.route('/createCurriculum')
def createCurriculum():
    return render_template('/createCurriculum/createCurriculum.html')

@app.route('/createCurriculum/result', methods=['POST'])
def createCurriculumResult():

    # ----- INFORMAÇÕES PESSOAIS -----
    name = request.form['userName']
    phone = request.form['telephone']
    email = request.form['email']
    linkedin = request.form['linkedin']
    github = request.form['github']


    # ----- EXPERIÊNCIA PROFISSIONAL -----
    companyNames = request.form.getlist('companyName[]')
    companyPositions = request.form.getlist('companyPosition[]')
    companyStartDates = request.form.getlist('companyStartDate[]')
    companyEndDates = request.form.getlist('companyEndDate[]')
    stillWorking = request.form.getlist('stillWorking[]')
    companyDescriptions = request.form.getlist('companyDescription[]')
    experiences = formatExperiences(companyNames, companyPositions, companyStartDates, companyEndDates, stillWorking, companyDescriptions)
    

    # ----- FORMAÇÃO ACADÊMICA -----
    institutions = request.form.getlist('institution[]')
    courses = request.form.getlist('course[]')
    edutaionStartDates = request.form.getlist('edutaionStartDate[]')
    educationEndDates = request.form.getlist('educationEndDate[]')
    stillStudying = request.form.getlist('stillStudying[]')
    educationDescriptions = request.form.getlist('educationDescription[]')
    educations = formatEducations(institutions, courses, edutaionStartDates, educationEndDates, stillStudying, educationDescriptions)


    # ----- PROJETOS -----
    projetctNames = request.form.getlist('projetctName[]')
    projectLinks = request.form.getlist('projectLink[]')
    projectDescriptions = request.form.getlist('projectDescription[]')
    projects = formatProjects(projetctNames, projectLinks, projectDescriptions)


    # ----- HABILIDADES -----
    skills = request.form.getlist('skills[]')


    # ----- RESULT -----
    result = {
        'name': name,
        'phone': phone,
        'email': email,
        'linkedin': linkedin,
        'github': github,
        'experiences': experiences,
        'educations': educations,
        'projects': projects,
        'skills': skills
    }

    html_content = render_template('/createCurriculum/createCurriculum-result.html', result=result)

    # Geração do PDF a partir do HTML
    pdf = pdfkit.from_string(html_content, False)
    # Configurar a resposta HTTP para download do PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=curriculo.pdf'

    return response

@app.route('/createCurriculum/pdf')
def generate_pdf():
    # Renderiza o HTML que você quer transformar em PDF
    rendered_html = render_template('/createCurriculum/createCurriculum-result.html')

    # Gera o PDF a partir do HTML usando pdfkit
    pdf = pdfkit.from_string(rendered_html, False)

    # Prepara a resposta HTTP com o arquivo PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


if __name__ == '__main__':
    app.run(debug=True, port=5001)