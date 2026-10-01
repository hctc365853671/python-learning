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
        related = rag.getCorrelation(chatRequest, collection,client)
        
        if not related:
            return {
                "code": 200,
                "message": "success",
                "data": "根据现有资料无法回答"
            }
        
        reference = "\n".join(related)
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的产品助手。请严格根据参考资料回答，不要编造。如果资料不足，请回答：根据现有资料无法回答。"
            },
            {
                "role": "user",
                "content": f"参考资料：\n{reference}\n\n用户问题：{chatRequest.content}"
            }
        ]
        
        completion = client.chat.completions.create(
            model="qwen-plus-2025-07-28",
            messages=messages
        )
        
        return {
            "code": 200,
            "message": "success",
            "data": completion.choices[0].message.content
        }
    except Exception as e:
        return {"code": 500, "message": str(e)}