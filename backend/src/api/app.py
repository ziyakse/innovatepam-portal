from fastapi import FastAPI

from src.api.auth_routes import router as auth_router

app = FastAPI(title="InnovatEPAM User Management API")
app.include_router(auth_router)
