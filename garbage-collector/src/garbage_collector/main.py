from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from src.garbage_collector.routers.api_router import router
from src.garbage_collector.services.user import get_current_user

app = FastAPI(title="Garbage Collector", description="L2 Project.")
app.include_router(router)
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<h1>Welcome!</h1><br>
<a href="/docs">Docs</a><br>
<a href="/redoc">ReDocs</a>
"""
