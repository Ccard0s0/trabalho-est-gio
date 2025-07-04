from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO
from flask_cors import CORS
import pdfkit

app = Flask(__name__)
CORS(app)

EMAIL_FROM = "cardoso200614@gmail.com"
EMAIL_PASSWORD = "vsww gdcz dxnl yzyi"  # senha de app do Gmail
EMAIL_TO = "cardoso200614@gmail.com"

# Função para gerar um design de PDF mais elegante
def gerar_pdf(nome, profissao, bio, cor, competencias, experiencia, formacao, projectos, contactos, idiomas, redes):
    buffer = BytesIO()
    
    # Criar o PDF com SimpleDocTemplate e usar Paragraphs para formatação
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo para o título
    title_style = styles["Title"]
    title_style.fontSize = 18
    title_style.alignment = 1  # Centralizar
    
    # Estilo para os textos
    text_style = styles["Normal"]
    text_style.fontSize = 12
    text_style.leading = 14  # Espaçamento entre linhas
    
    # Estilo para os subtítulos
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading1'], fontSize=14, spaceAfter=12)

    # Criar lista de elementos (Texto, parágrafos)
    elements = []

    # Título do currículo
    elements.append(Paragraph(f"<b>{nome}</b>", title_style))
    
    # Subtítulo: Profissão
    elements.append(Paragraph(f"<i>{profissao}</i>", subtitle_style))
    
    # Linha separadora
    elements.append(Paragraph("<hr/>", text_style))
    
    # Bio
    elements.append(Paragraph(f"<strong>Bio:</strong> {bio}", text_style))

    # Cor escolhida - destacada com um fundo
    color_box_style = ParagraphStyle('ColorBox', parent=styles['Normal'], fontSize=12, alignment=1)
    elements.append(Paragraph(f"<b>Cor escolhida:</b> <font color='{cor}'>{cor}</font>", color_box_style))

    # Competências
    elements.append(Paragraph(f"<strong>Competências:</strong> {competencias}", text_style))
    
    # Experiência
    elements.append(Paragraph(f"<strong>Experiência:</strong> {experiencia}", text_style))
    
    # Formação
    elements.append(Paragraph(f"<strong>Formação:</strong> {formacao}", text_style))
    
    # Projetos
    elements.append(Paragraph(f"<strong>Projetos:</strong> {projectos}", text_style))
    
    # Contactos
    elements.append(Paragraph(f"<strong>Contactos:</strong> {contactos}", text_style))
    
    # Idiomas
    elements.append(Paragraph(f"<strong>Idiomas:</strong> {idiomas}", text_style))
    
    # Redes Sociais
    elements.append(Paragraph(f"<strong>Redes Sociais:</strong> {redes}", text_style))

    # Finalizando o conteúdo
    doc.build(elements)
    buffer.seek(0)
    
    return buffer

@app.route("/enviar", methods=["POST"])
def enviar():
    dados = request.form  # Obtém os dados do formulário
    nome = dados.get("nome")
    profissao = dados.get("profissao")
    bio = dados.get("bio")
    cor = dados.get("cor")
    competencias = dados.get("competencias")
    experiencia = dados.get("experiencia")
    formacao = dados.get("formacao")
    projectos = dados.get("projectos")
    contactos = dados.get("contactos")
    idiomas = dados.get("idiomas")
    redes = dados.get("redes")

    if not nome or not profissao or not bio or not cor:
        return jsonify({"error": "Dados incompletos."}), 400

    # Gerar o PDF com os dados
    pdf_buffer = gerar_pdf(nome, profissao, bio, cor, competencias, experiencia, formacao, projectos, contactos, idiomas, redes)

    # Cria o e-mail
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Novo currículo enviado por {nome}"

    # Adiciona o corpo do e-mail
    body = f"Currículo enviado por {nome}. Abaixo estão as informações fornecidas:\n\nNome: {nome}\nProfissão: {profissao}\nBio: {bio}\nCor escolhida: {cor}\nCompetências: {competencias}\nExperiência: {experiencia}\nFormação: {formacao}\nProjetos: {projectos}\nContactos: {contactos}\nIdiomas: {idiomas}\nRedes Sociais: {redes}"
    msg.attach(MIMEText(body, "plain"))

    # Anexar o PDF ao e-mail
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename=curriculo.pdf")
    msg.attach(part)

    try:
        # Enviar o e-mail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        
        return jsonify({"message": "Currículo enviado com sucesso!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Erro ao enviar e-mail"}), 500

if __name__ == "__main__":
    app.run(debug=False)


def gerar_pdf_html(html_content):
    # Caminho completo para o wkhtmltopdf
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Gera o PDF a partir do HTML em memória
    pdf = pdfkit.from_string(html_content, False, configuration=config)

    return BytesIO(pdf)

    pdf = pdfkit.from_string(html_content, False)
    return BytesIO(pdf)
