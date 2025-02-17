from fastapi import FastAPI, HTTPException, Response, Query
from pydantic import BaseModel
from dify_client import DifyClient
from typing import Optional, List, Dict
from config import DIFY_PLATFORMS
import argparse
import sys

app = FastAPI()

# Dify 原生 API 的请求模型
class FileInfo(BaseModel):
    type: str
    transfer_method: str
    url: str

class DifyRequest(BaseModel):
    inputs: Dict = {}
    query: str
    response_mode: str = "streaming"
    conversation_id: str = ""
    user: str = "abc-123"
    files: List[FileInfo] = []
    platform: str  # 平台参数改为必填

# 简化版的请求模型
class SimpleRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    platform: str  # 平台参数改为必填

@app.get("/platforms")
async def get_platforms():
    """获取所有可用的平台及其描述"""
    return DifyClient.get_available_platforms()

@app.get("/chat")
@app.post("/chat")
async def chat(
    request: Optional[SimpleRequest] = None,
    query: Optional[str] = None,
    platform: str = Query(None),  # 改为可选参数
):
    try:
        # 处理 GET 请求
        if request and request.query:
            # POST 请求
            message = request.query
            conversation_id = request.conversation_id
            platform = request.platform
        elif query:
            # GET 请求
            message = query
            conversation_id = None
        else:
            raise HTTPException(status_code=400, detail="Missing query parameter")

        # 验证平台参数
        if not platform:
            raise HTTPException(status_code=400, detail="Platform parameter is required")

        # 验证平台是否有效
        if platform not in DIFY_PLATFORMS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Available platforms: {list(DIFY_PLATFORMS.keys())}"
            )

        # 创建对应平台的客户端
        client = DifyClient(platform=platform)
        response = client.chat(
            message=message,
            conversation_id=conversation_id,
            stream=False
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat-messages")
async def dify_chat(request: DifyRequest):
    try:
        if request.platform not in DIFY_PLATFORMS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Available platforms: {list(DIFY_PLATFORMS.keys())}"
            )

        client = DifyClient(platform=request.platform)
        
        if request.files:
            response = client.chat_with_image(
                message=request.query,
                image_url=request.files[0].url,
                conversation_id=request.conversation_id
            )
        else:
            response = client.chat(
                message=request.query,
                conversation_id=request.conversation_id,
                stream=request.response_mode == "streaming"
            )

        if request.response_mode == "streaming":
            return Response(
                content=response,
                media_type="text/event-stream"
            )
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/messages")
async def get_history(
    conversation_id: str,
    platform: str = Query(..., description="选择平台")  # 平台参数改为必填
):
    try:
        if platform not in DIFY_PLATFORMS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid platform. Available platforms: {list(DIFY_PLATFORMS.keys())}"
            )
            
        client = DifyClient(platform=platform)
        return client.get_conversation_history(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Dify API调用工具')
    parser.add_argument('--platform', '-p', required=True,
                       help=f'指定平台名称 (可用平台: {", ".join(DIFY_PLATFORMS.keys())})')
    parser.add_argument('--message', '-m', required=True,
                       help='要发送的消息内容')
    parser.add_argument('--conversation-id', '-c',
                       help='会话ID（可选）')
    
    args = parser.parse_args()
    
    # 验证平台是否有效
    if args.platform not in DIFY_PLATFORMS:
        print(f"错误: 不支持的平台 '{args.platform}'")
        print(f"支持的平台: {', '.join(DIFY_PLATFORMS.keys())}")
        sys.exit(1)
    
    try:
        # 创建对应平台的客户端并发送消息
        client = DifyClient(platform=args.platform)
        response = client.chat(
            message=args.message,
            conversation_id=args.conversation_id,
            stream=False
        )
        print(response)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 