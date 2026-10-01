from fastapi import FastAPI
from openai import OpenAI

import Day11_request,Day12_llm_chat

app=FastAPI()

@app.get("/weather")
def home():
    return "hello World"

@app.get("/weather")
def cityWeather(city:str):
    return {"city":city,"msg":"查询成功"}

@app.get("/ai-weather")
def aiWeather(city:str):
    return getWeather(city)

def getWeather(city:str):
  try:
    client = Day12_llm_chat.createClient()
    print(city)
    cityWeather=Day11_request.postWeather(city)
    print(cityWeather)
    messages=[{'role':'system','content':"你是一个天气助手."},
              {'role':'user','content':f"{cityWeather}这个是该城市天气请用json格式简介自然回复明天天气温度等等"}
             ]
    completion = client.chat.completions.create(
                                                    model="qwen-plus-2025-07-28",
                                                    messages=messages
                                                )
    aiAnswer=completion.choices[0].message.content
    return aiAnswer
  except Exception as e:
    return e