def NoteEntity(item) -> dict:
    return {
        "id": str(item.get("_id")),
        "title": item.get("title", ""),
        "desc": item.get("desc", ""),
        "important": bool(item.get("important", False)),
    }


def NotesEntity(items) -> list:
    return [NoteEntity(item) for item in items]
