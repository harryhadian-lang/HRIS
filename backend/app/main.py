from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HRIS Platform API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "HRIS Platform API", "status": "ok", "version": app.version}

@app.get("/api/v1/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/system/info")
def system_info():
    return {
        "name": "HRIS Platform",
        "architecture": "multi-tenant",
        "api_version": "v1",
        "modules": ["hris", "crm", "finance"],
    }
