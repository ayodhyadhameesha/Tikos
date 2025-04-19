# Tikos_Q1
 Answer and Approach for first question
This project implements a robust, scalable backend service that:
 Fetches data asynchronously from REST and GraphQL APIs
 Transforms and stores it in MongoDB  
 Serves the processed data via a RESTful API using FastAPI

 ### 1. Install dependencies

 ```bash
pip install -r requirements.txt

### 2. Start MongoDB
docker run -d -p 27017:27017 --name mongo mongo


### 3. Run ingestion script (to populate MongoDB)
python -m app.ingestion

### 4. Start FastAPI server
uvicorn app.main:app --reload

### 5. Visit in browser:
http://localhost:8000
 http://localhost:8000/users
 http://localhost:8000/docs