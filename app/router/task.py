import collections
from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from ..db import get_db

router = APIRouter(
    prefix="/task",
    tags=['task']
)


@router.get("/")
def sample():
    return {"Hello": "World"}


@router.post('/register_club', status_code=status.HTTP_201_CREATED)
def register_for_club(club_details: schemas.RegisterClub, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    current_user = db.query(models.User).filter(models.User.id == user_id.id).first()
    clubs_current_user = current_user.club
    for cur in clubs_current_user:
        if cur.clubs_registered == club_details.clubs_registered:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Already registered")
    new_club = models.Club(
        clubs_registered=club_details.clubs_registered
    )
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    new_club.user = user
    db.add(new_club)
    db.commit()
    db.refresh(new_club)
    return new_club


@router.get('/all_users', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_head:
        all_users = db.query(models.User).all()
        all_users_response = collections.defaultdict(dict)
        for i, cur_user in enumerate(all_users):
            cur = {
                "id": cur_user.id,
                "username": cur_user.username,
                "email": cur_user.email,
                "is_head": cur_user.is_head
            }
            # print(cur)
            all_users_response[i] = cur
        return all_users_response
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")


@router.get('/user/{id}', status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_head:
        user_searched = db.query(models.User).filter(models.User.id == id).first()
        if not user_searched:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
        clubs_registered_by_user_searched = user_searched.club
        response_user_searched_club = collections.defaultdict(dict)
        for i, cur in enumerate(clubs_registered_by_user_searched):
            response_user_searched_club[i] = cur.clubs_registered
        return clubs_registered_by_user_searched
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")


@router.get('/user_clubs', status_code=status.HTTP_200_OK)
def get_clubs_registered(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    user_clubs = user.club
    return jsonable_encoder(user_clubs)


@router.delete('/unregister_club/{id}', status_code=status.HTTP_204_NO_CONTENT)
def unregister_from_club(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    club_to_unregister = db.query(models.Club).filter(models.Club.id == id).first()
    if not club_to_unregister:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found in club")
    if int(user_id.id) != int(club_to_unregister.user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    db.delete(club_to_unregister)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/update_profile/{id}', status_code=status.HTTP_200_OK)
def update(id: int, updated_details: schemas.UpdateProfile, db: Session = Depends(get_db),
           user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_head:
        updated_user = db.query(models.User).filter(models.User.id == id).first()
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
        updated_user.is_head = updated_details.is_head
        db.commit()
        response = {
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "is_head": updated_user.is_head
        }
        return response
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
