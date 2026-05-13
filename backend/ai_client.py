import os
from typing import Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

from utils import extract_keywords

load_dotenv()


def _fallback_generation(job_description: str, base_profile: dict) -> dict:
    keywords = extract_keywords(job_description)
    base_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "Django",
        "LangChain",
        "Pydantic",
        "Hugging Face",
        "RAG",
        "Docker",
        "REST APIs",
    ]
    skills = list(dict.fromkeys(base_skills + [kw.upper() if len(kw) <= 5 else kw.title() for kw in keywords]))
    summary = (
        "AI and backend engineer focused on production-grade LLM applications, "
        "data pipelines, and scalable API systems. Tailors solutions to job requirements "
        "while highlighting measurable impact and reliable delivery."
    )
    return {
        "summary": summary,
        "skills": skills,
        "experience": base_profile.get("experience", []),
        "projects": base_profile.get("projects", []),
    }


async def generate_resume_content(job_description: str, base_profile: dict) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        return _fallback_generation(job_description, base_profile)

    client = AsyncOpenAI(api_key=api_key)
    system_prompt = (
        "You are a resume tailoring assistant. Use ONLY the facts provided in the base profile. "
        "Do not invent employers, degrees, dates, certifications, or awards. "
        "You may rephrase bullets to match the job description and highlight relevance. "
        "You may add tools/skills into experience bullets ONLY if they appear in base_profile.skills "
        "and are relevant to the job description. "
        "Return strictly valid JSON with keys: summary (string), skills (array of strings), "
        "experience (array of objects with company, role, location, dates, bullets), "
        "projects (array of objects with name, bullets)."
    )
    user_prompt = {
        "job_description": job_description,
        "base_profile": base_profile,
    }

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(user_prompt)},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    content = response.choices[0].message.content
    return _safe_json_parse(content, base_profile)


def _safe_json_parse(content: str, base_profile: dict) -> dict:
    import json

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return _fallback_generation("", base_profile)

    return {
        "summary": parsed.get("summary", ""),
        "skills": parsed.get("skills", []),
        "experience": parsed.get("experience", base_profile.get("experience", [])),
        "projects": parsed.get("projects", base_profile.get("projects", [])),
    }
