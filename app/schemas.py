from pydantic import  BaseModel
from fastapi_users import  schemas
import uuid
# pydantic нужен для валидации запросов, их проверки


# Тут у нас проверяется что запрос POST содержит именно тип str и имеет поля title и content
# Если бы у нас не было pydantic пришлось много кода писать на проверку типа и полей пример: isalnum isdigit и тд...
class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    title: str
    content: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass




