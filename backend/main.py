# ======================================================
# IMPORT
# ======================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from backend.core.exceptions import AppError

# 👉 IMPORT ROUTERS (CHỈ IMPORT 1 LẦN)
from backend.api.person import router as person_router
from backend.api.marriage import router as marriage_router
from backend.api.parent_child import router as parent_child_router
from backend.api.avatar import router as avatar_router
from backend.api.avatar_cdn import router as avatar_cdn_router
from backend.api.relationship import router as relationship_router
from backend.api.tree import router as tree_router
from backend.api.announcement import router as announcement_router

import os

# ======================================================
# APP INIT
# ======================================================
app = FastAPI(title="FamilyTree API")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 ADD HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ======================================================
# REGISTER ROUTERS (CHỈ 1 LẦN – CHUẨN)
# ======================================================
app.include_router(person_router, prefix="/api/person")
app.include_router(marriage_router, prefix="/api/marriage")
app.include_router(parent_child_router, prefix="/api/parent_child")
app.include_router(avatar_router, prefix="/api/avatar")
app.include_router(avatar_cdn_router, prefix="/cdn")
app.include_router(relationship_router)
app.include_router(tree_router, prefix="/api/tree")
app.include_router(announcement_router, prefix="/api/announcement")

# ======================================================
# EXCEPTION HANDLER
# ======================================================
@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.error,
            "message": exc.message,
            "details": exc.details
        }
    )

# ======================================================
# STATIC
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 🔵 [ADDED]: Static có CORS
from starlette.staticfiles import StaticFiles

class CORSStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

app.mount(
    "/static",
    CORSStaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# ======================================================
# CORS
# ======================================================
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
