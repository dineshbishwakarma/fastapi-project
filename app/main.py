from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# List of domains allowed , * means all domains are allowed
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Include posts router
app.include_router(post.router)

# Include users router
app.include_router(user.router)

# Include login router
app.include_router(auth.router)

# Include vote router
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


