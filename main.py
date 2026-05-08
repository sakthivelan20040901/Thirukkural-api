from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from datetime import date
import os

app = FastAPI(title="Thirukkural API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Load JSON safely
file_path = os.path.join(os.path.dirname(__file__), "clean_thirukkural.json")

try:
    with open(file_path, encoding="utf-8") as f:
        kurals = json.load(f)
except FileNotFoundError:
    raise Exception("❌ clean_thirukkural.json file not found")

kural_dict = {k["id"]: k for k in kurals}
TOTAL_KURALS = len(kurals)
TOTAL_CHAPTERS = 133


@app.get("/")
def home():
    return {
        "message": "Thirukkural API is running",
        "total_kurals": TOTAL_KURALS,
        "endpoints": [
            "/kural/{id}",
            "/kural?chapter=1",
            "/chapters/1",
            "/search?q=",
            "/search/start?q=",
            "/search/end?q=",
            "/random",
            "/daily",
            "/section?section=virtue",
            "/tamil/{id}"
        ]
    }


@app.get("/kural/{id}")
def get_kural(id: int):
    if id < 1 or id > TOTAL_KURALS:
        raise HTTPException(status_code=400, detail="Invalid Kural ID")
    return kural_dict.get(id)


@app.get("/kural")
def get_by_chapter(chapter: int = Query(...)):
    if chapter < 1 or chapter > TOTAL_CHAPTERS:
        raise HTTPException(status_code=400, detail="Invalid chapter")

    start = (chapter - 1) * 10
    end = start + 10
    return {
        "chapter": chapter,
        "count": len(kurals[start:end]),
        "data": kurals[start:end]
    }


@app.get("/chapters/{chapter_id}")
def get_chapter_details(chapter_id: int):
    if chapter_id < 1 or chapter_id > TOTAL_CHAPTERS:
        raise HTTPException(status_code=400, detail="Invalid chapter")

    start = (chapter_id - 1) * 10
    end = start + 10
    chapter_kurals = kurals[start:end]

    if not chapter_kurals:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return {
        "chapter_number": chapter_id,
        "chapter_name_en": chapter_kurals[0]["chapter_en"],
        "chapter_name_ta": chapter_kurals[0]["chapter_ta"],
        "total_kurals": len(chapter_kurals),
        "kurals": chapter_kurals
    }


@app.get("/search")
def search(q: str):
    q = q.strip()
    results = [
        k for k in kurals
        if q in k["tamil"] or q.lower() in k["english"].lower()
    ]
    return {"query": q, "count": len(results), "data": results}


@app.get("/search/start")
def search_start(q: str):
    q = q.strip()
    results = [k for k in kurals if k["tamil"].strip().startswith(q)]
    return {"query": q, "type": "starts_with", "count": len(results), "data": results}


@app.get("/search/end")
def search_end(q: str):
    q = q.strip()
    results = [k for k in kurals if k["tamil"].strip().endswith(q)]
    return {"query": q, "type": "ends_with", "count": len(results), "data": results}


@app.get("/random")
def random_kural():
    return random.choice(kurals)


@app.get("/daily")
def daily_kural():
    index = date.today().toordinal() % TOTAL_KURALS
    return kurals[index]


@app.get("/section")
def get_by_section(section: str):
    results = [
        k for k in kurals
        if section.lower() in k["section_en"].lower()
    ]
    return {"section": section, "count": len(results), "data": results}


@app.get("/tamil/{id}")
def get_tamil_kural(id: int):
    if id < 1 or id > TOTAL_KURALS:
        raise HTTPException(status_code=400, detail="Invalid Kural ID")

    kural = kural_dict.get(id)
    return {"id": kural["id"], "tamil": kural["tamil"]}

@app.get("/health")
def health():
    return {"status": "ok"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
