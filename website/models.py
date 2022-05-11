from pymongo import MongoClient
import certifi


cluster = MongoClient("mongodb+srv://GianITS:ProjectITS33@clusterits.do6lt.mongodb.net", tlsCAFile=certifi.where())
db = cluster['Agenzia_Immo']
clients_collection = db['Clienti']
properties_collection = db['Immobili']
agents_collection = db['Agenti']


class Agent():
    def __init__(self, firstName, lastName, userName, password):
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.password = password

    def __repr__(self):
        return (f"Agente: {self.firstName} {self.lastName}, Username: {self.userName}, Password: {self.password}")

class Client():
    def __init__(self, firstName, lastName, email, phoneNum, city):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNum = phoneNum
        self.city = city

    def __repr__(self):
        return (f"Nome: {self.firstName}, Cognome: {self.lastName}, Email: {self.email}, Cellulare: {self.phoneNum}, Citta di residenza: {self.city}")

class Property():
    def __init__(self, ownerName, squareMeters, roomNum, address, city, agent, **images):
        self.ownerName = ownerName
        self.squareMeters = squareMeters
        self.roomNum = roomNum
        self.address = address
        self.city = city
        self.agent = agent
        self.images = images

    def __repr__(self):
        #return (f"Nome: {self.firstName}, Cognome: {self.lastName}, Email: {self.email}, Cellulare: {self.phoneNum}, Citta di residenza: {self.city}")
        pass