from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chatbot_agent import run_agent
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[str] = []

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("web/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
def chat(chat: ChatRequest):
    reply, updated_history = run_agent(chat.message, chat.history)
    return {"reply": reply, "history": updated_history}


if __name__ == "__main__":    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)