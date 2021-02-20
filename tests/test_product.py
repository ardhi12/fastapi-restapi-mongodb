"""
Command execute : pytest tests/
"""
from unittest import TestCase

import json
from bson import ObjectId

from mongoengine import connect, disconnect
from fastapi.testclient import TestClient

from app import app
from app.models.product import Products


# TestClient berfungsi untuk menjalankan FastAPI tanpa uvicorn
client = TestClient(app)


class TestProduct(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        - Mongomock adalah database mocking (seolah-olah terkoneksi ke mongodb)
        - fungsi ini digunakan untuk melakukan koneksi ke Mongomock
        - fungsi ini akan eksekusi saat pertama kali dijalankan
        step :
        1. disconnect dari mongodb, karena sebelumnya app sudah terkoneksi dengan mongodb pada file __init__.py
        2. connect ke mongomock
        """
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/mocking_db')

    @classmethod
    def tearDownClass(cls):
        """            
        - fungsi ini akan eksekusi saat seluruh test selesai dijalankan. 
        - fungsi ini untuk melakukan disconnect dari mongomock
        """
        disconnect()
    
    # fungsi untuk test
    def test_read_all_products(self):                             
        response = client.get("/products")                
        assert response.status_code == 200  
        
    def test_read_product_with_id(self):                     
        response = client.get("/products")                
        
        res = response.text
        res = json.loads(res)
        res = res['datas']        
        
        for x in res:
            response = client.get(f"/products/{x['id']}")                
            print(response.text)
            assert response.status_code == 200                    
    
    def test_insert_product(self):
        name = "Tahu Bulat"

        # hit endpoint
        response = client.post("/products", json={"name": name})
        # assert berfungsi untuk testing. jika assert hasilnya False, maka akan mengembalikan nilai error    
        assert response.status_code == 200

        product = Products.objects(name=name).first()
        assert product.name == name
        
    def test_insert_product_long_name(self):
        name = "amamamamamamamamamamamamamamamamamamamamamamamamamamamamamamamamamam"

        # hit endpoint
        response = client.post("/products", json={"name": name})
        # assert berfungsi untuk testing. jika assert hasilnya False, maka akan mengembalikan nilai error    
        assert response.status_code == 400

    def test_insert_product_empty_name(self):
        name = ""

        # hit endpoint
        response = client.post("/products", json={"name": name})
        # assert berfungsi untuk testing. jika assert hasilnya False, maka akan mengembalikan nilai error    
        assert response.status_code == 400
    
    def test_insert_product_non_string_datatype(self):
        name = 1

        # hit endpoint
        response = client.post("/products", json={"name": name})
        # assert berfungsi untuk testing. jika assert hasilnya False, maka akan mengembalikan nilai error    
        assert response.status_code == 400
        
    def test_insert_product_without_name_parameter(self):
        response = client.post("/products", json={})
        assert response.status_code == 400
        
    def test_update_product(self):
        # insert 1 data
        name = "Indomie"        
        response = client.post("/products", json={"name": name})
        
        # get id from response
        res = response.text
        res = json.loads(res)
        id = res['datas']['id']

        # update name
        new_name = "Sarimi"
        response = client.put(f"/products/{id}", json={"name": new_name})
        assert response.status_code == 200

        product = Products.objects(id=id).first()
        assert product.name == new_name
        
    def test_update_product_long_name(self):        
        # insert 1 data
        name = "Indomie"
        response = client.post("/products", json={"name": name})
        
        # get id from response
        res = response.text
        res = json.loads(res)
        id = res['datas']['id']

        # update name
        new_name = "SarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimiSarimi"
        response = client.put(f"/products/{id}", json={"name": new_name})
        assert response.status_code == 400
        
    def test_update_product_with_wrong_id(self):
        # insert 1 data
        name = "Indomie"
        response = client.post("/products", json={"name": name})
        
        # create new ObjectId
        id = str(ObjectId())
        # print hanya akan muncul ketika test fail
        print(id)

        # update name
        new_name = "Sarimi"
        response = client.put(f"/products/{id}", json={"name": new_name})
        assert response.status_code == 400
        
    def test_update_product_without_name(self):
        # insert 1 data
        name = "Indomie"        
        response = client.post("/products", json={"name": name})
        
        # get id from response
        res = response.text
        res = json.loads(res)
        id = res['datas']['id']

        # update name        
        response = client.put(f"/products/{id}", json={})
        assert response.status_code == 400

        product = Products.objects(id=id).first()
        assert product.name == name
        
    def test_update_product_with_empty_name(self):
        # insert 1 data
        name = "Indomie"        
        response = client.post("/products", json={"name": name})
        
        # get id from response
        res = response.text
        res = json.loads(res)
        id = res['datas']['id']

        # update name
        new_name = ""
        response = client.put(f"/products/{id}", json={"name": new_name})
        assert response.status_code == 400

        product = Products.objects(id=id).first()
        assert product.name == name
        
    def test_delete_product(self):
        # insert 1 data
        name = "Indomie"        
        response = client.post("/products", json={"name": name})
        
        # get id from response
        res = response.text
        res = json.loads(res)
        id = res['datas']['id']

        # delete data        
        response = client.delete(f"/products/{id}")
        assert response.status_code == 200
        
        # check product is not available
        product = Products.objects(id=id).first()
        assert product is None
        
    def test_delete_product_wrong_id(self):
        # insert 1 data
        name = "Indomie"        
        response = client.post("/products", json={"name": name})
        
        # get id from response
        id = str(ObjectId())

        # delete data        
        response = client.delete(f"/products/{id}")
        assert response.status_code == 400      