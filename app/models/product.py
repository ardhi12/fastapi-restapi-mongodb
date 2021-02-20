from mongoengine import *

# mongoengine menggunakan model ODM (Object Document Mapper) mirip seperti ORM pada RDBMS
# Class ini akan digunakan mongoengine untuk membuat schema database
# Model ini juga terdapat validation input, jadi tidak perlu membuat model pydantic lagi
class Products(Document):
    name = StringField(max_length=50, required=True)
