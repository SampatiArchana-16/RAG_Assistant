import fitz

from sentence_transformers import SentenceTransformer

import faiss

import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def process_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    chunks = text.split(".")

    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return index, chunks


def search_answer(
    question,
    index,
    chunks
):

    question_embedding = model.encode(
        [question]
    )

    distances, indices = index.search(
        np.array(question_embedding).astype(
            "float32"
        ),
        3
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):
            results.append(chunks[idx])

    return " ".join(results)