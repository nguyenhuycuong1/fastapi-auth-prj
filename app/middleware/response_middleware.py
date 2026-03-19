from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
from fastapi import Request
from app.schemas.response_entity import ResponseModel

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/docs","/redoc","/openapi.json")):
            return await call_next(request)
        
        try:
            response = await call_next(request)

            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                return response

            body = b""
            async for chunk in response.body_iterator:
                body += chunk
                
            try:
                data = json.loads(body)
            except:
                return response
            
            new_response = ResponseModel(
                code=response.status_code,
                message="success" if response.status_code < 400 else "error",
                data=data
            )
            return JSONResponse(
                content=new_response.model_dump(),
                status_code=response.status_code
            )
        except Exception as error:
            return JSONResponse(
                status_code=500,
                content=ResponseModel(
                    code=500,
                    message=str(error),
                    data={}
                ).model_dump()
            )