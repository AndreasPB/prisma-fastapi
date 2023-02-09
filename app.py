from fastapi import FastAPI
from prisma import Prisma
from prisma.models import Post
from prisma.types import PostCreateInput
from uuid import uuid4


db = Prisma()
app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()

    # Only add if no posts
    if not await db.post.find_first():
        post = await db.post.create(
            {
                "title": "Hello from prisma!",
                "desc": "Prisma is a database toolkit and makes databases easy.",
                "published": True,
            }
        )

        print(f"created post: {post.json(indent=2, sort_keys=True)}")


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


@app.post("/posts")
async def create_post(post: PostCreateInput):
    post["id"] = str(uuid4())
    new_post = await db.post.create(post)
    return new_post
