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
        image_base64 = generate_plot(score, "total")

        body = f"""
        <html>
            <body
                style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; width: 580px; margin: 0 auto; background-color: #f9f9f9; padding: 20px;">

                <!-- <h1 style="color: #0056b3; text-align: center; margin-bottom: 40px;">Profissões de Afinidade</h1> -->
                <!-- 
                <p style="font-size: 16px; color: #555;">Olá,</p>
                <p style="font-size: 16px; color: #555;">Segue abaixo as 4 profissões que você mais teve afinidade:</p> -->

                <table style="width: 100%; margin: 20px 0;">
                    <thead>
                        <tr style="">
                            <th style="text-align: center;">
                                <img src="./jornadas.png" alt="Jornadas" style="width: 125px; " />
                                <p style="font-size: 16px; margin-bottom: 25px;">Segue abaixo as 4 profissões que você mais teve afinidade:</p>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <h2 style="color: #2c3e50; font-size: 30px; text-align: center; margin: 10px;">Computação</h2>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">
                                <!-- Texto com borda -->
                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Engenharia de Computação:</strong> A Engenharia de Computação é
                                    um curso de graduação com duração média de cinco anos, que combina conhecimentos de hardware e
                                    software para formar profissionais capazes de desenvolver e integrar sistemas computacionais.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Ciência da Computação:</strong> A Ciência da Computação é um
                                    curso de graduação com duração média de quatro anos, focado no estudo dos fundamentos teóricos e
                                    práticos da computação.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Ciência de Dados:</strong> A Ciência de Dados é um curso de
                                    graduação que combina conhecimentos de estatística, matemática e computação para analisar
                                    grandes volumes de dados e extrair informações valiosas.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Sistemas de Informação:</strong> Sistemas de Informação é uma
                                    graduação com duração média de quatro anos, que integra conhecimentos de tecnologia e gestão
                                    para desenvolver soluções que otimizem o fluxo de informações nas organizações.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Análise de Desenvolvimento de Sistemas:</strong> O curso de
                                    Análise e Desenvolvimento de Sistemas é uma graduação tecnológica com duração média de dois a
                                    três anos, focada na formação de profissionais aptos a projetar, desenvolver, testar e manter
                                    sistemas computacionais.
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <h2 style="color: #2c3e50; font-size: 30px; text-align: center; margin: 10px;">Computação</h2>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">
                                <!-- Texto com borda -->
                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Engenharia de Computação:</strong> A Engenharia de Computação é
                                    um curso de graduação com duração média de cinco anos, que combina conhecimentos de hardware e
                                    software para formar profissionais capazes de desenvolver e integrar sistemas computacionais.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Ciência da Computação:</strong> A Ciência da Computação é um
                                    curso de graduação com duração média de quatro anos, focado no estudo dos fundamentos teóricos e
                                    práticos da computação.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Ciência de Dados:</strong> A Ciência de Dados é um curso de
                                    graduação que combina conhecimentos de estatística, matemática e computação para analisar
                                    grandes volumes de dados e extrair informações valiosas.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Sistemas de Informação:</strong> Sistemas de Informação é uma
                                    graduação com duração média de quatro anos, que integra conhecimentos de tecnologia e gestão
                                    para desenvolver soluções que otimizem o fluxo de informações nas organizações.
                                </p>

                                <p style="font-size: 16px; color: #333; border: 2px solid #0056b3; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                                    <strong style="color: #0056b3;">Análise de Desenvolvimento de Sistemas:</strong> O curso de
                                    Análise e Desenvolvimento de Sistemas é uma graduação tecnológica com duração média de dois a
                                    três anos, focada na formação de profissionais aptos a projetar, desenvolver, testar e manter
                                    sistemas computacionais.
                                </p>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <!-- Rodapé -->
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