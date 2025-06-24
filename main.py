from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

fake_estudiantes= {
    1:{"id":1, "nombre":"Hector"},
    2:{"id":2, "nombre":"Antonio"},
    3:{"id":3, "nombre":"Carlos"},
    4:{"id":4, "nombre":"Jorge"},
    5:{"id":5,"nombre":"Adan"}
}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/estudiantes/{id}")
def read_student(id:int):
    estudiante = fake_estudiantes.get(id, {})
    if estudiante != {}:
        return estudiante
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=estudiante)
    


    