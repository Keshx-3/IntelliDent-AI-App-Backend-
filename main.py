# main.py
from fastapi import FastAPI
from routers.auth_routes import router as auth_router
from routers.doctors_routes import router as doctor_router
from routers.appointments_routes import router as appointment_router
from routers.products_routes import router as products_router
from routers.orders_routes import router as orders_router
from routers.profile_routes import router as profile_router
from routers.scan_routes import router as scan_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="IntelliDent AI API",
    description="FastAPI backend for IntelliDent AI App",
    version="1.0.0"
)

app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Register routers
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(profile_router)
app.include_router(scan_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

