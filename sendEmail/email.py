from fastapi import HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from dotenv import load_dotenv
import os

from sendEmail.areas import areas
from grafico.grafico import generate_plot


def send_email(user_email, score):

    load_dotenv()

    try:
        smtp_server=os.getenv("SMTP_SERVER")
        smtp_port=os.getenv("SMTP_PORT")
        email_address=os.getenv("EMAIL_ADDRESS")
        email_password=os.getenv("EMAIL_PASSWORD")

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

        body = """
            <html>
            <body
                style="font-family: 'Roboto', Arial, sans-serif; line-height: 1.6; color: #333; width: 600px; margin: auto; padding: 0px; background-color: #f9f9f9;">

                <table width="600" align="center" border="0" cellpadding="0" cellspacing="0">
                    <thead>
                        <tr>
                            <th style="text-align: center;">
                                <img src="https://main.d2dkvrfv0o0fyy.amplifyapp.com/jornadas-header-email.png" alt="Jornadas header" style="width: 600px; background-color: transparent;" />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 0 10px;">
                                <p style="font-size: 14px;">Olá,</p>
                                <p style="font-size: 14px; margin-bottom: 25px;">Segue abaixo as 4 profissões que você mais teve
                                    afinidade:</p>
                            </td>
                        </tr>
        """

        indices_ordenados = sorted(range(len(score)), key=lambda i: score[i], reverse=True)
        indices_ordenados = indices_ordenados[:4]

        for i in indices_ordenados:
            body += f"""
                        <tr>
                            <td>
                                <h2 style="color: #2c3e50; font-size: 28px; text-align: center; margin: 6px;">{areas[i]['area']}</h2>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">
                    """
            for j in range(len(areas[i]['cursos'])):
                body += f"""
                                <p
                                    style="font-size: 14px; color: #333; border: 2px solid #04caca; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #04caca;">{areas[i]['cursos'][j]['nome']}:</strong> {areas[i]['cursos'][j]['resumo']}
                                </p>
                        """
            body += """
                            </td>
                        </tr>
                """

        body += """
                        <tr>
                            <td style="text-align: center; padding-top: 10px;">
                                <a href=""
                                    style="background-color:#04caca; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-size: 14px;">
                                    Clique aqui para saber mais!
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <p style="text-align: center; font-size: 12px; color: #999; margin-top: 40px;">
                    Este é um e-mail automático. Por favor, não responda.
                </p>

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