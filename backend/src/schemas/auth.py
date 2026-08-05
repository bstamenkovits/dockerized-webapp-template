from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    display_name: str
    email: EmailStr
    password: str


#
# class UserCreate(BaseModel):
#     display_name: str
#     email: EmailStr
#     password: str
#
#
# class LoginRequest(BaseModel):
#     email: str
#     password: str
#
#
# class UserOut(BaseModel):
#     # allows you to pass any object to .model_validate(...)
#     model_config = ConfigDict(from_attributes=True)
#
#     id: str
#     display_name: str
#     email: EmailStr
#     is_active: int
#     created_at: str
#     updated_at: str
#
#
# class SessionOut(BaseModel):
#     # allows you to pass any object to .model_validate(...)
#     model_config = ConfigDict(from_attributes=True)
#
#     id: str
#     user_id: str
#     created_at: str
#     expires_at: str
#     revoked_at: str | None
#     user_last_active: str | None
