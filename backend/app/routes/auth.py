from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from passlib.context import CryptContext

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

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
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
    hashed_password = pwd_context.hash(
        user.password
    )

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