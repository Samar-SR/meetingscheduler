from typing import List, Any

from fastapi import FastAPI
from modal import chatting
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    user_message: str


class Output(BaseModel):
    input: str
    chat_history: Any
    output: str


@app.post("/chat")
def chat_function(msg: Message):
    data = chatting(msg.user_message)
    data = Output(**data)
    return data
