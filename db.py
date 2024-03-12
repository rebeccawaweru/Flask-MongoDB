from pymongo import MongoClient
import os

"""This class will return a connection to a certain mongo database"""
class Connection:
    def __new__(cls):
        """new is a method called before an instance of a class is created"""
        connection = MongoClient(os.getenv('MONGO_URI'))
        return connection