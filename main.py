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
async def openai_connector(
    apikey: str,
    body: dict):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apikey}"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)

    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

