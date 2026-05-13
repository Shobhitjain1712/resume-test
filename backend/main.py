import asyncio
import sys
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from db import init_db, get_profile, save_profile

load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

APP_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = APP_DIR.parent / "frontend"

app = FastAPI(title="Resume Tailor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


class Contact(BaseModel):
    phone: str
    email: str
    linkedin: str
    github: str


class Education(BaseModel):
    school: str
    dates: str
    degree: str
    specialization: str
    gpa: str


class Experience(BaseModel):
    company: str
    dates: str
    role: str
    location: str
    bullets: List[str]


class Project(BaseModel):
    name: str
    bullets: List[str]


class Profile(BaseModel):
    name: str
    contact: Contact
    skills: List[str]
    education: List[Education]
    achievements: List[str]
    experience: List[Experience]
    projects: List[Project]


class GenerateRequest(BaseModel):
    job_title: str = Field(..., min_length=2)
    job_description: str = Field(..., min_length=20)


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/")
async def serve_frontend():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


@app.get("/api/profile", response_model=Profile)
async def read_profile() -> dict:
    return await get_profile()


@app.put("/api/profile")
async def update_profile(profile: Profile) -> dict:
    await save_profile(profile.model_dump())
    return {"status": "saved"}


@app.post("/api/generate")
async def generate_resume(payload: GenerateRequest):
    await asyncio.sleep(5)
    return {
        "status": "success",
        "message": "Processing complete.",
        "job_title": payload.job_title,
    }
