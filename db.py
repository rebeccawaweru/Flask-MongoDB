from pymongo import MongoClient

"""This class will return a connection to a certain mongo database"""
class Connection:
    def __new__(cls, database):
        """new is a method called before an instance of a class is created"""
        connection = MongoClient("")
        return connection[database]