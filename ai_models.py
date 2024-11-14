import joblib
from utils import clean_text

# Load pre-trained models
vectorizer = joblib.load("models/vectorizer.pkl")
classifier = joblib.load("models/classifier.pkl")

def classify_text(text):
    processed_text = vectorizer.transform([clean_text(text)])
    category = classifier.predict(processed_text)
    return category[0]
