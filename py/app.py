from fastapi import FastAPI
from prisma import Prisma
from prisma.models import Post, User
from faker import Faker


db = Prisma()
app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()

    if not await db.user.find_first():
        for i in range(1, 5):
            fake = Faker()
            await db.user.create(
                {
                    "id": i,
                    "name": fake.name(),
                    "email": fake.email(),
                    "posts": {
                        "create": [
                            {
                                "title": f"Post {j}",
                                "content": f"Content for post {i}",
                                "published": True,
                            }
                            for j in range(1, 5)
                        ]
                    },
                }
            )

    if not await db.post.find_first():
        for i in range(1, 5):
            post = await db.post.create(
                {
                    "id": i,
                    "title": f"Post {i}",
                    "content": f"Content for post {i}",
                    "published": True,
                    "authorId": 1,
                }
            )

        # Add 5 posts to each user
        for i in range(1, 5):
            user = await db.user.find_first(where={"id": i})
            for j in range(1, 5):
                post = await db.post.create(
                    {
                        "title": f"Post {j}",
                        "content": f"Content for post {i}",
                        "published": True,
                        "authorId": i,
                    }
                )
                await db.user.update(
                    where={"id": i},
                    data={"posts": {"connect": {"id": post.id}}},
                )


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
def read_root():
    return {"version": "1.0.0"}


@app.get("/posts", response_model=list[Post])
async def get_posts():
    posts = await db.post.find_many()
    return posts


@app.get("/users", response_model=list[User])
async def get_users():
    users = await db.user.find_many()
    return users