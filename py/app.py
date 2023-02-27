from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from prisma import Prisma
from prisma.models import Post, User
from faker import Faker


db = Prisma()
app = FastAPI()
fake = Faker()


@app.on_event("startup")
async def startup():
    await db.connect()

    if not await db.user.find_first():
        for i in range(1, 5):
            await db.user.create(
                {
                    "id": i,
                    "name": fake.name(),
                    "email": fake.email(),
                    "posts": {
                        "create": [
                            {
                                "title": f"Post {j}",
                                "content": fake.paragraph(nb_sentences=5),
                                "published": True,
                            }
                            for j in range(1, 5)
                        ]
                    },
                }
            )


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
def home():
    return RedirectResponse(url="/docs")


@app.get("/posts", response_model=list[Post])
async def get_posts():
    return await db.post.find_many(include={"author": True})


@app.get("/users", response_model=list[User])
async def get_users():
    return await db.user.find_many(include={"posts": True})


@app.delete("/all")
async def delete_all():
    deleted_posts = await db.post.delete_many()
    deleted_users = await db.user.delete_many()

    return {"Deleted posts": deleted_posts, "Deleted users": deleted_users}
