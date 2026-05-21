from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

import shutil

import os

from app.rag import (
    process_pdf,
    search_answer
)

router = APIRouter(
    prefix="/chat"
)


@router.post("/ask")
async def ask_question(
    pdf: UploadFile = File(...),
    question: str = Form(...)
):

    try:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        file_path = f"uploads/{pdf.filename}"

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                pdf.file,
                buffer
            )

        index, chunks = process_pdf(
            file_path
        )

        answer = search_answer(
            question,
            index,
            chunks
        )

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "answer": str(e)
        }