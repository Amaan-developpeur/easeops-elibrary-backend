from pydantic import BaseModel

class UserPreferencesUpdate(BaseModel):
    dark_mode: bool

class UserPreferencesOut(BaseModel):
    dark_mode: bool

    class Config:
        from_attributes = True
