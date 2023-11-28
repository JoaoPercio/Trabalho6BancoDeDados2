from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["concessionaria"]

# Modelos
class Marca(BaseModel):
    id: int
    nome: str
    
class MarcaEdit(BaseModel):
    nome: str


class Modelo(BaseModel):
    id: int
    id_marca: int
    nome: str
class ModeloEdit(BaseModel):
    id_marca: int
    nome: str

class Carro(BaseModel):
    id: int
    id_modelo: int
    nome: str
    renavam: int
    placa: str
    valor: float
    ano: int

class CarroEdit(BaseModel):
    id_modelo: int
    nome: str
    renavam: int
    placa: str
    valor: float
    ano: int



# Rotas CRUD para Marca
@app.post("/marca/", response_model=Marca)
async def create_marca(marca: Marca):
    marca_id = db.marca.insert_one(marca.dict()).inserted_id
    return {"id": marca_id, **marca.dict()}

@app.get("/marca/", response_model=List[Marca])
async def get_all_marcas():
    return list(db.marca.find())

@app.get("/marca/{marca_id}", response_model=Marca)
async def get_marca(marca_id: int):
    marca = db.marca.find_one({"id": marca_id})
    if marca:
        return marca
    else:
        raise HTTPException(status_code=404, detail="Marca não encontrada")

@app.put("/marca/{marca_id}", response_model=Marca)
async def update_marca(marca_id: int, marca: MarcaEdit):
    marca_existente = db.marca.find_one({"id": marca_id})
    if marca_existente:
        db.marca.update_one({"id": marca_id}, {"$set": {"nome": marca.nome}})
        marca_atualizada = db.marca.find_one({"id": marca_id})
        return Marca(**marca_atualizada)
    else:
        raise HTTPException(status_code=404, detail="Marca não encontrada")


@app.delete("/marca/{marca_id}", response_model=Marca)
async def delete_marca(marca_id: int):
    marca = db.marca.find_one({"id": marca_id})
    if marca:
        db.marca.delete_one({"id": marca_id})
        return marca
    else:
        raise HTTPException(status_code=404, detail="Marca não encontrada")

# Rotas CRUD para Modelo
@app.post("/modelo/", response_model=Modelo)
async def create_modelo(modelo: Modelo):
    modelo_id = db.modelo.insert_one(modelo.dict()).inserted_id
    return {"id": modelo_id, **modelo.dict()}

@app.get("/modelo/", response_model=List[Modelo])
async def get_all_modelos():
    return list(db.modelo.find())

@app.get("/modelo/{modelo_id}", response_model=Modelo)
async def get_modelo(modelo_id: int):
    modelo = db.modelo.find_one({"id": modelo_id})
    if modelo:
        return modelo
    else:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")

@app.put("/modelo/{modelo_id}", response_model=Modelo)
async def update_modelo(modelo_id: int, modelo: ModeloEdit):
    modelo_existente = db.modelo.find_one({"id": modelo_id})
    if modelo_existente:
        db.carro.update_one({"id": modelo_id}, {"$set": modelo.dict()})
        modelo_atualizado = db.modelo.find_one({"id": modelo_id})
        return Modelo(**modelo_atualizado)
    else:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")

@app.delete("/modelo/{modelo_id}", response_model=Modelo)
async def delete_modelo(modelo_id: int):
    modelo = db.modelo.find_one({"id": modelo_id})
    if modelo:
        db.modelo.delete_one({"id": modelo_id})
        return modelo
    else:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")

# Rotas CRUD para Carro
@app.post("/carro/", response_model=Carro)
async def create_carro(carro: Carro):
    carro_id = db.carro.insert_one(carro.dict()).inserted_id
    return {"id": carro_id, **carro.dict()}

@app.get("/carro/", response_model=List[Carro])
async def get_all_carros():
    return list(db.carro.find())

@app.get("/carro/{carro_id}", response_model=Carro)
async def get_carro(carro_id: int):
    carro = db.carro.find_one({"id": carro_id})
    if carro:
        return carro
    else:
        raise HTTPException(status_code=404, detail="Carro não encontrado")

@app.put("/carro/{carro_id}", response_model=Carro)
async def update_carro(carro_id: int, carro: CarroEdit):
    carro_existente = db.carro.find_one({"id": carro_id})
    if carro_existente:
        db.carro.update_one({"id": carro_id}, {"$set": carro.dict()})
        carro_atualizado = db.carro.find_one({"id": carro_id})
        return Carro(**carro_atualizado)
    else:
        raise HTTPException(status_code=404, detail="Carro não encontrado")

@app.delete("/carro/{carro_id}", response_model=Carro)
async def delete_carro(carro_id: int):
    carro = db.carro.find_one({"id": carro_id})
    if carro:
        db.carro.delete_one({"id": carro_id})
        return carro
    else:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
