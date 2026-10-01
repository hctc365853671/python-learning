import chromadb
import models
from chatRequest import ChatRequest


def collectionAdd(collection,knowledge_base,client):
    ragLIst=models.get_ali_embedding(knowledge_base,client)
    current=collection.count()
    collection.add(
        embeddings=ragLIst,
        documents=knowledge_base,
        ids=[f"doc__{current+i+1}" for i in range(len(knowledge_base))]
        
    )
    print(f"成功追加{len(knowledge_base)}条数据")
    

def depositRag(knowledge_base:list[str],client):
    chroma_client=chromadb.PersistentClient("./chroma_db")
    try:
        collection=chroma_client.get_collection(name="product_knowledge")
        # 判断集合里面有没有数据
        count = collection.count()
        if count > 0:
            print("向量库已有数据，跳过入库")
            return collection
    except:
        collection=chroma_client.create_collection(name="product_knowledge",metadata={"hnsw:space":"cosine"})

    oneNum=1
    for i in knowledge_base:
        collection.add(
            embeddings=[models.get_ali_embedding(i,client)],
            documents=[i],
            ids=[f"doc__{str(oneNum)}"],
        )
        oneNum+=1
    print(f"入库完成，共{len(knowledge_base)}条")
    return collection

def getCorrelation(chatRequest:ChatRequest,collection,client):
    requestRag=models.get_ali_embedding(chatRequest.content,client)
    requry=collection.query(
        query_embeddings=[requestRag],
        n_results=3     
    )
    return requry["documents"][0]

def build_knowledge_base(manual, chunk_size=100, overlap=20):
    knowledge_base = []
    
    for title, content in manual.items():
        # 把标题和内容拼在一起，检索时更有上下文
        full_text = f"{title}{content}"
        
        start = 0
        while start < len(full_text):
            end = start + chunk_size
            chunk = full_text[start:end]
            knowledge_base.append(chunk)
            start += chunk_size - overlap
            
    return knowledge_base