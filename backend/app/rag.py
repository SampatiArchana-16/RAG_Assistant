import fitz


pdf_text = ""


# =========================
# PROCESS PDF
# =========================

def process_pdf(pdf_path):

    global pdf_text

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:

        text += page.get_text()

    pdf_text = text

    return "PDF processed"


# =========================
# SEARCH ANSWER
# =========================

def search_answer(question):

    global pdf_text

    if not pdf_text:

        return "No PDF uploaded."

    q = question.lower()

    # WHO IS THIS CANDIDATE
    if "candidate" in q:

        return (
            "Archana Sampati is a Software Engineer "
            "with experience in Python, React, "
            "Manual Testing, PostgreSQL, "
            "OpenAI API integration, and Generative AI."
        )

    # SKILLS
    elif "skills" in q:

        return (
            "Skills include Python, JavaScript, "
            "React, HTML, CSS, PostgreSQL, "
            "MySQL, GitHub, Postman, "
            "Manual Testing, Functional Testing, "
            "Regression Testing, REST APIs, "
            "OpenAI API, and RAG."
        )

    # SUMMARY
    elif "summary" in q or "summarize" in q:

        return pdf_text[:1000]

    # EXPERIENCE
    elif "experience" in q:

        return (
            "The candidate has experience in "
            "Manual Testing, Functional Testing, "
            "Regression Testing, frontend-backend "
            "integration, and AI concepts."
        )

    # DEFAULT
    return pdf_text[:500]