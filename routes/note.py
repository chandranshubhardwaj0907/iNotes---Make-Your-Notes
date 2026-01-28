from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime

from config.db import conn

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []

    for doc in docs:
        newDocs.append({
            "id": str(doc.get("_id")),
            "title": doc.get("title", ""),
            "desc": doc.get("desc", ""),
            "important": bool(doc.get("important", False)),
        })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "newDocs": newDocs}
    )


@note.post("/")
async def create_note(request: Request):
    form = await request.form()
    data = dict(form)

    title = data.get("title", "").strip()
    desc = data.get("desc", "").strip()
    important = data.get("important") == "on"  # checkbox handling

    # Basic validation
    if not title:
        return {"success": False, "error": "Title is required"}

    conn.notes.notes.insert_one({
        "title": title,
        "desc": desc,
        "important": important,
        "created_at": datetime.utcnow()
    })

    # Redirect back to homepage (best UX for forms)
    return RedirectResponse(url="/", status_code=303)
