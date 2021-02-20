from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.product import Products
from app.transformers import ProductTransformer

# Controller digunakan untuk melakukan aksi CRUD 
# return pada setiap fungsi adalah JSONResponse
class ProductController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        """
        index digunakan untuk get all data (READ)
        """
        try:
            # query select all
            products = Products.objects()
            # parsing object products ke transform
            transformer = ProductTransformer.transform(products)
            return response.ok("Products successfully retrieved", transformer)
        except Exception as e:
            return response.badRequest(f'{e}', None)

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        """
        store digunakan untuk menyimpan data (CREATE)
        """
        try:
            # get name on body request
            body = await request.json()
            name = body['name']

            if name == "":
                # message error
                raise Exception("Name couldn't be empty")
            
            # query insert
            product = Products(name=name)
            # simpan
            product.save()
            transformer = ProductTransformer.singleTransform(product)
            return response.ok("Product successfully created", transformer)
        except Exception as e:
            return response.badRequest(f'{e}')

    @staticmethod
    async def show(id: str) -> JSONResponse:
        """
        show digunakan untuk get data dengan id spesifik (READ)
        """
        try:
            # query select where id
            product = Products.objects(id=id).first()

            if product is None:
                # message error
                raise Exception('No products found with this ID')

            transformer = ProductTransformer.singleTransform(product)
            return response.ok("Product successfully retrieved", transformer)
        except Exception as e:
            return response.badRequest(f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        """
        update digunakan untuk merubah data (UPDATE)
        """
        try:
            body = await request.json()
            name = body['name']

            if name == "":
                # message error
                raise Exception("Name couldn't be empty!")
            
            # query select where id
            product = Products.objects(id=id).first()

            if product is None:
                # message error
                raise Exception('No products found with this ID')

            # isi field name dengan value name pada request
            product.name = name
            product.save()

            transformer = ProductTransformer.singleTransform(product)
            return response.ok("Product successfully updated", transformer)
        except Exception as e:
            return response.badRequest(f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        """
        delete digunakan untuk menghapus data (DELETE)
        """
        try:

            product = Products.objects(id=id).first()

            if product is None:
                raise Exception('No products found with this ID')

            product.delete()
            return response.ok("Product successfully deleted")
        except Exception as e:
            return response.badRequest(f'{e}')
