from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.routers.chat import router as chat_router
from app.routers.pages import router as pages_router
from app.services.gemini import get_client

load_dotenv()

app = FastAPI(title="MoodMate", version="0.1.0")

app.add_middleware(	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router)
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

@app.get("/healthz")
async def health():
	return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
	# Initialize Gemini client on startup to load API key
	_ = get_client()
	start_scheduler(app)

@app.on_event("shutdown")
async def on_shutdown():
	shutdown_scheduler()

