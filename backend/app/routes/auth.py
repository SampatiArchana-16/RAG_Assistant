from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

import bcrypt

from app.database import SessionLocal

from app.models import User

from app.schemas import (
    RegisterSchema,
    LoginSchema
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(
    user: RegisterSchema,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # HASH PASSWORD
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message":
        "Registration Successful"
    }


@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return {
        "message":
        "Login Successful"
    }