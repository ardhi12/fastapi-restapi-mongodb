from fastapi import APIRouter, Request

from app.controllers.ProductController import ProductController as controller

# APIRouter berfungsi untuk membuat path operation(action) sesuai dengan resource agar terorganisir dengan baik
# router ini sudah berisi resource name yaitu /products karena sudah di set pada include_router di app -> __init__.py
router = APIRouter()

# tambahkan path operation (contoh: /{id})
# tags digunakan untuk judul pada dokumentasi API
# Request berfungsi untuk mengambil semua data dari request yg dibuat. contoh : body, Endpoint, Header, dll
@router.get("")
async def action(request: Request):
    return await controller.index(request)


@router.get("/{id}")
async def action(id: str):
    return await controller.show(id)


@router.post("")
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}")
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}")
async def action(id: str):
    return await controller.delete(id)