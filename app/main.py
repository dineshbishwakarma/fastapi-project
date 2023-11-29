from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include posts router
app.include_router(post.router)

# Include users router
app.include_router(user.router)

# Include login router
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


