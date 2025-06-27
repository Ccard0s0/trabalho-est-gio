from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import pdfkit
import tempfile
import os

app = Flask(__name__)
CORS(app)

EMAIL_FROM = "cardoso200614@gmail.com"
EMAIL_PASSWORD = "vsww gdcz dxnl yzyi"
EMAIL_TO = "cardoso200614@gmail.com"

caminho_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtmltopdf)

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.json

    nome = data.get("nome")
    profissao = data.get("profissao")
    bio = data.get("bio")
    cor = data.get("cor")
    competencias = data.get("competencias")
    experiencia = data.get("experiencia")
    contactos = data.get("contactos")
    redes = data.get("redes")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
      <meta charset="UTF-8">
      <style>
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background-color: {cor};
          padding: 40px;
          color: #333;
        }}
        .container {{
          background: white;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
          max-width: 800px;
          margin: auto;
        }}
        h1 {{
          color: #2c3e50;
          margin-bottom: 5px;
        }}
        h2 {{
          color: #7f8c8d;
          margin-top: 0;
        }}
        h3 {{
          margin-top: 30px;
          color: #2c3e50;
        }}
        p {{
          font-size: 16px;
          line-height: 1.6;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>{nome}</h1>
        <h2>{profissao}</h2>

        <h3>Sobre mim</h3>
        <p>{bio}</p>

        <h3>Competências</h3>
        <p>{competencias}</p>

        <h3>Experiência</h3>
        <p>{experiencia}</p>

        <h3>Contactos</h3>
        <p>{contactos}</p>

        <h3>Redes Sociais</h3>
        <p>{redes}</p>
      </div>
    </body>
    </html>
    """

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            pdfkit.from_string(html_content, pdf_file.name, configuration=config)

            msg = MIMEMultipart()
            msg["From"] = EMAIL_FROM
            msg["To"] = EMAIL_TO
            msg["Subject"] = f"Currículo enviado por {nome}"

            msg.attach(MIMEText("Em anexo encontra-se o currículo gerado pelo utilizador.", "plain"))

            with open(pdf_file.name, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attachment.add_header("Content-Disposition", "attachment", filename="curriculo.pdf")
                msg.attach(pdf_attachment)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.send_message(msg)

        os.unlink(pdf_file.name)

        return jsonify({"message": "Currículo enviado por e-mail como PDF!"}), 200
    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": "Erro ao enviar e-mail"}), 500

if __name__ == "__main__":
    app.run(debug=True)
