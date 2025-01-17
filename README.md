# financialMongoDBVertexAiBot
Here’s a README.md template for your GitHub project that outlines the key features of your project, instructions for setup, and how to use the files you’ve provided:
<img width="850" alt="Screenshot 2025-01-17 at 14 52 56" src="https://github.com/user-attachments/assets/d1d29f31-03b5-400f-925b-5dcd06f4bffb" />


# Client Financial Assistant

A web-based interactive assistant designed to manage and analyze client financial data. The app integrates with MongoDB to store client data, provides a conversational interface to ask questions about the data, and utilizes Google Vertex AI for intelligent querying. Built with React.js for the frontend and Python (FastAPI) for the backend, this project demonstrates how to load, store, and interact with financial data.

## Project Structure

This project consists of the following key files:

1. **`generate_data.py`**: A Python script responsible for generating synthetic client data and storing it in MongoDB.
2. **`app.js`**: A React.js component that acts as the frontend, where users can interact with the financial assistant by asking questions and viewing loaded client data.
3. **`app.css`**: Contains the styles for the frontend of the application, ensuring a clean and user-friendly interface.

## Features

- **Data Generation**: Automatically generates synthetic financial data (client information, portfolios, transactions) using `generate_data.py`.
- **Interactive Assistant**: Allows users to ask questions about the loaded data using the `app.js` React interface.
- **Data Visualization**: Displays client data in a JSON format, making it easy to read and understand with the help of `ReactJson`.
- **MongoDB Integration**: Stores generated client data in a MongoDB database for persistent storage and retrieval.
- **Google Vertex AI Integration**: Uses Vertex AI for intelligent queries and responses related to the financial data.

## Prerequisites

Before running the project, ensure you have the following installed on your system:

- **MongoDB**: MongoDB should be running locally or via a cloud provider.
- **Node.js and npm**: To run the frontend React application.
- **Python and pip**: To run the backend and data generation script.
- **Google Cloud Account**: For using Google Vertex AI for embedding and question-answering functionality.

## Installation

### Backend (Python)

1. Clone the repository:
   bash
   git clone  https://github.com/darmad78/financialMongoDBVertexAiBot/edit/main/README.md
   cd client-financial-assistant

2.	Install the required Python packages:

	pip install -r requirements.txt


3.	Set up your environment variables for MongoDB and Google Cloud in the .env file:
	• MONGO_URI: Connection string for MongoDB.
	• PROJECT_ID: Your Google Cloud project ID.
	• REGION: Google Cloud region.
	• YOUR_GEMINI_API_KEY: Your API key for Vertex AI.

4.	Run the backend server:

	uvicorn backend.app.main:app --reload                               

5.	The server should be running on http://127.0.0.1:8000.

	
 Frontend (React)

1.	Navigate to the frontend directory:

	cd client-financial-assistant/frontend


2.	Install the required Node.js dependencies:

	npm install


3.	Start the frontend development server:

	npm start


4.	The frontend should be running on http://localhost:3000.

How to Use

1. Load Data

Click the “Load Data into MongoDB” button in the app to generate and load synthetic financial data into your MongoDB database. This step will populate the database with random client data, portfolios, and transactions.

2. Ask Questions

Enter a question in the text input and press “Send”. The assistant will use the data in the MongoDB database to provide an answer, powered by Google Vertex AI. You can ask questions like:
	•	“What is the portfolio allocation for this client?”
	•	“Find the 5 most common stocks held by the investors listed”

3. Toggle Data Visibility

You can toggle the visibility of the loaded data by clicking the “Show Data” or “Hide Data” button. This will display or hide the data in a formatted JSON view.

4. Clear Chat

Click the “Clear Chat” button to reset the chat history and start fresh.

Example Questions
	•	“What is the client’s total investment in Amazon?”
	•	“Show me the client’s spending history on entertainment.”

Data Model

The generated data consists of:
	•	Client Information: Personal details like name, email, risk tolerance, and investment goals.
	•	Portfolio: Investments in stocks, bonds, and other financial instruments.
	•	Transaction History: Spending categories like groceries, entertainment, bills, and transport.

Tech Stack
	•	Frontend: React.js, React JSON View
	•	Backend: Python (FastAPI)
	•	Database: MongoDB
	•	AI: Google Vertex AI (Gemini API)
	•	Styling: CSS

Troubleshooting
	•	Ensure your MongoDB instance is running and accessible with the correct URI.
	•	Verify that your Google Cloud credentials are set up correctly in your environment variables.
	•	If the React app doesn’t load, check the console for any error messages and ensure that all dependencies are installed correctly.

License

This project is licensed under the MIT License - see the LICENSE file for details.
