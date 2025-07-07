from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import pdfkit
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)

EMAIL_FROM = "cardoso200614@gmail.com"
EMAIL_PASSWORD = "vsww gdcz dxnl yzyi"  # senha de app do Gmail
EMAIL_TO = "cardoso200614@gmail.com"

# 🧠 Gera PDF a partir do HTML (com CSS aplicado)
def gerar_pdf_html(html_content):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': None
    }

    # Caminho para o CSS (caminho absoluto completo)
    caminho_css = os.path.abspath("css/style.css")

    # Gera o PDF com o CSS aplicado
    pdf = pdfkit.from_string(html_content, False, configuration=config, css=caminho_css, options=options)
    return BytesIO(pdf)

@app.route("/enviar", methods=["POST"])
def enviar():
    html_content = request.form.get("html")

    if not html_content:
        return jsonify({"error": "HTML não fornecido."}), 400

    try:
        # Gerar PDF
        pdf_buffer = gerar_pdf_html(html_content)

        # Criar o e-mail
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = "Novo currículo com estilo visual"

        # Corpo do e-mail
        msg.attach(MIMEText("Segue em anexo o currículo gerado com o estilo visual.", "plain"))

        # Anexar o PDF
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_buffer.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=curriculo.pdf")
        msg.attach(part)

        # Enviar
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        return jsonify({"message": "Currículo enviado com sucesso!"}), 200

    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": "Erro ao gerar ou enviar o PDF"}), 500

if __name__ == "__main__":
    app.run(debug=True)
