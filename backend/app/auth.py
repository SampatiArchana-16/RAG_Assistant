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
    tags=["Authentication"]
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

        # CHECK EXISTING EMAIL
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        # LIMIT PASSWORD LENGTH
        password = user.password[:72]

        # HASH PASSWORD
        hashed_password = pwd_context.hash(
            password
        )

        # CREATE USER
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

    except Exception as e:

        print("REGISTER ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Registration Failed"
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

        return {
            "message":
            "Login Successful"
        }

    except Exception as e:

        print("LOGIN ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Login Failed"
        )