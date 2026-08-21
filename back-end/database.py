from sqlalchemy import create_engine, String, Float, Integer, Column, select, update, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from datetime import date, timezone, datetime
from fastapi.responses import FileResponse
from fpdf import FPDF
def connect():
    load_dotenv()
    url = os.getenv('DATA_URL')
    engine = create_engine(url)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    return Base, engine, SessionLocal

Base, engine, SessionLocal = connect()
class Meats(Base):
    __tablename__ = 'meats'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    usage_kg = Column(Float)
    rest_kg = Column(Float)

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    type = Column(String)
    value = Column(Float)
    is_reversed = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

def create_data():
    meats_list = [
    ("ACEM", 0.0, 0.0),
    ("ALCATRA COMPLETA", 0, 0.0),
    ("ANCHO", 0.0, 0.0),
    ("ASA DE FRANGO", 0.0, 0.0),
    ("BABY BEEF", 0.0, 0.0),
    ("BIFE DO VAZIO", 0.0, 0.0),
    ("CAPA DO FILÉ", 0.0, 0.0),
    ("CARRÉ DE CARNEIRO", 0.0, 0.0),
    ("CHORIZO", 0.0, 0.0),
    ("CONTRA FILÉ", 0.0, 0.0),
    ("COPA LOMBO (JAVALI)", 0.0, 0.0),
    ("CORAÇÃO DE FRANGO", 0.0, 0.0),
    ("COSTELA DE CARNEIRO", 0.0, 0.0),
    ("COSTELA JANELA", 0.0, 0.0),
    ("COSTELA MINGA", 0.0, 0.0),
    ("COSTELA PRIME", 0.0, 0.0),
    ("COSTELA SUÍNA", 0.0, 0.0),
    ("COXA SOBRE COXA", 0.0, 0.0),
    ("COXÃO MOLE", 0.0, 0.0),
    ("CUPIM", 0.0, 0.0),
    ("FILÉ DE FRANGO", 0.0, 0.0),
    ("FILÉ MIGNON", 0.0, 0.0),
    ("FRALDINHA", 0.0, 0.0),
    ("LAGARTO", 0.0, 0.0),
    ("LINGUIÇA", 0.0, 0.0),
    ("LINGUIÇA APIMENTADA", 0.0, 0.0),
    ("PALETA CARNEIRO", 0.0, 0.0),
    ("PANCETA", 0.0, 0.0),
    ("PICANHA", 0.0, 0.0),
    ("PICANHA FATIADA", 0.0, 0.0),
    ("PONTA DE PEITO", 0.0, 0.0),
    ("PRIME", 0.0, 0.0),
    ("QUEIJO", 0.0, 0.0),
    ("SHOT RIBY", 0.0, 0.0),
    ("T BONE CARNEIRO", 0.0, 0.0),
    ("THIBON BOVINO", 0.0, 0.0),
    ("MAMINHA", 0.0, 0.0),
    ("LINGUIÇA CUIABANA", 0.0, 0.0),
    ("PERNIL DE CARNEIRO", 0.0, 0.0)
    ]
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        query = select(Meats)
        if not session.scalars(query).first():
            for meat, usage, rest in meats_list:
                session.add(Meats(name=meat, usage_kg=usage, rest_kg=rest))
            session.commit()

def get_data():
    with SessionLocal() as session:
        query = select(Meats)
        results = session.scalars(query).all()      
        return {result.name: {'usage_kg': result.usage_kg, 'rest_kg': result.rest_kg} for result in results }
    
def get_history():
    with SessionLocal() as session:
        results = session.scalars(select(History)).all()
        return [{'name': meat.name, 'value': meat.value, 'type': meat.type, 'date': meat.date} for meat in results]

def add_usage(name, value):
    with SessionLocal() as session:
        meat = session.scalars(select(Meats).where(Meats.name == name)).first()
        if not meat:
            return {'status': 'invalid'}
        meat.usage_kg += value
        session.add(History(name=name, type='usage', value=value))
        session.commit()
        return {'status': 'success'}
              
def add_rest(name, value):
    with SessionLocal() as session:
        meat = session.scalars(select(Meats).where(Meats.name == name)).first()
        if not meat:
            return {'status': 'invalid'}        
        meat.rest_kg += value
        session.add(History(name=name, type='rest', value=value))
        session.commit()
        return {'status': 'success'}
            
def reset():
    with SessionLocal() as session:
        query_values = select(Meats.name, Meats.usage_kg, Meats.rest_kg)
        values = session.execute(query_values).all()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', size=16)
        pdf.cell(0, 3, txt='Relatório Nativas Grill Estoque Carnes', ln=1, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 10)  
        for meat, usage, rest in values:
            if usage != 0.0 or rest != 0.0:
                pdf.cell(0, 7, txt=f"{meat}: USADO: {usage:.3f} | SOBRA: {rest:.3f}", ln=1, align='L')
        pdf.output('backup.pdf')
        session.execute(
            update(Meats).values(
                usage_kg=0.0,
                rest_kg=0.0
            )
        )
        session.commit()
        return FileResponse(path='backup.pdf', filename=f'Backup{date.today()}.pdf', media_type='application/pdf')
def reverse():
    with SessionLocal() as session:
        last = session.scalars(select(History).where(History.is_reversed == False).order_by(History.id.desc())).first()
        if last:
            meat = session.scalars(select(Meats).where(Meats.name == last.name)).first()
            if last.type == 'usage':
                meat.usage_kg = meat.usage_kg - last.value
            elif last.type == 'rest':
                meat.rest_kg = meat.rest_kg - last.value
            last.is_reversed = True
            session.commit()
            return {'status': 'success', 'date': last.date}
        return {'status': 'invalid'}

            

    
          
               

     
        




