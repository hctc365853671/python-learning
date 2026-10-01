from fastapi import FastAPI
import llm
from chatRequest import ChatRequest
app=FastAPI()

@app.get("/ai-weather")
def aiWeather(city:str):
    return llm.getWeather(city)

@app.post("/chat")
def ai_chat(chatRequest:ChatRequest):
    return llm.get_response(chatRequest=chatRequest)