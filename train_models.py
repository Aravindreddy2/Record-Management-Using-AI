from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Sample data for training (replace with actual data)
texts = [
    "financial report for the year",
    "employee performance review",
    "quarterly sales meeting",
    "new product launch",
    "HR policies update"
]
labels = [0, 1, 0, 1, 1]  # Replace with your actual categories

# Initialize and train vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Initialize and train classifier
classifier = LogisticRegression()
classifier.fit(X, labels)

# Save the trained models to the models directory
joblib.dump(vectorizer, "models/vectorizer.pkl")
joblib.dump(classifier, "models/classifier.pkl")

print("Models saved successfully!")
