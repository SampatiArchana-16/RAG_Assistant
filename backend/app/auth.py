from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

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


# REGISTER
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

        # HASH PASSWORD
        hashed_password = pwd_context.hash(
            user.password
        )

        # CREATE USER
        new_user = User(
            email=user.email,
            password=hashed_password
        )

        # SAVE USER
        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        print("USER SAVED SUCCESSFULLY")

        return {
            "message":
            "Registration Successful"
        }

    except Exception as e:

        print("REGISTER ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# LOGIN
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
            status_code=400,
            detail="Invalid Email"
        )

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid Password"
        )

    return {
        "message":
        "Login Successful"
    }