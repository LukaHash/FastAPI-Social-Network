import uuid

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.schemas  import  PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import  Post, create_db_and_tables, get_async_session, User

from  sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from sqlalchemy import  select
from app.users import  auth_backend, current_active_user, fastapi_users


from app.images import imagekit
import shutil
import os
import  tempfile



# жизненный цикл ДБ
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate), prefix="/users", tags=["users"])









# модернизированная функция POST для отправки файла
@app.post("/upload")
async  def upload_file(
        user: User = Depends(current_active_user), # функция не сработает если мы не зарегистрированы как current_active_user
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    # Создаем временный файл для того чтобы загрузки пользователя не копились на сервере
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file = f,
                file_name = file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )


        post = Post(
            user_id=user.id,
            caption = caption,
            url = upload_result.url,
            file_type = "video" if file.content_type.startswith("video/") else "image",
            file_name= upload_result.name
        )
        session.add(post) # Функция говорит что пост готов к комиту
        await session.commit() # Пост комитится/сохраняется в ДБ
        await session.refresh(post) # Перезагружаем сессию ДБ чтобы добавились автоматические данные (типо ID и когда было созданно)
        return post
    except Exception as e:
        raise  HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)

):

    result = await  session.execute(select(Post).order_by(Post.created.desc()))
    posts = [row[0] for row in result.all()]

    result = await  session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id:  u.email for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "unknown")

            }

        )
    return {"posts": posts_data}




@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user),):
    try:
        post_uuid = uuid.UUID(post_id) # Превратили пользовательский id в UUID

        result = await  session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first() # Дает результат внутри объекта НО НЕ САМ ОБЪЕКТ
        # если бы строки выше не было, нам бы просто выводился сам объект, но не то, что находится внутри него.

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
        await  session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}



    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))







# @app.get("/hello-world") #Первый эндпоинт
# def hello_world():
#     return {"message": "Hello World"} # JSON -> JavaScript object Notation #


# text_posts = test_posts = {
#     1: {"title": "Welcome to the API", "content": "This is a sample post to test the creation endpoint."},
#     2: {"title": "Second Post", "content": "Another test post with some dummy content."},
#     3: {"title": "Lorem Ipsum", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
#     4: {"title": "Testing Pagination", "content": "This post is used to verify pagination and filtering logic."},
#     5: {"title": "Update Test", "content": "Content to be modified during PUT/PATCH test cases."},
#     6: {"title": "Delete Me", "content": "This post will be used for deletion tests."},
#     7: {"title": "Edge Case: Empty Content", "content": ""},
#     8: {"title": "Long Title" + "x" * 50, "content": "Title exceeds typical length to test validation."},
#     9: {"title": "Special Chars", "content": "Includes emojis 🚀 and symbols: @#%&*()"},
#    10: {"title": "Final Post", "content": "Last test post for bulk operations or sorting checks."}
# }
#
#
#
# # при вызове url.get(/posts) мы получим все посты которые есть
# # query params
# @app.get("/posts")
# def get_all_posts(limit: int = None): #  int = None Параметр который можно не указывать, ели бы просто было int, то тогда нужно было 100% указывать
#     if limit:
#         return list(text_posts.values())[:limit] # тут с values чисто заглушка, если бы не она мы бы пытались применить list операцию на dict
#     return text_posts
#
# # (-> PostResponse) тут означает что функция обязана вернуть данные типа PostResponse иначе будет ошибка
# # Id тут меняемый
# @app.get("/posts/{id}")
# def get_post(id: int) -> PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404,detail="Post not found")
#     return text_posts.get(id)
#
#
#
# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     test_posts[max(text_posts.keys())+1] = new_post # при помощи max(..) добавляет единицу к максимальному айди поста
#     return new_post
#
#
#
#
# @app.delete("/delete/{id}")
# def delete(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404,detail="Post not found")
#     del text_posts[id]
#     return {"status": "success", "message": f"post {id} was deleted"} # POST GET DELETE без DB









