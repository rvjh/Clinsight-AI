import re

def extract_symptoms(text: str) -> list[str]:
    symptoms = re.findall(f"\b(headache|cough|fever|fatigue|nausea|vomiting|diarrhea|constipation|abdominal pain|back pain|joint pain|muscle pain|joint stiffness|muscle stiffness|joint swelling|muscle swelling|joint redness|muscle redness|joint warmth|muscle warmth|joint cold|muscle cold|joint numbness|muscle numbness|joint tingling|muscle tingling|joint weakness|muscle weakness|joint stiffness|muscle stiffness|joint swelling|muscle swelling|joint redness|muscle redness|joint warmth|muscle warmth|joint cold|muscle cold|joint numbness|muscle numbness|joint tingling|muscle tingling|joint weakness|muscle weakness)\b", text.lower())
    return list(set(symptoms))

