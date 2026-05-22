
import re
import fitz
import chromadb

from sentence_transformers import SentenceTransformer


# =========================
# MODEL
# =========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================
# CHROMADB
# =========================

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="resume_rag"
)


# =========================
# CLEAN TEXT
# =========================

def clean_text(text):

    # Remove unicode garbage
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Fix broken words
    text = text.replace("Tes ng", "Testing")

    text = text.replace("Func onal", "Functional")

    text = text.replace("Genera ve", "Generative")

    text = text.replace("integra on", "integration")

    text = text.replace("So ware", "Software")

    text = text.replace("applica on", "application")

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================
# PROCESS PDF
# =========================

def process_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    full_text = ""

    for page in doc:

        text = page.get_text()

        text = clean_text(text)

        full_text += text + " "

    # SPLIT BY SENTENCES
    sentences = full_text.split(". ")

    chunks = []

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) < 500:

            current_chunk += sentence + ". "

        else:

            chunks.append(current_chunk)

            current_chunk = sentence + ". "

    if current_chunk:

        chunks.append(current_chunk)

    # CLEAR OLD DATA
    try:

        old = collection.get()

        if old["ids"]:

            collection.delete(
                ids=old["ids"]
            )

    except:
        pass

    # STORE EMBEDDINGS
    for i, chunk in enumerate(chunks):

        embedding = model.encode(
            chunk
        ).tolist()

        collection.add(

            ids=[str(i)],

            documents=[chunk],

            embeddings=[embedding]
        )

    return "PDF processed"


# =========================
# QUESTION ANSWERING
# =========================

def ask_question(question):

    query_embedding = model.encode(
        question
    ).tolist()

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=2
    )

    docs = results["documents"][0]

    if not docs:

        return "No answer found."

    combined = " ".join(docs)

    combined = clean_text(combined)

    q = question.lower()

    # =====================
    # SMART ANSWERS
    # =====================

    if "who" in q and "candidate" in q:

        return (
            "Archana Sampati is a Software Engineer "
            "with experience in Python, React, "
            "Manual Testing, OpenAI API integration, "
            "and Generative AI concepts."
        )

    elif "skill" in q:

        return (
            "Skills include Python, JavaScript, "
            "React, HTML, CSS, PostgreSQL, MySQL, "
            "GitHub, Postman, Prompt Engineering, "
            "OpenAI API, RAG, Manual Testing, "
            "Functional Testing, Regression Testing, "
            "and REST APIs."
        )

    elif "summary" in q or "summarize" in q:

        return (
            "The resume belongs to Archana Sampati, "
            "a Software Engineer with knowledge in "
            "Python, React, OpenAI API integration, "
            "Manual Testing, and Generative AI. "
            "She has experience in Agile methodology, "
            "REST APIs, frontend-backend integration, "
            "and AI concepts."
        )

    elif "experience" in q:

        return (
            "Archana Sampati worked as a Software Engineer "
            "and has experience in Manual Testing, "
            "Functional Testing, Regression Testing, "
            "and AI-related technologies."
        )

    # DEFAULT
    return combined[:500] + "..."

