from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import user, login
from app.middleware.response_middleware import ResponseMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(ResponseMiddleware)

app.include_router(user.router)
app.include_router(user.public_router)
app.include_router(login.router)