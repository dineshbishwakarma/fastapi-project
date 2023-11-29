from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas
from ..database import  get_db
from sqlalchemy.orm import Session
from ..utils import hash


router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # # Check if user with same username exists
    # existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    # if existing_user:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Check if user with same email exists
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password
    hashed_password = hash(user.password)

    # Store in the variable
    user.password = hashed_password

    # Get user in dictionary form and unpack with **
    new_user = models.User(**user.model_dump())

    # Send the data to our database

    # add to database
    db.add(new_user)
    db.commit()

    # get back newly created user from database and save back to new_user variable
    db.refresh(new_user)

    return new_user

# Get User
@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail= f"User with id: {id} not found.")
    
    return user