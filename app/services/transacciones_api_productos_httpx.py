import httpx
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


# LISTAR PRODUCTOS desde FastAPI
# GET /products/?limit=500&offset=0
# Retorna: {"total": X, "items": [...]}
async def list_products(limit: int = 500, offset: int = 0) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/products/",
            params={"limit": limit, "offset": offset}
        )
    response.raise_for_status()
    return response.json()


# OBTENER PRODUCTO POR ID
# GET /products/{product_id}
async def get_product(product_id: str) -> Dict | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products/{product_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


# CREAR PRODUCTO
# POST /products/
async def create_product(producto: Dict) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/products/", json=producto)
    response.raise_for_status()
    return response.json()


# ACTUALIZAR PRODUCTO
# PUT /products/{product_id}
async def update_product(product_id: str, datos: Dict) -> Dict | None:
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/products/{product_id}", json=datos)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


# ELIMINAR PRODUCTO
# DELETE /products/{product_id}
async def delete_product(product_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/products/{product_id}")
    if response.status_code == 404:
        return False
    response.raise_for_status()
    return True
