from fastapi import FastAPI, HTTPException, Query
import json
import random
from datetime import date
import os

app = FastAPI(title="Thirukkural API")

# ✅ Load JSON safely (works locally + cloud)
file_path = os.path.join(os.path.dirname(__file__), "clean_thirukkural.json")

try:
    with open(file_path, encoding="utf-8") as f:
        kurals = json.load(f)
except FileNotFoundError:
    raise Exception("❌ clean_thirukkural.json file not found")

# Fast lookup
kural_dict = {k["id"]: k for k in kurals}

TOTAL_KURALS = len(kurals)
TOTAL_CHAPTERS = 133


# 🏠 Root
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
            "/section?section=virtue"
        ]
    }


# ✅ 1. Get Kural by ID
@app.get("/kural/{id}")
def get_kural(id: int):
    if id < 1 or id > TOTAL_KURALS:
        raise HTTPException(status_code=400, detail="Invalid Kural ID")

    return kural_dict.get(id)


# ✅ 2. Get Kurals by Chapter
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


# ✅ 3. Get Chapter Details
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


# ✅ 4. Search
@app.get("/search")
def search(q: str):
    q = q.strip()

    results = [
        k for k in kurals
        if q in k["tamil"] or q.lower() in k["english"].lower()
    ]

    return {"query": q, "count": len(results), "data": results}


# ✅ 5. Starts with
@app.get("/search/start")
def search_start(q: str):
    q = q.strip()

    results = [
        k for k in kurals
        if k["tamil"].strip().startswith(q)
    ]

    return {"query": q, "type": "starts_with", "count": len(results), "data": results}


# ✅ 6. Ends with
@app.get("/search/end")
def search_end(q: str):
    q = q.strip()

    results = [
        k for k in kurals
        if k["tamil"].strip().endswith(q)
    ]

    return {"query": q, "type": "ends_with", "count": len(results), "data": results}


# ✅ 7. Random
@app.get("/random")
def random_kural():
    return random.choice(kurals)


# ✅ 8. Daily
@app.get("/daily")
def daily_kural():
    index = date.today().toordinal() % TOTAL_KURALS
    return kurals[index]


# ✅ 9. Section filter
@app.get("/section")
def get_by_section(section: str):
    results = [
        k for k in kurals
        if section.lower() in k["section_en"].lower()
    ]

    return {
        "section": section,
        "count": len(results),
        "data": results
    }

# ✅ 10. Tamil-only Kural
@app.get("/tamil/{id}")
def get_tamil_kural(id: int):
    if id < 1 or id > TOTAL_KURALS:
        raise HTTPException(status_code=400, detail="Invalid Kural ID")

    kural = kural_dict.get(id)

    return {
        "id": kural["id"],
        "tamil": kural["tamil"]
    }
