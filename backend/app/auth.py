import token

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta

from app.database import SessionLocal

from app.models import User

from app.schemas import (
    RegisterSchema,
    LoginSchema
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

SECRET_KEY = "your_secret_key_123"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# PASSWORD HASH
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    user: RegisterSchema,
    db: Session = Depends(get_db)
):
    try:

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        password = user.password[:72]

        hashed_password = pwd_context.hash(
        password
        )

        new_user = User(
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Registration Successful"
        }

    except Exception as e:

        print("REGISTER ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    try:

        db_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if not db_user:

            raise HTTPException(
                status_code=400,
                detail="Invalid Email or Password"
            )

        password = user.password[:72]

        valid_password = pwd_context.verify(
            password,
            db_user.password
        )

        if not valid_password:

            raise HTTPException(
                status_code=400,
                detail="Invalid Email or Password"
            )

        token = create_access_token(
        {
            "sub": db_user.email
        }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except Exception as e:

        print("LOGIN ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Login Failed"
        )