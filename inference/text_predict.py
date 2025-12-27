import joblib

model = joblib.load("models/text_emotion_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def predict_text_emotion(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]
