from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# We need 3 things 

# SECRET_KEY
# to get a string like this run:
# openssl rand -hex 32 in terminal
SECRET_KEY = settings.secret_key

# Algorithm 
ALGORITHM = settings.algorithm

# TOKEN
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire

# Lets provide the data that we want to encode 
def create_access_token(data: dict):

    # Payload
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Update the to_encode dict
    to_encode.update({"exp": expire})


    encoded_jwt =  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    # we might run into error so lets user try except 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Convert the id into string, since we compare string type TokenData
        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f'Invalid Credentials', 
                                           headers= {"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    