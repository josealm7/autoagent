"""
Tool: send_email
Envía emails via Gmail SMTP.
Requiere EMAIL_SENDER y EMAIL_PASSWORD en .env
"""
from langchain_core.tools import tool
from app.core.config import get_settings

settings = get_settings()


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    Envía un email a una dirección de correo.
    Úsala cuando el usuario pida enviar información, presupuestos o resúmenes por email.
    Input: dirección de destino, asunto y cuerpo del mensaje.
    El cuerpo puede contener texto plano o HTML básico.
    """
    if not settings.email_sender or not settings.email_password:
        return (
            "⚠️ Email no configurado. Para activar esta función, "
            "añade EMAIL_SENDER y EMAIL_PASSWORD en las variables de entorno."
        )

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.email_sender
        msg["To"] = to

        # Plain text version
        text_part = MIMEText(body, "plain", "utf-8")
        msg.attach(text_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.email_sender, settings.email_password)
            server.sendmail(settings.email_sender, to, msg.as_string())

        return f"✅ Email enviado correctamente a {to} con asunto '{subject}'"

    except Exception as e:
        return f"❌ Error al enviar email: {str(e)}"
