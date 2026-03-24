from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="FamilyTree API")

# Static (production safe absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)
    
# CORS
ENV = os.environ.get("ENV", "development")

if ENV == "development":
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
else:
    origins = ["https://familytree.example.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# REGISTER ROUTERS
# ==============================
from backend.api.person import router as person_router
from backend.api.marriage import router as marriage_router
from backend.api.parent_child import router as parent_child_router
from backend.api.avatar import router as avatar_router
from backend.api.tree import router as tree_router
# from backend.api.clean_parent_api import router as clean_parent_router
from backend.api.avatar_cdn import router as avatar_cdn_router
from backend.api.relationship import router as relationship_router

app.include_router(person_router)
app.include_router(marriage_router)
app.include_router(parent_child_router)
app.include_router(avatar_router)
app.include_router(tree_router, prefix="/api/tree")
# app.include_router(clean_parent_router)
app.include_router(avatar_cdn_router, prefix="/cdn")
app.include_router(relationship_router)

@app.get("/")
def root():
    return {"message": "FastAPI running"}