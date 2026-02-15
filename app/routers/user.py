from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.schemas.user_preferences import UserPreferencesUpdate, UserPreferencesOut
from app.schemas.api_response import APIResponse


router = APIRouter(prefix="/user", tags=["User"])

@router.put("/profile", response_model=APIResponse[UserPreferencesOut])
def update_preferences(
    prefs: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_pref = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not user_pref:
        user_pref = UserPreferences(user_id=current_user.id)
        db.add(user_pref)

    user_pref.dark_mode = prefs.dark_mode

    db.commit()
    db.refresh(user_pref)

    return {
    "success": True,
    "data": user_pref,
    "message": "Preferences updated"
    }

