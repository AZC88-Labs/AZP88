from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers.users import router as users_router
app = FastAPI()
root_path = Path(__file__).parent.parent
frontend_path = root_path / "docs"

app.include_router(users_router, prefix="/api/users")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
