from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request, Query
from database import engine, inicializar_bd
from sqlmodel import Session
from sqlmodel import select
from models import Estudiante
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

inicializar_bd()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs, puedes poner solo la de tu frontend si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/estudiantes/")
def leer_estudiantes(request:Request, skip:int = Query(0,ge=0),limit:int = Query(10, ge=1)):
    with Session(engine) as session:
        total = session.exec(select(Estudiante)).all()
        total_conteo = len(total)
        estudiantes_pagina = session.exec(select(Estudiante).offset(skip).limit(limit)).all()
        base_url = str(request.url).split('?')[0]
        siguiente_skip = skip + limit
        anterior_skip = max(0, skip - limit)
        siguiente_url = f"{base_url}?skip={siguiente_skip}&limit={limit}" if siguiente_skip < total_conteo else None
        anterior_url = f"{base_url}?skip={anterior_skip}&limit={limit}" if skip > 0 else None
        return{
            "count": total_conteo,
            "next": siguiente_url,
            "previus": anterior_url,
            "detail": estudiantes_pagina
        }


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
        estudiante.apellidos = estudiantes_actualizar.apellidos
        estudiante.genero = estudiantes_actualizar.genero
        estudiante.direccion = estudiantes_actualizar.direccion
        estudiante.telefono = estudiantes_actualizar.telefono

        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)