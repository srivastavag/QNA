from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import os

app = FastAPI()

LLM_BACKEND_URL = "https://19788fe6e5cb.ngrok-free.app"


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head><title>Q&A Client</title></head>
    <body>
        <h2>Ask a Question</h2>
        <form method="post" action="/ask-form">
            <input type="text" name="question" size="80"/>
            <input type="submit" value="Ask"/>
        </form>
        <div style="margin-top:20px;">
            <p><i>Answer will appear below.</i></p>
            <div id="answer-box">{{ANSWER}}</div>
        </div>
    </body>
    </html>
    """


@app.post("/ask-form", response_class=HTMLResponse)
async def ask_form(question: str = Form(...)):
    try:
        response = requests.post(
            f"{LLM_BACKEND_URL}/ask",
            json={"question": question},
            timeout=60
        )
        data = response.json()
        answer = data.get("answer", "No answer received.")
    except Exception as e:
        answer = f"Error contacting backend: {str(e)}"

    # Simple HTML template response with inserted answer
    return f"""
    <html>
    <head><title>Q&A Client</title></head>
    <body>
        <h2>Ask a Question</h2>
        <form method="post" action="/ask-form">
            <input type="text" name="question" value="{question}" size="80"/>
            <input type="submit" value="Ask"/>
        </form>
        <div style="margin-top:20px;">
            <p><b>Answer:</b></p>
            <div>{answer}</div>
        </div>
    </body>
    </html>
    """


@app.post("/ask")
async def ask_api(request: Request):
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
