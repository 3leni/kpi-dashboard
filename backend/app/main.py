from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, inspect

from app.database.database import engine, get_db
from app.models import user, kpi, departament  # Importar modelos para que se creen las tablas
from app.models.user import Base
from app.api.v1.enpoints import kpis, users
# Crear tablas en la base de datos
user.Base.metadata.create_all(bind=engine)
kpi.Base.metadata.create_all(bind=engine)
departament.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPI Dashboard API",
    description="API FOR KPI DASHBOARD",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(kpis.router, prefix="/api/v1/kpis", tags=["kpis"])

@app.get("/")
async def root():
    return {"message": "¡Bienvenido al KPI Dashboard API!",
            "status": "OK",
            "version":"1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/info")
async def project_info(db=Depends(get_db)):
    inspector = inspect(db.bind)

    tables_name = inspector.get_table_names()
    num_tables = len(tables_name)

    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = "disconnected"

    modelos = list({cls.__name__ for cls in Base.__subclasses__()})
    return {
        "project": "KPI Dashboard",
        "version": "1.0.0",
        "author": "Luz Elena Tovar Flores",
        "start_date": "2023-01-01",
        "features": [
            "Autentication with JWT",
            "Dashboard from KPIs",
            "CRUD Completed",
            "Interactive graphs"
        ],
        "tables": num_tables,
        "status_db": db_status,
        "models_disp": modelos,
    }

@app.get("/users/me")
async def read_current_user():
    return {
        "user_id": 1,
        "username": "usuario_luz",
        "email": "luzejemplos.com"
    }

@app.get("/greet/{name}")
async def greet_user(name: str):
    return {
        "mesage": f"Hola, {name}! Bienvenido al KPI dashboard",
        "timestamp": "2024-01-01T00:00:"
    }

@app.get("/items/")
async def read_itemd(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit,
        "items": [f"item_{i}" for i in range(skip, skip + limit)]
    }

@app.get("/db-health")
async def db_health_check(db=Depends(get_db)):
    try:
        # Ejecutar consulta simple para verificar conexión
        result = db.execute(text("SELECT 1"))
        return {"database": "connected", "status": "healthy"}
    except Exception as e:
        return {"database": "disconnected", "status": "error", "detail": str(e)}
    
if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)