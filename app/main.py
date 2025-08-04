from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

LLM_BACKEND_URL = "https://19788fe6e5cb.ngrok-free.app"

@app.post("/ask")
async def ask_question(request: Request):
    question = await request.body()
    question = question.decode("utf-8").strip()

    try:
        response = requests.post(
            f"{LLM_BACKEND_URL}/ask",
            json={"question": question},
            timeout=60
        )
        data = response.json()
        answer = data.get("answer", "Error: No answer returned.")
    except Exception as e:
        answer = f"Error: Could not contact local backend: {str(e)}"

    return JSONResponse(content={"answer": answer})
