import llm
def get_ali_embedding(text: str,client):
    resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=text
    )
    # 返回向量 list
    return resp.data[0].embedding