from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(
    tags= ['Authentication']
)

@router.post("/login", response_model=schemas.Token)
# def login(user_credentials:schemas.UserLogin, \
#           db: Session = Depends(database.get_db)):
# Get the user credentials from databse
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
# we can ask user_credentials from fastapi inbuilt library OAuth2PasswordRequestForm

def login(user_credentials:OAuth2PasswordRequestForm = Depends(), \
          db: Session = Depends(database.get_db)):

    # user_credentials:OAuth2PasswordRequestForm returns
    # { "username": "adfsdf", "password": "asdfsdf"}
    
    # Get the user credentials from databse
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # If not available throw exception
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Invalid Credentials')

    # If available lets verify with our database
    # verify function was created in utils to very  
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
                             detail=f'Invalid Credentials')
    
    #If verified lets create token
    # and return token
    # Here we add the data that we want to add it to payload, here we add user_id
    access_token = oauth2.create_access_token(data={"user_id" : user.id})

    return {"access_token": access_token, "token_type": "bearer"}