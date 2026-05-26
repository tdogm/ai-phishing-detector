import re
import pandas as pd
import tensorflow as tf
import joblib
import streamlit as st
from textblob import TextBlob

# Load saved model and scaler
model = tf.keras.models.load_model("phishing_model.keras")
scaler = joblib.load("scaler.pkl")

st.set_page_config(
    page_title="AI Phishing Email Detector",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ AI Phishing Email Detector")
st.write("Paste an email below and the AI will analyze whether it looks suspicious.")

email_text = st.text_area("Paste email text here:", height=200)

def analyze_email(email_text):
    # Detect links
    has_link = 1 if re.search(r"http|www|\.com", email_text.lower()) else 0

    # Detect attachment words
    attachment_keywords = [
        "attachment",
        "attached",
        "invoice",
        "pdf",
        "document",
        "file"
    ]

    has_attachment = 1 if any(word in email_text.lower() for word in attachment_keywords) else 0

    # Detect urgency
    urgent_words = [
        "urgent",
        "immediately",
        "verify",
        "suspended",
        "warning",
        "action required",
        "click now",
        "limited time"
    ]

    urgency_score = sum(
        2 for word in urgent_words if word in email_text.lower()
    )

    if has_link == 1:
        urgency_score += 2

    if "password" in email_text.lower():
        urgency_score += 2

    if "account" in email_text.lower():
        urgency_score += 1

    urgency_score = min(urgency_score, 10)

    # Approximate spelling errors
    words = email_text.split()
    spelling_errors = 0

    for word in words:
        cleaned_word = re.sub(r"[^a-zA-Z]", "", word)

        if cleaned_word:
            corrected = str(TextBlob(cleaned_word).correct())
            if corrected.lower() != cleaned_word.lower():
                spelling_errors += 1

    # Email length
    email_length_words = len(words)

    sample_email = pd.DataFrame([{
        "has_link": has_link,
        "has_attachment": has_attachment,
        "urgency_score": urgency_score,
        "spelling_errors": spelling_errors,
        "email_length_words": email_length_words
    }])

    sample_scaled = scaler.transform(sample_email)
    prediction = model.predict(sample_scaled)[0][0]

    risk_score = round(float(prediction) * 100, 2)

    return {
        "risk_score": risk_score,
        "has_link": has_link,
        "has_attachment": has_attachment,
        "urgency_score": urgency_score,
        "spelling_errors": spelling_errors,
        "email_length_words": email_length_words
    }

if st.button("Analyze Email"):
    if email_text.strip() == "":
        st.warning("Please paste an email first.")
    else:
        result = analyze_email(email_text)

        st.subheader("Final Result")

        risk_score = result["risk_score"]

        if risk_score >= 70:
            st.error(f"High Risk: {risk_score}%")
            st.write("Result: Likely phishing")
        elif risk_score >= 40:
            st.warning(f"Medium Risk: {risk_score}%")
            st.write("Result: Suspicious")
        else:
            st.success(f"Low Risk: {risk_score}%")
            st.write("Result: Likely safe")

        st.subheader("Analysis Details")

        st.write("Has Link:", result["has_link"])
        st.write("Has Attachment:", result["has_attachment"])
        st.write("Urgency Score:", result["urgency_score"])
        st.write("Spelling Errors:", result["spelling_errors"])
        st.write("Email Length:", result["email_length_words"], "words")

        st.subheader("Why this result?")

        if result["has_link"] == 1:
            st.write("- The email contains a link.")

        if result["has_attachment"] == 1:
            st.write("- The email mentions an attachment or file.")

        if result["urgency_score"] >= 5:
            st.write("- The email uses urgent or pressure-based language.")

        if result["spelling_errors"] >= 3:
            st.write("- The email has multiple possible spelling errors.")

        if result["email_length_words"] < 20:
            st.write("- The email is very short, which can appear in simple phishing attempts.")