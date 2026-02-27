from fastapi import FastAPI, HTTPException
from models import Libro, Prestamo
from data import libros, prestamos

app = FastAPI(title="API Biblioteca Digital")

@app.post("/libros", status_code=201)
def registrar_libro(libro: Libro):
    for l in libros:
        if l.nombre.lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="Libro ya registrado")
    libros.append(libro)
    return libro

@app.get("/libros")
def listar_libros():
    return libros

@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in libros:
        if libro.nombre.lower() == nombre.lower():
            return libro
    raise HTTPException(status_code=400, detail="Libro no encontrado")

@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    for libro in libros:
        if libro.nombre == prestamo.libro:
            if libro.estado == "prestado":
                raise HTTPException(status_code=409, detail="Libro ya prestado")
            libro.estado = "prestado"
            prestamos.append(prestamo)
            return {"mensaje": "Préstamo registrado"}
    raise HTTPException(status_code=400, detail="Libro no válido")

@app.put("/prestamos/devolver/{nombre}")
def devolver_libro(nombre: str):
    for libro in libros:
        if libro.nombre == nombre:
            libro.estado = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}
    raise HTTPException(status_code=409, detail="Préstamo no existe")

@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):
    for prestamo in prestamos:
        if prestamo.libro == nombre:
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}
    raise HTTPException(status_code=409, detail="Registro de préstamo no existe")