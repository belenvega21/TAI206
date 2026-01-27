from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def HolaUPQ():
    return {"mensaje": "HolaUPQ estoy en FastAPI"}

@app.get("/bienvenidos")
async def bienvenidos():
    return {"mensaje": "Bienvenidos a tu API REST"}
