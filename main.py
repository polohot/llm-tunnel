import os
import uvicorn
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/openai")
async def openai(apikey: str, body: dict):
    # INIT HEADER
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {apikey}"}
    # CALL API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    return response.json()

@app.post("/openai_single")
async def openai_single(apikey: str, question: str):
    # INIT HEADER
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {apikey}"}
    # BUILD BODY    
    body = {"model": "gpt-4o",
            "messages": [{'role': 'user', 
                          'content': question}],
            "max_tokens": 1000}
    # CALL API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    return response.json()



# @app.post("/deepseek")
# async def deepseek(apikey: str, body: dict):
#     # INIT HEADER
#     headers = {"Content-Type": "application/json",
#                "Authorization": f"Bearer {apikey}"}
#     # CALL API
#     response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=body)
#     return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

