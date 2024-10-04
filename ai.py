import os
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------
# -------------------------------- GPT --------------------------------
# ---------------------------------------------------------------------
gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gptModel = os.getenv("GPT_MODEL")

# Código para obter os modelos disponíveis na API do OpenAI

""" 
    import requests
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {os.getenv("OPENAI_API_KEY")}"}
    request = requests.get(url, headers=headers)
    request = request.json()

    ids = [model['id'] for model in request['data']]
    for id in ids:
        print(id)  
"""


# ---------------------------------------------------------------------
# ------------------------------- GEMINI ------------------------------
# ---------------------------------------------------------------------
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
genaiModel = genai.GenerativeModel(os.getenv("GENAI_MODEL"))


# ---------------------------------------------------------------------
# ------------------------------- PROMPT ------------------------------
# ---------------------------------------------------------------------

PROMPT = """ 
        O sitema atual tem como objetivo ajudar os usuários a analisar seus currículos de acordo com a descrição das vagas para as quais estão se candidatando. 
        
        O público alvo/persona são desenvolvedores de software e programadores que estão no início de suas carreiras e buscam oportunidades de emprego, seja como estagiários ou efetivados juniores.

        A ideia é bem simples, você receberá o currículo do usuário e a descrição de alguma determinada vaga de emprego e deverá retornar uma porcentagem (de 0% a 100%) que represente o quanto o candidato se encaixa na vaga. 
        
        Você precisa ser o mais preciso possível. Por se tratar única e exclusivamente da área de técnologia e programação, é importante que você consiga identificar as habilidades técnicas que são necessárias para a vaga, como ferramentas, tecnologias, linguagens de programação, metodologias, frameworks, etc. Lembre-se que, o sistema foi feito para programadores iniciantes, não espere que o candidato preencha todos ou quase todas as competências para considerar porcentagens mais altas.

        O sistema será utilizado por pessoas reais, seja o mais coerente possível.

        Como você deve retornar a resposta?
        Preciso que você retorne uma porcentagem de 0% a 100%, apenas isso, sem mais detalhes.
        Depois disso, quebre a linha e digite um parágrafo explicando o motivo da sua resposta, com possíveis sugestões. É importante ressaltar que utilizarei sua resposta para imprimi-la na tela, então tome cuidado para retornar exatamente como foi solicitado.

        Lembre-se que, em alguns casos, as descrições das vagas são dividias em "Requisitos" e "Diferenciais", ou algo parecido. 
        Você deve considerar os "Requisitos" como obrigatórios e correspondendo a maior parte da sua nota/porcentagem final, e os "Diferenciais" como opcionais e valendo menos "pontos" para a análise final. 

        Aqui estão alguns exemplos:
        
        
        EXEMPLO DE RESPOSTA 1:
        54%

        De acordo com o que foi analisado no seu currículo, você possui conhecimento em algumas tecnologias que são necessárias para a vaga, porém, ainda faltam outras habilidades para o cargo, como conhecimento no mundo de PHP e seus Framworks. Sugiro que busque estudar sobre essa tenlogia necessária e faça um curso de inglês para aumentar suas chances de se destacar nesse processo seletivo.

        
        EXEMPLO DE RESPOSTA 2:
        88%

        De acordo com o que foi analisado no currículo, você possui uma boa parte das habilidades técnicas e comportamentais necessárias para a vaga. No entanto, seria interessante se adquirisse mais experiência prática em projetos reais para se destacar ainda mais. Você preenche todos os requisitos obrigatórios, por isso recebeu uma alta. Para aumentar suas chances, aproveite para estudar mais sobre as tecnologias cidatas como "Diferenciais" na vaga. Lembre-se que nenhum candidato será o ideal, preenchendo 100% dos requisitos, então não se preocupe com isso. Você parece estar apto para a vaga.

        
        EXEMPLO DE RESPOSTA 3:
        32%

        Você não possui experiência nas linguagens de programação ou frameworks exigidos na vaga. Recomendo que invista tempo em aprender e praticar essas tecnologias para aumentar suas chances, ou se candidatar em vagas que exijam habilidades nas quais você já domina.

        
        EXEMPLO DE RESPOSTA 4:
        Caso o texto enviado pelo usuário não seja suficiente para você analisar, você pode pode retornar da seguinte forma:
        0%

        Preciso de mais informações. O arquivo ou a descrição podem estar incorretos.

        Agora que você já sabe como deve responder, vamos para a prática. Seja bem coerente e preciso em sua resposta, pois caso o usuário solicite a análise novamente, ele deverá receber a mesma porcentagem ou uma parecida.

        Aqui está o texto extraódo do currículo do candidato: {curriculumContent}

        E aqui está a descrição da vaga: {jobDescription}
    """