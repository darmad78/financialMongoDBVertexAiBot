import random
import faker
from datetime import datetime, timedelta
import os
from google.cloud import aiplatform
from google.auth import credentials
import pymongo
import json
import google.generativeai as genai
from sklearn.decomposition import PCA


fake = faker.Faker()
# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["financial_db"]
collection = db["clients"]

categories = ["groceries", "entertainment", "bills", "transport"]
merchants = ["Walmart", "Netflix", "Shell", "Amazon", "McDonald's"]
bond_pool = ["BondA", "BondB"]
stocks_pool = [
    {"stock": "Amazon", "ticker": "AMZN"},
    {"stock": "Shell", "ticker": "SHEL"},
    {"stock": "Tesla", "ticker": "TSLA"},
    {"stock": "Apple", "ticker": "AAPL"},
    {"stock": "Netflix", "ticker": "NFLX"},
    {"stock": "Microsoft", "ticker": "MSFT"},
    {"stock": "Google", "ticker": "GOOG"},
    {"stock": "Meta", "ticker": "META"},
    {"stock": "NVIDIA", "ticker": "NVDA"},
    {"stock": "Visa", "ticker": "V"},
    {"stock": "Coca-Cola", "ticker": "KO"},
    {"stock": "Pepsi", "ticker": "PEP"},
    {"stock": "Walmart", "ticker": "WMT"},
    {"stock": "Nike", "ticker": "NKE"},
    {"stock": "Johnson & Johnson", "ticker": "JNJ"},
    {"stock": "Intel", "ticker": "INTC"},
    {"stock": "Disney", "ticker": "DIS"},
    {"stock": "Berkshire Hathaway", "ticker": "BRK.A"},
    {"stock": "Exxon Mobil", "ticker": "XOM"},
    {"stock": "Pfizer", "ticker": "PFE"},
    {"stock": "McDonald's", "ticker": "MCD"},
    {"stock": "PepsiCo", "ticker": "PEP"},
    {"stock": "Lockheed Martin", "ticker": "LMT"},
    {"stock": "Caterpillar", "ticker": "CAT"},
    {"stock": "Salesforce", "ticker": "CRM"},
    {"stock": "AbbVie", "ticker": "ABBV"},
    {"stock": "Bristol-Myers Squibb", "ticker": "BMY"},
    {"stock": "Home Depot", "ticker": "HD"},
    {"stock": "Starbucks", "ticker": "SBUX"},
    {"stock": "Goldman Sachs", "ticker": "GS"},
    {"stock": "Morgan Stanley", "ticker": "MS"}
]
# Vertex AI setup using gcloud authentication
# Replace with your actual project ID and region
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION") 
YOUR_GEMINI_API_KEY = os.getenv("YOUR_GEMINI_API_KEY")
genai.configure(api_key=YOUR_GEMINI_API_KEY) 


def generate_portfolio():
    num_stocks = random.randint(5, min(100, len(stocks_pool)))  # Ensure num_stocks is never larger than available stocks
    portfolio = []
    chosen_stocks = random.sample(stocks_pool, num_stocks)  # Sample the stocks without exceeding the pool size
    for stock in chosen_stocks:
        portfolio.append({"stock": stock, "shares": random.randint(5, 100)})
    
    num_bonds = random.randint(0, 2)
    chosen_bonds = random.sample(bond_pool, num_bonds)
    for bond in chosen_bonds:
        portfolio.append({"stock": bond, "shares": random.randint(5, 50)})
    
    return portfolio

def generate_embedding(portfolio):
    # Convert portfolio into a string or JSON-like format to send to Vertex AI for embedding generation
    portfolio_str = json.dumps(portfolio)
    
    # Call the Vertex AI API for embedding generation (assumes you have a model deployed)
    embedding_response = genai.embed_content(
      model="models/embedding-001", 
      content=portfolio_str
    )
    #print(embedding_response)
    
    return embedding_response

def generate_client():
    client_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "riskTolerance": random.choice(["Low", "Medium", "High"]),
        "investmentGoals": {
            "retirement": fake.date_this_century().strftime("%Y-%m-%d"),  # Convert date to string
            "downpayment": round(random.uniform(10000.0, 50000.0), 2),
            "otherGoals": random.sample(["Education", "Travel", "Home Improvement", "Vacation"], random.randint(1, 3))
        },
        "portfolioAllocation": generate_portfolio(),
    }

    # Generate Vertex AI embedding for the client data
    embedding = generate_embedding(client_data)
    client_data["embedding"] = embedding['embedding']  # Add the embedding to the data

    return client_data


# Generate and insert a new client into MongoDB