from fastapi import HTTPException
from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from grafico.grafico import generate_plot


def send_email(user_email, score):

    try:
        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = 587
        EMAIL_ADDRESS = 'fab.sampaioo@gmail.com'
        EMAIL_PASSWORD = 'obrj hkau wphg htvu'

        msg = MIMEMultipart("alternative")
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = "Gráfico Gerado"

        body = generate_body(score)
        msg.attach(body)

        attachment = generate_anexo(score)
        msg.attach(attachment)

        # enviando o email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
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