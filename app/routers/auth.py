from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.core.response import success_response
from app.schemas.api_response import APIResponse
from app.core.logger import logger
from app.schemas.token import TokenOut
from app.schemas.api_response import APIResponse



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=APIResponse[UserOut])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        logger.warning(f"Duplicate registration attempt: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")


    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    #return success_response(data=db_user)
    #return success_response(data=UserOut.model_validate(db_user))
    return {
    "success": True,
    "data": db_user,
    "message": "User registered successfully"
    }

# @router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if not db_user or not verify_password(user.password, db_user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": str(db_user.id)})

#     return {"access_token": token, "token_type": "bearer"}

from fastapi.security import OAuth2PasswordRequestForm
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -----------------------------------
from app.core.security import get_current_user

@router.get("/me", response_model=APIResponse[UserOut])
def get_me(current_user: User = Depends(get_current_user)):
    return {
    "success": True,
    "data": current_user,
    "message": None
    }

# --------------------------------------------