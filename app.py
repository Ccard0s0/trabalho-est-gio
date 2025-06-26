from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Substitui pela tua senha de aplicação (não a senha normal!)
EMAIL_FROM = "cardoso200614@gmail.com"
EMAIL_PASSWORD = "vsww gdcz dxnl yzyi"
EMAIL_TO = "cardoso200614@gmail.com"

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.json

    nome = data.get("nome")
    profissao = data.get("profissao")
    bio = data.get("bio")
    cor = data.get("cor")

    # Criação do e-mail com HTML e estilo
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Novo currículo enviado por {nome}"

    corpo = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                color: #2c3e50;
                text-align: center;
            }}
            .info {{
                margin: 20px 0;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: #fafafa;
            }}
            .info p {{
                font-size: 16px;
                color: #555;
            }}
            .color-box {{
                width: 100%;
                height: 20px;
                background-color: {cor};
                margin-top: 10px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Detalhes do Currículo</h2>
            <div class="info">
                <p><strong>Nome:</strong> {nome}</p>
                <p><strong>Profissão:</strong> {profissao}</p>
                <p><strong>Bio:</strong> {bio}</p>
            </div>
            <div class="color-box"></div>
            <p><strong>Cor escolhida:</strong> {cor}</p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(corpo, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Currículo enviado com sucesso!"}), 200
    except Exception as e:
        print("Erro:", e)
        return jsonify({"error": "Erro ao enviar e-mail"}), 500

if __name__ == "__main__":
    app.run(debug=True)
