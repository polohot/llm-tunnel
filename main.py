import uvicorn
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/openai")
async def callopenai(body, apikey):
    """
    EXAMPLE HEADER
    ==============
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {apikey}"
    }

    EXAMPLE BODY
    ============
    body = {
        "model": "gpt-4o",
        "messages": [
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
    "max_tokens": 1000
    }    
    """ 
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {apikey}"
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)