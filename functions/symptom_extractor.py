import re

SYMPTOM_PATTERN = re.compile(
    r"\b("
    r"headache|cough|fever|fatigue|nausea|vomiting|diarrhea|constipation|"
    r"abdominal pain|back pain|joint pain|muscle pain|joint stiffness|"
    r"muscle stiffness|joint swelling|muscle swelling|joint redness|"
    r"muscle redness|joint warmth|muscle warmth|joint cold|muscle cold|"
    r"joint numbness|muscle numbness|joint tingling|muscle tingling|"
    r"joint weakness|muscle weakness"
    r")\b",
    re.IGNORECASE,
)


def extract_symptoms(text: str) -> list[str]:
    symptoms = SYMPTOM_PATTERN.findall(text)
    return list(dict.fromkeys(symptoms))
