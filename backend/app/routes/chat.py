from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

import shutil

from app.rag import (
    process_pdf,
    search_answer
)

router = APIRouter()


@router.post("/chat")
async def chat_with_pdf(

    file: UploadFile = File(...),

    question: str = Form(...)
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

        return {
            "answer": answer
        }

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return {
            "answer": str(e)
        }