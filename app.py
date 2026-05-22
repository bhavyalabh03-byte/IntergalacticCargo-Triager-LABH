from fastapi import FastAPI, Header
from fastapi.responses import PlainTextResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

JSON_FILE_PATH = "Task 1 - LABH - Parser.json"

# --- TASK 3 FRONTEND ROUTES ---

# 1. Serve the frontend HTML file at the root URL (http://127.0.0.1:8000/)
@app.get("/")
def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return PlainTextResponse("Frontend index.html not found.", status_code=404)

# 2. Serve static styles if you put them in a separate folder (optional safety fallback)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# --- TASK 2 BACKEND ENDPOINT ---
@app.get("/api/cargo")
def get_cargo(x_system_override: str = Header(None, alias="X-System-Override")):
    # Business Rule 3: Catch the system override header and return a 418 Teapot
    if x_system_override == "true":
        return PlainTextResponse(
            content="System override denied.", 
            status_code=418
        )
    
    # Normal behavior: Serve your valid parsed JSON cargo data
    if not os.path.exists(JSON_FILE_PATH):
        return JSONResponse(
            status_code=404, 
            content={"detail": "Cargo data manifest not found."}
        )
        
    with open(JSON_FILE_PATH, "r") as f:
        data = json.load(f)
    return data