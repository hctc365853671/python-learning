import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from chatRequest import ChatRequest
import rag


def createClient():
    load_dotenv()
    api_key=os.getenv("QWEN_KEY")
    client = OpenAI(
                        api_key=api_key,  # 请用阿里云百炼 API Key
                        base_url="https://ws-7h0jau08ma2r8dha.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                    )
    return client

def get_response(chatRequest: ChatRequest, collection,client):
    try:
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的产品助手。请严格根据参考资料回答，不要编造。如果资料不足，请回答：根据现有资料无法回答。"
            },
            {
                "role": "user",
                "content": f"{chatRequest.content}"
            }
        ]
        tools=[
            {
                    "type": "function",
                    "function": {
                        "name": "getCorrelation",
                        "description": "在知识库中查询与问题相关的内容",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "question": {
                                    "type": "string",
                                    "description": "用户输入的问题"
                                }
                            },
                            "required": ["question"]
                        }
                    }
            }
        ]
        while True:
            response=client.chat.completions.create(
                model="qwen-plus-2025-07-28",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            msg=response.choices[0].message
            if msg.tool_calls:
                messages.append(msg)
                for tool_call in msg.tool_calls:
                    question = json.loads(tool_call.function.arguments).get("question")
                    if tool_call.function.name == "getCorrelation":
                        tool_result = rag.getCorrelation(question, collection, client)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": "\n".join(tool_result)
                        })
            else:
                return {
                            "code": 200,
                            "message": "success",
                            "data": msg.content
                        }
               
    except Exception as e:
        return {"code": 500, "message": str(e)}