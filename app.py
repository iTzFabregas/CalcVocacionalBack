from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from grafico.grafico import generate_plot
from db.database import select_all
# from email.email import generate_body

# Biblioteca para email
from pydantic import EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64

# Configurações do servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'  # Substitua pelo servidor do seu provedor (ex: Outlook, Yahoo)
SMTP_PORT = 587
EMAIL_ADDRESS = 'fab.sampaioo@gmail.com'  # Substitua pelo seu email
EMAIL_PASSWORD = 'obrj hkau wphg htvu'          # Substitua pela senha ou app password

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestTypePlot(BaseModel):
    score: list[int]
    result_type: str

class RequestTypeEmail(BaseModel):
    score: list[int]
    user_email: str


@app.get("/")
async def home_endpoint():
    return 'Continua tendo nada aqui não!'

@app.post("/generate-plot")
async def generate_plot_endpoint(data: RequestTypePlot):
    try:
        image_base64 = generate_plot(data.score, data.result_type)
        return JSONResponse(content={"image": image_base64})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar grafico: {str(e)}")

@app.get("/db")
async def db_select_endpoint():
    try:
        result = select_all()  # Obter os dados do banco de dados
        if not result: 
            raise HTTPException(status_code=500, detail="Nenhum dado encontrado.")
        
        return JSONResponse(content=jsonable_encoder({"select": result}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao selecionar dados: {str(e)}")

@app.get("/send-email/")
async def send_email_endpoint(data: RequestTypeEmail):
    try:
        
        # criando o email com o body
        body = generate_body(data.score)

        msg = MIMEMultipart("alternative")
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = data.user_email
        msg['Subject'] = "Gráfico Gerado"
        msg.attach(MIMEText(body, 'html'))


        # criando a imagem em anexo
        image_base64 = generate_plot(data.score, "total") 
        image_bytes = base64.b64decode(image_base64)

        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(image_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename=grafico.png',
        )
        msg.attach(attachment)

        # enviando o email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return {"message": "Email enviado com sucesso com o gráfico no corpo do e-mail!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {str(e)}")


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

        return body

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar corpo do e-mail: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)

