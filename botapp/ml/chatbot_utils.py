import json
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm

# Load intents
with open('botapp/ml/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Prepare patterns and responses
patterns = []
responses = []
tags = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern.lower())
        responses.append(intent['responses'][0])
        tags.append(intent['tag'])

# Train TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(patterns).toarray()

# Set threshold for confidence
CONFIDENCE_THRESHOLD = 0.5

def get_response(user_input):
    user_input = user_input.lower()
    user_vec = vectorizer.transform([user_input]).toarray()[0]

    best_score = 0
    best_response = "Sorry, I didn't understand that. Can you rephrase?"
    matched_tag = "unknown"

    for i, pattern_vec in enumerate(tfidf_matrix):
        score = dot(pattern_vec, user_vec) / (norm(pattern_vec) * norm(user_vec) + 1e-6)
        if score > best_score:
            best_score = score
            best_response = responses[i]
            matched_tag = tags[i]

    if best_score < CONFIDENCE_THRESHOLD:
        return best_response  # fallback
    else:
        print(f"[DEBUG] Matched tag: {matched_tag}, confidence: {best_score:.2f}")
        return best_response
