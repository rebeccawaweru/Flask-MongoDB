from pymongo import MongoClient

"""This class will return a connection to a certain mongo database"""
class Connection:
    def __new__(cls, database):
        """new is a method called before an instance of a class is created"""
        connection = MongoClient("mongodb+srv://rebeccawaweru:turntisbae@cluster0.91mfo.mongodb.net/Realestate?retryWrites=true&w=majority")
        return connection[database]