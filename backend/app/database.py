from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

def init_db():
    global client, db
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client.finance_assistant_db

def get_user_transactions(user_id: str):
    transactions_collection = db.transactions
    return list(transactions_collection.find({"user_id": user_id}))

def add_transactions(transactions):
    transactions_collection = db.transactions
    transactions_collection.insert_many(transactions)