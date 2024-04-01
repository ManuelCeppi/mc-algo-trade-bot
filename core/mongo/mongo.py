import os
import requests
import pymongo

class MongoClient:
    def __init__(self):
        # Mongodb connection
        self.__mongo_client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_HOST')}:{os.environ.get('MONGO_PORT')}/") 

    def __get_database(self, database_name):
        return self.__mongo_client[database_name]

    def __get_collection(self, database_name, collection_name):
        return self.__get_database(database_name)[collection_name]
    
    def insert_one(self, database_name, collection_name, data):
        collection = self.__get_collection(database_name, collection_name)
        return collection.insert_one(data)
    
    def insert_many(self, database_name, collection_name, data):
        collection = self.__get_collection(database_name, collection_name)
        return collection.insert_many(data)
    
    def find_one(self, database_name, collection_name, query):
        collection = self.__get_collection(database_name, collection_name)
        return collection.find_one(query)
    
    def delete_one(self, database_name, collection_name, query):
        collection = self.__get_collection(database_name, collection_name)
        return collection.delete_one(query)

    def delete_many(self, database_name, collection_name, query):
        collection = self.__get_collection(database_name, collection_name)
        return collection.delete_many(query)
    
