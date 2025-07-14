from sqlmodel import SQLModel, Field

class Estudiante(SQLModel, table=True):
    matricula:str = Field(default=None, primary_key=True)
    nombre:str
    apellidos:str
    genero:str
    direccion:str
    telefono:str