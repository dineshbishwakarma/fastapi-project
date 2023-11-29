from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import oauth2
from sqlalchemy import func



router = APIRouter(
     prefix="/posts",
     tags= ["Posts"]
)
# Get post
     
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
               # Here limit is the query parameter, if limit = 5, will show only 5 posts by default
               # here skip skips the given value number of posts
               # here search parameter is used to search
               limit: int = 5, skip: int = 0, search:Optional[str] = ""):
     
     # # To show the logged in user post only 
     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()


     # This will query the database and return the columns from table 
     # here we will use offset to skip some posts 
     # here we will use filter contains method
     # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     # return in jason format
     return posts

# Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int =
                 Depends(oauth2.get_current_user)):

    
    # Create the post
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)

    # Let's say we have 50 fields like title, content, ... . Then how do we do? 

    # Grab post in dictionary form and unpack with **, update the current user 
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())

    # Send the post data to our database
    
    # add to databse
    db.add(new_post)
    db.commit()

    # get back newly created post from database and save back to new_post variable
    db.refresh(new_post)
    
    return new_post
    # The returned new_post is according response model defined above i.e. pydantic model
    # But new_post in line 36 is SQLAlchemy model. 
    # So, there my be model conflict. 
    # FastAPI handles this internally converting
    # But it is good to set 
    # class Config:
    #  from_attributes = True
    # schemas.py file under Post class 



# we can force the client to send data in a schema that we expect
# title: str, content: str

# Read a single Post 
# here {id}: path parameter 

@router.get("/{id}", response_model=schemas.PostOut)

# here id can be assigned data type by id : int or str
def get_post(id: int, db: Session = Depends(get_db), current_user: int =
                 Depends(oauth2.get_current_user)):
        
     # here we need filter to get specific id and one post
     #post = db.query(models.Post).filter(models.Post.id == id).first()

     post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 

     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"Post with {id} not found")

     return post

# # Delete a post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session= Depends(get_db), current_user: int =
                 Depends(oauth2.get_current_user)):

     # here we need filter to get specific id
     post = db.query(models.Post).filter(models.Post.id == id)

     # Check there is post or no with the id given
     if post.first() == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"Post with {id} not found.")

     # Check is the user to delete the post is valid
     if post.first().owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail= f"Not authorized to delete post.")

     # delete the post
     post.delete(synchronize_session = False)

     # Commit the changes
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update post
@router.put("/{id}" , response_model=schemas.Post)
def update_post(id : int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
                 Depends(oauth2.get_current_user)):

  
    # Query the post 
     post_query = db.query(models.Post).filter(models.Post.id == id)

     post_to_update = post_query.first() 
    

     # If there is now row with id given
     if not post_to_update:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id {id} not found.")
    
     # Check is the user to update the post is valid
     if post_to_update.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail= f"Not authorized to delete post.")
     
     # Update the post, updated_post will save which row is updated
     post_query.update(post.model_dump(), synchronize_session = False)
     
     # Commit changes
     db.commit() 

     # To see the updated post need to user .first() method
     return post_query.first()