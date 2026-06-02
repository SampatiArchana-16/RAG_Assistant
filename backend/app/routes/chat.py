from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from app.database import SessionLocal
from app.models import ChatHistory

import shutil

from app.rag import (
    process_pdf,
    search_answer
)

router = APIRouter()


@router.post("/chat")
async def chat_with_pdf(

    file: UploadFile = File(...),

    question: str = Form(...),

    email: str = Form(...)
):

    try:

        # SAVE FILE
        file_location = f"temp_{file.filename}"

        with open(file_location, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # PROCESS PDF
        process_pdf(file_location)

        # GET ANSWER
        answer = search_answer(question)

        db = SessionLocal()

        chat = ChatHistory(
        user_email=email,
        question=question,
        answer=answer
    )

        db.add(chat)

        db.commit()

        db.close()

        return {
            "answer": answer
        }

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return {
            "answer": str(e)
        }
    

@router.get("/history/{email}")
def get_history(email: str):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_email == email
    ).all()

    result = []

    for chat in chats:

        result.append({
            "question": chat.question,
            "answer": chat.answer
        })

    db.close()

    return result