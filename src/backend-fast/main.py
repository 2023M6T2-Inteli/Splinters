from math import atan2
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from fastapi import FastAPI
from models import Relatorio, create_client, create_supabase_client
import httpx
from fastapi.middleware.cors import CORSMiddleware

from embedded.modules.queue import Queue
from embedded.modules.stack import Stack

app = FastAPI()


schema_name = "public"  
table_name = "Relatorio"

#supafastgrupo3

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/relatorios")
async def create_relatorio(relatorio: Relatorio):
    supabase = create_supabase_client()
    
    try:

        response = supabase.table(table_name).insert(relatorio.dict()).execute()
        print(response)
        return response
    except httpx.HTTPError as e:
        return {"message": "Erro ao criar o relatório: " + str(e)}

@app.get("/relatorios")
async def get_relatorios():
    supabase = create_supabase_client()
    
    response = supabase.table(table_name).select("*").execute()
    
    return response


@app.get("/relatorios/{id}")
async def get_relatorios(id: int):
    supabase = create_supabase_client()
     
    response = supabase.table(table_name).select("*").eq('id', str(id)).limit(1).execute()
    print(id)
    return response

import os
import fastapi
import asyncio
from supabase import Client
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from models import create_client, create_supabase_client
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()

# URL e Chave de acesso 
url: str = "https://qeqhovaiuqfkrjywqayz.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFlcWhvdmFpdXFma3JqeXdxYXl6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NTAxNjgwOSwiZXhwIjoyMDAwNTkyODA5fQ.0tuA_64ZpGS8olQikZBDzacoWr1Hj-srdCe46-5Mq90"  
models: Client = create_client(url, key)

#Nome do bucket utilizado - No meu caso é "Images"
bucket_name: str = "video"

@app.get("/list")
async def list():
    # Lista todas as imagens do Bucket 
    res = models.storage.from_(bucket_name).list()
    print(res)

@app.get("/images")
# async def images(image: bytes = fastapi.File(...)):
async def images():
    # Rota da imagem local para ser feito o upload (no meu caso esta na pasta mock e é a imagem "lala.png")
    with open("./mock/lala.png", 'rb+') as f:
        arquivo = f.read()
        # Realiza o upload da imagem no bucket, sendo que o nome "lala.png" será o nome salvo no bucket, e você não pode criar imagens com o mesmo nome, emtão vale adicionar um timestamp pra garantir a diferença de nomes 

        res = models.storage.from_(bucket_name).upload("lala.png", arquivo)
        print(res)
    return {"message": "Image uploaded successfully"}