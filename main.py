from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import os

app = FastAPI()

# 数据库初始化
DB_PATH = "/app/data/submissions.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Submission(BaseModel):
    name: str
    email: str
    year: str
    degree: str
    school: str
    major: str
    research: str
    photo: str
    papers: List[str]
    awards: Optional[str] = ""
    links: Optional[str] = ""
    linkDesc: Optional[str] = ""

@app.post("/api/submit")
async def submit(data: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO submissions (data) VALUES (?)", (json.dumps(data),))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/submissions")
async def get_submissions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, submitted_at FROM submissions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = json.loads(row[1])
        item["db_id"] = row[0]
        # 如果原始数据里没有提交时间，则使用数据库的时间
        if "submittedAt" not in item:
            item["submittedAt"] = row[2]
        results.append(item)
    return results

@app.delete("/api/submissions/{db_id}")
async def delete_submission(db_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM submissions WHERE id = ?", (db_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.post("/api/clear")
async def clear_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM submissions")
    conn.commit()
    conn.close()
    return {"status": "cleared"}

# 静态文件服务
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    return FileResponse("form.html")

@app.get("/admin")
async def read_admin():
    return FileResponse("admin.html")

@app.get("/{filename}")
async def read_file(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename)
    return JSONResponse(status_code=404, content={"message": "Not found"})
