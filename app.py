from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from grafico.grafico import generate_plot
from db.database import select_all, save_results
from sendEmail.email import send_email

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads/"

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
        result = select_all()
        if not result: 
            raise HTTPException(status_code=500, detail="Nenhum dado encontrado.")
        
        return JSONResponse(content=jsonable_encoder({"select": result}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao selecionar dados: {str(e)}")

@app.post("/send-email/")
async def send_email_endpoint(data: RequestTypeEmail):
    try:
        send_email(data.user_email, data.score)
        return {"message": "Email enviado com sucesso com o gráfico no corpo do e-mail!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {str(e)}")

@app.post("/save-results")
async def save_results_endpoint(data: RequestTypeEmail):
    try:
        save_results(data.user_email, data.score)
        return {"message": "Resultados salvos com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os resultados: {str(e)}")
  
@app.post("/upload-image/")
async def upload_image(file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Gere a URL pública (ajuste para o domínio do seu site)
    public_url = f"https://3.12.246.4:4000/uploads/{file.filename}"
    return JSONResponse({"url": public_url})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)

