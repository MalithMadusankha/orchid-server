# main.py
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.fertilizer import fertilizer

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Dynamically get the absolute path of the 'results' directory
RESULTS_DIR = os.path.abspath("results")
print(RESULTS_DIR)

# Ensure the directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

print("Results Directory Absolute Path:", RESULTS_DIR)
print("Contents:", os.listdir(RESULTS_DIR) if os.path.exists(RESULTS_DIR) else "Not Found")

# CORS Setup
origins = ["http://localhost", "http://localhost:3000", "https://*.railway.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/results", StaticFiles(directory=RESULTS_DIR, html=True), name="results")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    print("""
    ╔════════════════════════════════╗
    ║   🚀 Call Default Route  🚀   ║
    ╚════════════════════════════════╝
    """)
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request}
    )

@app.get("/list-results")
async def list_results():
    files = os.listdir(RESULTS_DIR)
    return JSONResponse(content={"files": files})

app.include_router(fertilizer)

print("""
╔════════════════════════════════╗
║ 🚀 FastAPI Server Started! 🚀 ║
╚════════════════════════════════╝
""")

print("===== Hello Orchid Server ===== \n")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
