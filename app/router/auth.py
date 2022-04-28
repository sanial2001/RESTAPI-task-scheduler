from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.get("/")
def sample():
    return {"Hello": "World"}


@router.post('/signup')
def signup(user: schemas.Signup, db: Session = Depends(get_db)):
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email : {user.email} already exist")
    user.password = utils.hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_head=user.is_head
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No account registered")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
