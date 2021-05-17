from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import time

from app.api.routes.user import router as user_router
from app.api.routes.authentification import router as auth_router
from app.api.middlewares.process_time import ProcessTimeMiddleWare
from app.api.dependencies.login import get_current_actif_user

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1"
]

app = FastAPI(title="Rest-API",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProcessTimeMiddleWare)

app.include_router(user_router, tags=[
                   "User"], prefix="/user", dependencies=[Depends(get_current_actif_user)])
app.include_router(auth_router, tags=["Auth"], prefix="/auth")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Octogone Project!"}
