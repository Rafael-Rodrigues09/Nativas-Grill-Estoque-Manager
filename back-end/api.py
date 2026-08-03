import psycopg2
import os
from sqlalchemy import create_engine, String, Float, Integer, Column, select, update
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date
from dotenv import load_dotenv
from database import connect, Carnes, criar_banco, add_usado, add_sobra, reset, get_data

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def api_door(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Acesso negado")

Base, engine, SessionLocal = connect()

class ModeloRegistro(BaseModel):
    carne_nome: str
    valor: float

app = FastAPI()
criar_banco()

@app.get('/estoque')
def rote_show_data(verify = Depends(api_door)):
    return get_data()

@app.post('/uso')
def rote_uso(dados: ModeloRegistro, verify = Depends(api_door)):
    return add_usado(carne_nome=dados.carne_nome, valor=dados.valor)
    
@app.post('/sobra')
def rote_sobra(dados: ModeloRegistro, verify = Depends(api_door)):
    return add_sobra(carne_nome=dados.carne_nome, valor=dados.valor)
    

@app.post('/reset')
def rote_reset(verify = Depends(api_door)):
    return reset()





