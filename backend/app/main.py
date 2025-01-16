from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from .database import init_db, get_user_transactions
from data.generate_data import generate_embedding,generate_client
from google.cloud import aiplatform
from app.generativeAI import generate_content 
import os
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import pymongo
import json
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import html  # Import the html module

# Custom function to handle non-serializable objects like ObjectId
def json_serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    raise TypeError(f"Type {type(obj)} not serializable")

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["financial_db"]
collection = db["transactions"]

@app.get("/check_env")
def check_env():
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri:
        return {"message": "MONGO_URI is loaded", "MONGO_URI": mongo_uri}
    else:
        return {"error": "MONGO_URI not found"}
# Initialize Google Vertex AI client

vertex_client = aiplatform.gapic.PredictionServiceClient()

@app.on_event("startup")
def startup():
    init_db()  # Initialize MongoDB connection
@app.get("/")
def read_root():
    return {"message": "Welcome to the Transaction API"}
def json_escape_values(data):
    """HTML encode the values of a JSON object."""
    if isinstance(data, dict):
        return {key: json_escape_values(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [json_escape_values(item) for item in data]
    elif isinstance(data, str):
        return html.escape(data)  # HTML-encode string values
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    else:
        return data
@app.post("/load_client")
async def load_client_endpoint():
    try:
        print("Loading clients")
        transactions = generate_client()  # Generate a new client transactions
        
        # Ensure transactions are not empty
        if not transactions:
            return {"message": "No data to load."}
        
        collection = db["clients"]
        inserted_data_str=""
        # Insert generated data into MongoDB
        try:
            x = collection.insert_one(transactions)
            inserted_data = collection.find_one({"_id": x.inserted_id})
            # Apply HTML escaping to the values before passing to ReactJson
            inserted_data_str = json_escape_values(inserted_data)
            
            #inserted_data_str = json.dumps(inserted_data, default=str)  # Convert back to JSON string
           
            #inserted_data_str = json.dumps(inserted_data, default=json_serialize)
            # Convert the inserted data to a string (JSON format)
            result = "Data loaded successfully"
        except Exception as e:
            result = "Error loading data: " + str(e)
    
    except Exception as e:
        return {"error": str(e)}
    print(inserted_data_str)
    return {"message": result,
            "data": inserted_data_str  # Return the actual inserted data
            }

@app.post("/ask_question/")
async def ask_question(request: Request):
    try:
      
      
      
        data = await request.json()
        question = data.get("question", "")
        #print("Question:", question)
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        prompt = f"short answers, Question: {question}\n\nContext:\n"

        #Step1: Do I need to pull data, if yes, I go to step 2 else I go to step 3
        #ask aI to choose
        # Define the client attributes for the decision prompt
        client_attributes = """clientId,name,email,phone,address,portfolio,investment Amount,
                            investment Date,stock Holdings,bond Holdings,risk Profile,
                            preferred Contact Method,date Of Birth,gender,marital Status,
                            occupation,financial Goals,account Status"""

        # Construct the decision prompt
        decision_prompt = f"""if the question talks about clients, and it is about 
                            any of these client attributes: {client_attributes}, 
                            then answer: "YES" 
                            otherwise answer: "NO" 

                            Question: {question}"""
        decision = generate_content(decision_prompt)
        print(decision)
        
        if "YES" in decision :

            # Step 2: Generate vector embedding for the question
            question_embedding = generate_embedding(question)

            collection = db["clients"]

            # Step 3: Perform vector search in MongoDB
            search_query = [ {'$vectorSearch': {
                        'queryVector': question_embedding['embedding'],
                        'path': 'embedding', 
                        'numCandidates': 50, 
                        'index': 'vector_index', 
                        'limit': 50
                                }
                        },
                        {
                        '$project': {
                            '_id': 0, 
                            'embedding': 0
                        }
                        }]
            #print(search_query)

            search_results = list(collection.aggregate(search_query))

            if not search_results:
                return JSONResponse(
                    content={"answer": "No relevant documents found"}, status_code=200
                )
            
            #print(search_results)
            # Step 3: Send MongoDB results to Vertex AI for response generation

            #print(search_results)
            #prompt = f"short answers, Question: {question}\n\nContext:\n"

            for result in search_results:
                try:
                    # Extract basic details
                    first_name = result.get("firstName", "N/A")
                    last_name = result.get("lastName", "N/A")
                    email = result.get("email", "N/A")
                    risk_tolerance = result.get("riskTolerance", "N/A")
                    investment_goals = result.get("investmentGoals", {})
                    portfolio = result.get("portfolioAllocation", [])

                    # Summarize investment goals
                    retirement = investment_goals.get("retirement", "N/A")
                    downpayment = investment_goals.get("downpayment", "N/A")
                    other_goals = ", ".join(investment_goals.get("otherGoals", []))

                    # Summarize portfolio
                    portfolio_summary = "\n".join(
                        [f"  - {alloc['stock'].get('stock', 'N/A')} ({alloc['stock'].get('ticker', 'N/A')}): {alloc['shares']} shares"
                        if isinstance(alloc.get("stock"), dict) else
                        f"  - {alloc['stock']}: {alloc['shares']} shares"
                        for alloc in portfolio]
                    )

                    # Construct the document summary
                    document_summary = (
                        f"Investor: {first_name} {last_name} (Email: {email})\n"
                        f"Risk Tolerance: {risk_tolerance}\n"
                        f"Investment Goals:\n"
                        f"  - Retirement: {retirement}\n"
                        f"  - Downpayment: {downpayment}\n"
                        f"  - Other Goals: {other_goals}\n"
                        f"Portfolio Allocation:\n{portfolio_summary}\n"
                    )

                    # Append to the prompt
                    prompt += f"{document_summary}\n"
                except Exception as e:
                    print("Error processing result:", e)

            prompt += f"elaborate the question with the data provided\n"
            prompt += f"Add a return line at end of each line\n"
        answer = generate_content(prompt)
        
        return JSONResponse(content={"answer": answer}, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=500
        )