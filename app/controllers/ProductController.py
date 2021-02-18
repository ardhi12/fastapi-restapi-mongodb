from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.user import Users
from app.transformers import UserTransformer


class ProductController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            products = Products.objects()
            transformer = UserTransformer.transform(products)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            if name == "":
                raise Exception("name couldn't be empty!")

            product = Products(name=name)
            product.save()
            transformer = ProductTransformer.singleTransform(product)
            return response.ok(transformer, "Berhasil Membuat Produk!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            product = Product.objects(id=id).first()

            if product is None:
                raise Exception('produk tidak ditemukan!')

            transformer = ProductTransformer.singleTransform(product)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            if name == "":
                raise Exception("name couldn't be empty!")

            product = Products.objects(id=id).first()

            if product is None:
                raise Exception('product tidak ditemukan!')

            product.name = name
            product.save()

            transformer = ProductTransformer.singleTransform(product)
            return response.ok(transformer, "Berhasil Mengubah Produk!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:

            product = Products.objects(id=id).first()

            if product is None:
                raise Exception('produk tidak ditemukan!')

            product.delete()
            return response.ok('', "Berhasil Menghapus Produk!")
        except Exception as e:
            return response.badRequest('', f'{e}')
