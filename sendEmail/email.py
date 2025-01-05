from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from dotenv import load_dotenv
import os

from grafico.grafico import generate_plot


def send_email(user_email, score):

    load_dotenv()

    try:
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=os.getenv("SMTP_PORT"),
        email_address=os.getenv("EMAIL_ADDRESS"),
        email_password=os.getenv("EMAIL_PASSWORD"),

        msg = MIMEMultipart("alternative")
        msg['From'] = email_address
        msg['To'] = user_email
        msg['Subject'] = "Gráfico Gerado"

        body = generate_body(score)
        msg.attach(body)

        attachment = generate_anexo(score)
        msg.attach(attachment)

        # enviando o email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(msg)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar e-mail ou enviar: {str(e)}")


def generate_body(score):
    try:
        image_base64 = generate_plot(score, "total")

        body = f"""
        <html>
            <body>
                <h2>Segue o gráfico gerado com os dados fornecidos:</h2>
                <img src="data:image/png;base64,{image_base64}" alt="Gráfico Gerado" width="400" height="300" />
            </body>
        </html>
        """

        body = MIMEText(body, 'html')

        return body

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar corpo do e-mail: {str(e)}")


def generate_anexo(score):
    try:
        image_base64 = generate_plot(score, "total") 
        image_bytes = base64.b64decode(image_base64)

        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(image_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=grafico.png',
        )

        return attachment
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar anexo do e-mail: {str(e)}")