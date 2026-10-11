import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import Base, engine
from .routes import router

logging.basicConfig(level=logging.INFO)
Base.metadata.create_all(engine)
app = FastAPI(title="Credit Assistant API")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    logging.getLogger("api").exception("Unhandled error on %s", request.url.path)
    return JSONResponse({"detail": "Something went wrong on our side. Try again."}, status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}
