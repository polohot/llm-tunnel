import os
import uvicorn
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Form

from typing import List
import shutil
import tempfile
from llama_cloud_services import LlamaParse


app = FastAPI()

# HOME
@app.get("/")
async def root():
    return {"message": "Hello World"}

# OPENAI - NEED TO BUILD FULL BODY
@app.post("/openai")
async def openai(apikey: str, body: dict):
    # INIT HEADER
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {apikey}"}
    # CALL API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    return response.json()

# OPENAI - SINGLE QUESTION
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

# OPENAI - SEARCH SINGLE
@app.post("/openai_search_single")
async def openai_search_single(apikey: str, question: str, search_context_size: str = 'low'):
    # INIT HEADER
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {apikey}"}
    # BUILD BODY
    body = {"model": "gpt-4o-search-preview",
            'web_search_options': {'search_context_size': search_context_size},
            "messages": [{'role': 'user', 
                          'content': question}],
            }
    # CALL API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    return response.json()

# LLAMA PARSE
@app.post("/llama_parse_batch")
async def llama_parse_batch(apikey: str = Form(...), files: List[UploadFile] = File(...)):
    temp_file_paths = []
    try:
        # Save uploaded files temporarily
        for file in files:
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                temp_file_paths.append(tmp.name)
        # Call LlamaParse
        parser = LlamaParse(
            api_key=apikey,
            num_workers=4,
            verbose=True,
            language="en"
        )
        results = parser.parse(temp_file_paths)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files safely
        for path in temp_file_paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Failed to delete temp file {path}: {e}")

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

