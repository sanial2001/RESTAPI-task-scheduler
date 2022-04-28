from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, oauth2, nlp
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/mail",
    tags=['mail']
)


@router.post('/personal_reminder', status_code=status.HTTP_201_CREATED)
def personal_reminder(message_body: schemas.PersonalReminder, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    user_email = user.email
    nlp.processing(message_body.message, [user_email])
    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/club_mail', status_code=status.HTTP_201_CREATED)
def send_mail_by_club(message_body: schemas.ClubMail, db: Session = Depends(get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_head:
        club_members = db.query(models.Club).filter(models.Club.clubs_registered == message_body.club).all()
        user_emails = []
        for club_member in club_members:
            user_info = club_member.user
            user_email = user_info.email
            user_emails.append(user_email)
        nlp.processing(message_body.message, user_emails)
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
