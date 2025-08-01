from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.qa_engine import answer_question

app = FastAPI()

@app.post("/ask")
async def ask_question(request: Request):
    question = await request.body()
    question = question.decode("utf-8").strip()

    print(f"\nQ: {question}")
    str_answer = answer_question(question)
    print(f"A: {str_answer}")

    return JSONResponse(content={"answer": str_answer})
