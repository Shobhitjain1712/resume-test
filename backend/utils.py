import re
from pathlib import Path

LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "you", "your", "are",
    "our", "their", "have", "has", "had", "will", "can", "but", "not", "all",
    "any", "who", "what", "when", "where", "why", "how", "job", "role", "team",
    "work", "experience", "skills", "skill", "years", "year", "must", "should",
    "preferred", "required", "plus", "across", "into", "about", "use", "using",
    "able", "ability", "strong", "high", "good", "best", "based",
}


def escape_latex(text: str) -> str:
    if text is None:
        return ""
    escaped = "".join(LATEX_REPLACEMENTS.get(ch, ch) for ch in text)
    return escaped.replace("\n", " ").strip()


def sanitize_filename(text: str, default: str = "resume") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9-_]+", "-", text.strip()).strip("-")
    return cleaned or default


def extract_keywords(text: str, limit: int = 12) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{2,}", text.lower())
    keywords = []
    for word in words:
        if word in STOPWORDS:
            continue
        if word not in keywords:
            keywords.append(word)
        if len(keywords) >= limit:
            break
    return keywords


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
