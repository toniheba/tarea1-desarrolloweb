from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from database import engine, inicializar_bd
from sqlmodel import Session
from models import Estudiante
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

inicializar_bd()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/estudiantes/{matricula}", response_model=Estudiante)
def leer_estudiante(matricula:str):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return estudiante

@app.post("/estudiantes/", response_model=Estudiante, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: Estudiante):
    with Session(engine) as session:
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante

@app.delete("/estudiantes/{matricula}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(matricula:str):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado") 
            session.delete(estudiante)
            session.commit()

@app.put("/estudiantes/{matricula}", response_model=Estudiante)
def actualizar_estudiante(matricula:str, estudiantes_actualizar:Estudiante):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        estudiante.nombre = estudiantes_actualizar.nombre
        estudiante.apellido = estudiantes_actualizar.apellido
        estudiante.genero = estudiantes_actualizar.genero
        estudiante.direccion = estudiantes_actualizar.direccion
        estudiante.telefono = estudiantes_actualizar.telefono

        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)       