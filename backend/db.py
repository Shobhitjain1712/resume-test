import json
from pathlib import Path
import aiosqlite

DB_PATH = Path(__file__).resolve().parent / "data" / "app.db"

BASE_PROFILE = {
    "name": "Shobhit Jain",
    "contact": {
        "phone": "+91 7697858499",
        "email": "shobhitjain1712@gmail.com",
        "linkedin": "https://www.linkedin.com/in/shobhit-jain-985519133/",
        "github": "https://github.com/Shobhitjain1712",
    },
    "skills": [
        "Python",
        "OOPS",
        "SQL",
        "Django",
        "FastAPI",
        "LangChain",
        "LangGraph",
        "Pydantic",
        "Hugging Face Transformers",
        "Google Cloud",
        "Azure",
        "AWS",
        "Ollama",
        "Groq",
        "RAG",
        "ChromaDB",
        "Pinecone",
        "Weaviate",
        "Docker",
        "GitHub",
        "Dagster",
        "Agentic AI",
        "Prompt Engineering",
        "REST APIs",
        "Analytical Thinking",
        "Communication",
        "Collaboration",
    ],
    "education": [
        {
            "school": "Medicaps University",
            "dates": "2021 -- 2025",
            "degree": "Bachelor of Technology in Computer Science and Engineering",
            "specialization": "Specialization: Artificial Intelligence",
            "gpa": "CGPA : 8.19",
        }
    ],
    "achievements": [
        "Internal Systango Hackathon Winner - Built an AI-driven solution to automate hiring workflows as part of a team, improving recruitment efficiency and winning a cash prize of $200.",
        "Hack-AI-Thon Winner (Systango x Medicaps) - Secured 1st place as a solo participant by developing an innovative AI solution under competitive constraints, winning a cash prize of $50.",
    ],
    "experience": [
        {
            "company": "Systango Technologies",
            "dates": "September 2025 -- Present",
            "role": "SDE - 1 (Backend)",
            "location": "Indore",
            "bullets": [
                "Engineered scalable backend and AI-driven solutions, improving system performance by ~25% and reducing data processing time by ~40%.",
                "Designed and integrated ETL pipelines and Generative AI capabilities, enhancing automation efficiency by ~30%.",
                "Built robust data-driven systems enabling faster and more reliable decision-making across applications.",
            ],
        },
        {
            "company": "Systango Technologies",
            "dates": "February 2025 -- August 2025",
            "role": "AI Intern",
            "location": "Indore",
            "bullets": [
                "Built and experimented with LLM-powered applications using LangChain and open-source models, focusing on real-world AI use cases.",
                "Developed and tested Agentic AI workflows, improving task automation efficiency by ~20%.",
                "Integrated AI models via REST APIs and backend services, enabling scalable deployment of Generative AI solutions.",
            ],
        },
    ],
    "projects": [
        {
            "name": "MediScan Bot - AI-Powered Medical Assistant (Hackathon Winner)",
            "bullets": [
                "Built an AI-powered medical assistant enabling users to upload disease images and receive LLM-driven analysis with chatbot-based interaction.",
                "Leveraged Gemini 2.5 Flash, LangChain, and Pinecone Vector Database to implement semantic search over vectorized medical data, improving response accuracy by ~35%.",
                "Developed a context-aware chatbot with memory handling, securing 1st place in an AI Hackathon for delivering a scalable healthcare solution.",
            ],
        },
        {
            "name": "Legal Case Management & Communication Platform",
            "bullets": [
                "Architected an AI-driven legal platform by integrating Zoho CRM APIs and Dagster ETL pipelines, significantly improving data processing efficiency by ~40%.",
                "Implemented Gemini LLM-based summarization to automate case insights, reducing manual effort by ~30% and enhancing overall information accessibility.",
                "Optimized backend performance through efficient caching strategies and real-time synchronization mechanisms, improving overall system performance by ~25%.",
            ],
        },
    ],
}


async def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL
            )
            """
        )
        await db.commit()
        async with db.execute("SELECT data FROM user_profile WHERE id = 1") as cursor:
            row = await cursor.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO user_profile (id, data) VALUES (1, ?)",
                (json.dumps(BASE_PROFILE),),
            )
            await db.commit()


async def get_profile() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT data FROM user_profile WHERE id = 1") as cursor:
            row = await cursor.fetchone()
        if row is None:
            return BASE_PROFILE
        stored = json.loads(row[0])
        merged = {**BASE_PROFILE, **stored}
        for key in ("contact",):
            if key in BASE_PROFILE:
                merged[key] = {**BASE_PROFILE[key], **stored.get(key, {})}
        return merged


async def save_profile(profile: dict) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE user_profile SET data = ? WHERE id = 1",
            (json.dumps(profile),),
        )
        await db.commit()
