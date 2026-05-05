from fastapi import FastAPI, HTTPException, Query
import json
import random
from datetime import date

app = FastAPI(title="Thirukkural API")

# Load JSON
with open("/home/sakthivelan/Desktop/Thirukural/clean_thirukkural.json", encoding="utf-8") as f:
    kurals = json.load(f)

kural_dict = {k["id"]: k for k in kurals}

TOTAL_KURALS = len(kurals)  # 1330
TOTAL_CHAPTERS = 133


# 🏠 Root
@app.get("/")
def home():
    return {
        "message": "Thirukkural API is running",
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
        raise HTTPException(400, "Invalid Kural ID")
    return kural_dict[id]


# ✅ 2. Get Kurals by Chapter (basic)
@app.get("/kural")
def get_by_chapter(chapter: int = Query(...)):
    if chapter < 1 or chapter > TOTAL_CHAPTERS:
        raise HTTPException(400, "Invalid chapter")

    start = (chapter - 1) * 10
    end = start + 10

    return {
        "chapter": chapter,
        "data": kurals[start:end]
    }


# ✅ 3. ⭐ Get Chapter Details (NEW)
@app.get("/chapters/{chapter_id}")
def get_chapter_details(chapter_id: int):
    if chapter_id < 1 or chapter_id > TOTAL_CHAPTERS:
        raise HTTPException(400, "Invalid chapter")

    start = (chapter_id - 1) * 10
    end = start + 10
    chapter_kurals = kurals[start:end]

    # Take chapter name from first kural
    chapter_name_en = chapter_kurals[0]["chapter_en"]
    chapter_name_ta = chapter_kurals[0]["chapter_ta"]

    return {
        "chapter_number": chapter_id,
        "chapter_name_en": chapter_name_en,
        "chapter_name_ta": chapter_name_ta,
        "total_kurals": len(chapter_kurals),
        "kurals": chapter_kurals
    }


# ✅ 4. Search (general)
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