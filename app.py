import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def enviar_email(email, password):
    remetente = os.environ.get("MAIL_SENDER")
    senha = os.environ.get("MAIL_PASSWORD")
    destinatario = os.environ.get("MAIL_RECIPIENT")

    msg = MIMEMultipart()
    msg["Subject"] = "Nova mensagem do site"
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <h2>Nova mensagem</h2>
    <p><b>Nome:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Mensagem:</b> {message}</p>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)

@app.get("/")
def home():
    return "API ONLINE 🚀"

@app.post("/send-email")
def send_email():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Preencha email e senha"}), 400


    try:
        enviar_email(email, password)
        return jsonify({"message": "Enviado com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
