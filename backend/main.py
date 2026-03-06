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
ENV = os.environ.get("FLASK_ENV", "development")

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
from backend.api.person_basic import router as person_basic_router
from backend.api.marriage_fastapi import router as marriage_router
from backend.api.parent_child_fastapi import router as parent_child_router
from backend.api.avatar import router as avatar_router
from backend.api.tree_fastapi import router as tree_router
from backend.api.clean_parent_api import router as clean_parent_router

app.include_router(person_basic_router)
app.include_router(marriage_router)
app.include_router(parent_child_router)
app.include_router(avatar_router)
app.include_router(tree_router)
app.include_router(clean_parent_router)

# ==============================
# RELATIONSHIP ROUTE
# ==============================
from app.core.relationship_resolver import RelationshipResolver

resolver = RelationshipResolver()

@app.get("/api/relationship")
def get_relationship(source_id: int, target_id: int):
    return resolver.resolve(source_id, target_id)
@app.get("/")
def root():
    return {"message": "FastAPI running"}