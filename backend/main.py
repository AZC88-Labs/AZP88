from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers.users import router as users_router
from .routers.projects import router as projects_router
from .routers.tasks import router as tasks_router
app = FastAPI()
root_path = Path(__file__).parent.parent
frontend_path = root_path / "docs"

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
app.include_router(users_router, prefix="/api/users")
app.include_router(projects_router, prefix="/api/projects")
app.include_router(tasks_router, prefix="/api/{project_id}/tasks")
