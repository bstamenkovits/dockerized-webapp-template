from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    display_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    # allows you to pass any object to .model_validate(...)
    model_config = ConfigDict(from_attributes=True)

    id: str
    display_name: str
    email: EmailStr
    is_active: int
    created_at: str
    updated_at: str
