from fastapi import FastAPI
from mongoengine import connect

from app.routers import products

# create an app
app = FastAPI()

# konek ke database mongodb
mongodb = connect('mongodb', host='mongodb://localhost/test_db', maxPoolSize=10)

# fungsi include_router adalah agar memudahkan dalam membuat route
# prefix adalah resource name atau awalan, jadi user.router otomatis endpoint awalannya adalah /products
# tags adalah judul untuk dokumentasi API
# format : include_router(<router>, prefix=<resource_name>, tags=<judul_dokumentasi>)
app.include_router(products.router, prefix="/products", tags=["Product Docs"], )