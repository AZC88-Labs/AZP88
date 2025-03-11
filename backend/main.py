from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
app = FastAPI()
root_path = Path(__file__).parent.parent
frontend_path = root_path / "frontend"


app.mount("/", StaticFiles(directory=frontend_path,html = True), name="static")