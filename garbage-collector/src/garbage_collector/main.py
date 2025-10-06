from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Garbage Collector", description="L2 Project.")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<h1>Welcome!</h1><br>
<a href="/docs">Docs</a><br>
<a href="/redoc">ReDocs</a>
"""
