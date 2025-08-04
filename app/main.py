from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
import requests
import os
import json

ALLOWED_IPS = set(json.loads(os.environ.get("ALLOWED_IPS", "[]")))


class IPAllowMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        if client_ip not in ALLOWED_IPS:
            return PlainTextResponse(
                f"Access denied for IP {client_ip}",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return await call_next(request)

app = FastAPI()
app.add_middleware(IPAllowMiddleware)

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
