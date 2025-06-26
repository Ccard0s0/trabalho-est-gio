from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ⚠️ Troca isto pelos teus dados
EMAIL_FROM = "teuemail@gmail.com"
EMAIL_PASSWORD = "tua_senha_de_aplicacao"  # usa senha de app (Gmail)
EMAIL_TO = "teuemail@gmail.com"

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.json

    nome = data.get("nome")
    bio = data.get("bio")
    cor = data.get("cor")

    # Cria o e-mail
    msg = MIMEMultipart()
    msg["From"] = cardoso20061@gmai.com
    msg["To"] = cardoso200614@gmail.com
    msg["Subject"] = f"Novo currículo enviado por {nome}"

    corpo = f"""
    Nome: {nome}
    Bio: {bio}
    Cor escolhida: {cor}
    """

    msg.attach(MIMEText(corpo, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Currículo enviado com sucesso!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Erro ao enviar e-mail"}), 500

if __name__ == "__main__":
    app.run(debug=True)
