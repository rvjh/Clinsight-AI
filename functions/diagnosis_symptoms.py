import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_diagnosis(symptoms: list[str]) -> str:
    prompt = f"Patient has the following symptoms: {', '.join(symptoms)}. Please suggest a diagnosis for the patient."
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests a diagnosis for a patient based on their symptoms."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
