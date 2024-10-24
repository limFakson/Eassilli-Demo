from fastapi import FastAPI, Request
from . import base, base_read
from .middleware.TokenAuthMiddleware import TokenAuthMiddleware

# // Initailse fast api app
app = FastAPI()

excluded_path = ["/docs", "/openapi.json"]
app.add_middleware(TokenAuthMiddleware, excluded_path=excluded_path)

# app router caller
app.include_router(base.router, prefix="/api")
app.include_router(base_read.router, prefix="/api")


@app.get("/reload")
async def reload(request: Request):
    user = request.state.auth_user
    return {"message": f"App working nice"}
