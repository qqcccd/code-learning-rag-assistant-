from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from llm.code_analyzer import analyze_code
from rag.vector_db import similarity_search
from rag.qa_chain import rag_qa_chain

load_dotenv()

app = FastAPI(
    title="代码学习智能审查助手",
    description="基于RAG与大模型的编程答疑系统后端接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeAnalyzeRequest(BaseModel):
    code: str
    language: str = "Python"

class RagRetrieveRequest(BaseModel):
    question: str
    top_k: int = 10

class RagQARequest(BaseModel):
    question: str
    code_context: str = ""

@app.get("/", tags=["健康检查"])
async def health_check():
    return {
        "status": "ok",
        "service": "代码学习智能审查助手后端服务",
        "version": "1.0.0"
    }

@app.post("/api/code-analysis", tags=["核心功能接口"])
async def code_analysis(request: CodeAnalyzeRequest):

    if not request.code.strip():
        raise HTTPException(status_code=400, detail="代码内容不能为空")

    try:
        result = analyze_code(request.code, request.language)

        return {
            "code": 200,
            "message": "代码分析成功",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代码分析失败：{str(e)}")

@app.post("/api/rag-retrieve", tags=["核心功能接口"])
async def rag_retrieve(request: RagRetrieveRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="查询问题不能为空")

    try:
        results = similarity_search(request.question, request.top_k)

        return {
            "code": 200,
            "message": "检索成功",
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检索失败：{str(e)}")

@app.post("/api/rag-qa", tags=["核心功能接口"])
async def rag_qa(request: RagQARequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        result = rag_qa_chain(request.question, request.code_context)

        return {
            "code": 200,
            "message": "问答生成成功",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问答生成失败：{str(e)}")

if __name__ == "__main__":

    import uvicorn
    import os

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host=host, port=port)