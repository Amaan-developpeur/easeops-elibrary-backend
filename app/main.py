from fastapi import FastAPI
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.models.book import Book

from app.routers import auth
from app.routers import user
from app.routers import books
from app.models.bookmark import Bookmark
from app.models.note import Note

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.response import error_response
from app.core.logger import logger

app = FastAPI(title="EaseOps E-Library API")

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------------------------
from app.database import engine, Base

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# ----------------------------------------
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(books.router)
# --------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=error_response("Internal server error")
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response("Validation error")
    )





