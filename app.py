from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from flask_cors import CORS
import pdfkit

app = Flask(__name__)
CORS(app)

EMAIL_FROM = "cardoso200614@gmail.com"
EMAIL_PASSWORD = "vsww gdcz dxnl yzyi"
EMAIL_TO = "cardoso200614@gmail.com"

# Função para gerar o PDF com visual renderizado
def gerar_pdf_html(html_content):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    options = {
        'enable-local-file-access': None,
        'encoding': "UTF-8",
    }

    pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
    return BytesIO(pdf)

@app.route("/enviar", methods=["POST"])
def enviar():
    dados = request.form

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
    curriculo_html = dados.get("curriculo_html")

    if not nome or not profissao or not bio or not cor or not curriculo_html:
        return jsonify({"error": "Dados incompletos."}), 400

    try:
        pdf_buffer = gerar_pdf_html(curriculo_html)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = f"Novo currículo enviado por {nome}"

        body = f"Currículo enviado por {nome}."
        msg.attach(MIMEText(body, "plain"))

        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_buffer.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=curriculo.pdf")
        msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        return jsonify({"message": "Currículo enviado com sucesso!"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": "Erro ao enviar e-mail"}), 500

if __name__ == "__main__":
    app.run(debug=False)
