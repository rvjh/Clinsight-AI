from fastapi import FastAPI
from pydantic import BaseModel

from functions.symptom_extractor import extract_symptoms
from functions.diagnosis_symptoms import get_diagnosis
from functions.pubmed_articles import fetch_pubmed_articles_with_metadata
from functions.summerize_pubmed import summarize_text

app = FastAPI(title="Clinsight-AI")


class SymptomInput(BaseModel):
    description: str


def _articles_to_text(articles: list[dict]) -> str:
    parts = []
    for article in articles:
        title = article.get("title", "Untitled")
        abstract = article.get("abstract", "")
        parts.append(f"{title}\n{abstract}")
    return "\n\n".join(parts)


@app.post("/diagnosis")
def run_diagnosis(data: SymptomInput):
    symptoms = extract_symptoms(data.description)
    diagnosis_result = get_diagnosis(symptoms)

    search_query = " ".join(symptoms) if symptoms else data.description
    pubmed_articles = fetch_pubmed_articles_with_metadata(search_query)

    abstract_text = _articles_to_text(pubmed_articles)
    summary = summarize_text(
        abstract_text[:3000] if abstract_text else "No PubMed abstracts found."
    )

    return {
        "symptoms": symptoms,
        "diagnosis": diagnosis_result,
        "pubmed_articles": pubmed_articles,
        "pubmed_summary": summary,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
