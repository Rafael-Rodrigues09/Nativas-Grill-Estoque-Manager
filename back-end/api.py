import psycopg2
import os
from sqlalchemy import create_engine, String, Float, Integer, Column, select, update
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date
from dotenv import load_dotenv
from database import connect, Meats, create_data, add_usage, add_rest, reset, get_data, reverse, get_history, add_lot, get_lot

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def api_door(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Acesso negado")

Base, engine, SessionLocal = connect()

class ModeloRegistro(BaseModel):
    name: str
    value: float

class ModeloLot(BaseModel):
    name: str
    value: float
    expiration_date: date

app = FastAPI()
create_data()

@app.api_route('/health', methods=['GET', 'HEAD'])
def check_health(): return {'status': 'valid'}

@app.get('/estoque')
def rote_show_data(verify = Depends(api_door)):
    return get_data()

@app.get('/historico')
def rote_show_history():
    return get_history()

@app.get('/allestoque')
def rote_show_lot(verift = Depends(api_door)):
    return get_lot()
@app.post('/add-estoque')
def rote_add_lot(data: ModeloLot, verify = Depends(api_door)):
    return add_lot(name=data.name, value=data.value, expiration_date=data.expiration_date)

@app.post('/uso')
def rote_uso(data: ModeloRegistro, verify = Depends(api_door)):
    return add_usage(data.name, data.value)
    
@app.post('/sobra')
def rote_sobra(data: ModeloRegistro, verify = Depends(api_door)):
    return add_rest(name=data.name, value=data.value)
    

@app.post('/reset')
def rote_reset(verify = Depends(api_door)):
    return reset()

@app.post('/reverse')
def reverse_value(verify = Depends(api_door)):
    return reverse()





