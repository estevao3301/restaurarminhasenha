from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def enviar_email(name: str, email: str, message: str) -> None:
    remetente = os.environ.get("MAIL_SENDER")
    senha = os.environ.get("MAIL_PASSWORD")
    destinatario = os.environ.get("MAIL_RECIPIENT")

    if not all([remetente, senha, destinatario]):
        raise RuntimeError("Variáveis de ambiente não configuradas.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Nova mensagem do site"
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Nova mensagem recebida</h2>
        <p><strong>Nome:</strong> {name}</p>
        <p><strong>E-mail:</strong> {email}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{message}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)


@app.route("/", methods=["GET"])
def home():
    return redirect("https://robiox-site.github.io/login/", code=302)


@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "Visitante").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not email or not message:
        return jsonify({"error": "Preencha todos os campos."}), 400

    try:
        enviar_email(name, email, message)
    except Exception as e:
        return jsonify({"error": f"Erro ao enviar email: {str(e)}"}), 500

    return jsonify({"message": "Mensagem enviada com sucesso!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
