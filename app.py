import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, jsonify, request, send_from_directory


app = Flask(__name__)


def enviar_email(name: str, email: str, message: str) -> None:
    remetente = os.environ.get("MAIL_SENDER")
    senha = os.environ.get("MAIL_PASSWORD")
    destinatario = os.environ.get("MAIL_RECIPIENT")

    if not remetente or not senha or not destinatario:
        raise RuntimeError(
            "Defina MAIL_SENDER, MAIL_PASSWORD e MAIL_RECIPIENT nas variaveis de ambiente."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Nova mensagem do site"
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <html>
      <body>
        <h2>Nova mensagem recebida</h2>
        <p><strong>Nome:</strong> {name}</p>
        <p><strong>E-mail:</strong> {email}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{message}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.post("/send-email")
def send_email():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Preencha nome, e-mail e mensagem."}), 400

    try:
        enviar_email(name, email, message)
    except Exception as exc:
        return jsonify({"error": f"Erro ao enviar e-mail: {exc}"}), 500

    return jsonify({"message": "Mensagem enviada com sucesso."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
