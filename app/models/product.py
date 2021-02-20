from mongoengine import *

# mongoengine menggunakan model ODM (Object Document Mapper) mirip seperti ORM pada RDBMS
# Class ini akan digunakan mongoengine untuk membuat schema database
class Products(Document):
    name = StringField(max_length=200, required=True)
