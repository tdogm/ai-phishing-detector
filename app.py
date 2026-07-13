import re
from pathlib import Path

import pandas as pd
import tensorflow as tf
import joblib
import streamlit as st
from textblob import TextBlob

APP_DIR = Path(__file__).resolve().parent

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="AI Phishing Email Detector",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #0f172a;
}

.subtitle {
    font-size: 18px;
    color: #475569;
}

.card {
    background-color: #f8fafc;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

.high-risk {
    background-color: #fee2e2;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ef4444;
}

.medium-risk {
    background-color: #fef3c7;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #f59e0b;
}

.low-risk {
    background-color: #dcfce7;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #22c55e;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_ai_model():
    model = tf.keras.models.load_model(APP_DIR / "phishing_model.keras")
    scaler = joblib.load(APP_DIR / "scaler.pkl")
    return model, scaler

model, scaler = load_ai_model()

PHISHING_EXAMPLE = (
    "URGENT: Your account has been suspended. Click here immediately to verify "
    "your password: http://fake-bank-login.com"
)

SAFE_EXAMPLE = (
    "Hello everyone, thank you for joining our weekly project meeting. We reviewed "
    "the latest design, discussed the testing schedule, and agreed on the next set "
    "of assignments. The development work is moving forward as planned, and the "
    "team will share another progress update during our regular meeting next "
    "Tuesday. Please add your comments to the shared notes before then so we can "
    "include them in the agenda. I appreciate everyone's time and thoughtful "
    "feedback. Have a great afternoon, and I look forward to speaking with you "
    "again next week. Best, Thomas"
)


def load_example(example_text):
    st.session_state.email_text = example_text

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🛡️ Project Info")
st.sidebar.write("**AI Phishing Email Detector**")
st.sidebar.write("Built with Python, TensorFlow, Streamlit, pandas, and scikit-learn.")

st.sidebar.markdown("---")
st.sidebar.write("### What it checks")
st.sidebar.write("- Links")
st.sidebar.write("- Attachments")
st.sidebar.write("- Urgent language")
st.sidebar.write("- Password/account wording")
st.sidebar.write("- Spelling issues")
st.sidebar.write("- Email length")

st.sidebar.markdown("---")
st.sidebar.write("### Project Purpose")
st.sidebar.write(
    "This tool demonstrates how machine learning can support phishing email detection and cybersecurity awareness."
)

# -----------------------------
# Feature Extraction Function
# -----------------------------
def analyze_email(email_text):
    text_lower = email_text.lower()

    # Detect links
    has_link = 1 if re.search(r"(http|https|www\.|\.com|\.net|\.org|\.io)", text_lower) else 0

    # Detect attachment/file language
    attachment_keywords = [
        "attachment",
        "attached",
        "invoice",
        "pdf",
        "document",
        "file",
        "download"
    ]

    has_attachment = 1 if any(word in text_lower for word in attachment_keywords) else 0

    # Urgency words
    urgent_words = [
        "urgent",
        "immediately",
        "verify",
        "suspended",
        "warning",
        "action required",
        "click now",
        "limited time",
        "final notice",
        "act now",
        "important"
    ]

    urgency_score = sum(
        2 for word in urgent_words if word in text_lower
    )

    if has_link == 1:
        urgency_score += 2

    if "password" in text_lower:
        urgency_score += 2

    if "account" in text_lower:
        urgency_score += 1

    if "login" in text_lower:
        urgency_score += 1

    urgency_score = min(urgency_score, 10)

    # Spelling error estimate
    words = email_text.split()
    spelling_errors = 0

    for word in words:
        cleaned_word = re.sub(r"[^a-zA-Z]", "", word)

        if cleaned_word and len(cleaned_word) > 3:
            corrected = str(TextBlob(cleaned_word).correct())
            if corrected.lower() != cleaned_word.lower():
                spelling_errors += 1

    # Email length
    email_length_words = len(words)

    # DataFrame for model
    sample_email = pd.DataFrame([{
        "has_link": has_link,
        "has_attachment": has_attachment,
        "urgency_score": urgency_score,
        "spelling_errors": spelling_errors,
        "email_length_words": email_length_words
    }])

    sample_scaled = scaler.transform(sample_email)
    prediction = model.predict(sample_scaled)[0][0]

    ml_score = round(float(prediction) * 100, 2)

    # Rule-based support score
    rule_score = 0

    if has_link == 1:
        rule_score += 25

    if has_attachment == 1:
        rule_score += 10

    if urgency_score >= 8:
        rule_score += 30
    elif urgency_score >= 5:
        rule_score += 20
    elif urgency_score >= 3:
        rule_score += 10

    if "password" in text_lower or "login" in text_lower or "verify" in text_lower:
        rule_score += 20

    if spelling_errors >= 3:
        rule_score += 10

    if email_length_words < 20:
        rule_score += 5

    rule_score = min(rule_score, 100)

    # Conservative cybersecurity score
    final_score = max(ml_score, rule_score)

    return {
        "final_score": final_score,
        "ml_score": ml_score,
        "rule_score": rule_score,
        "has_link": has_link,
        "has_attachment": has_attachment,
        "urgency_score": urgency_score,
        "spelling_errors": spelling_errors,
        "email_length_words": email_length_words
    }

# -----------------------------
# Main Page
# -----------------------------
st.markdown('<div class="main-title">🛡️ AI Phishing Email Detector</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Paste an email below to analyze its phishing risk using machine learning and security rules.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# Example buttons
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

col_example1, col_example2 = st.columns(2)

with col_example1:
    st.button(
        "Load Phishing Example",
        on_click=load_example,
        args=(PHISHING_EXAMPLE,)
    )

with col_example2:
    st.button(
        "Load Safe Example",
        on_click=load_example,
        args=(SAFE_EXAMPLE,)
    )

email_text = st.text_area(
    "Paste email text here:",
    key="email_text",
    height=220
)

analyze_button = st.button("Analyze Email")

if analyze_button:
    if email_text.strip() == "":
        st.warning("Please paste an email before analyzing.")
    else:
        result = analyze_email(email_text)

        final_score = result["final_score"]

        st.markdown("---")
        st.subheader("Final Risk Result")

        if final_score >= 70:
            st.markdown(
                f'<div class="high-risk"><h2>High Risk: {final_score}%</h2><p>Result: Likely phishing</p></div>',
                unsafe_allow_html=True
            )
        elif final_score >= 40:
            st.markdown(
                f'<div class="medium-risk"><h2>Medium Risk: {final_score}%</h2><p>Result: Suspicious</p></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="low-risk"><h2>Low Risk: {final_score}%</h2><p>Result: Likely safe</p></div>',
                unsafe_allow_html=True
            )

        st.progress(int(final_score))

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("ML Model Score", f"{result['ml_score']}%")

        with col2:
            st.metric("Rule-Based Score", f"{result['rule_score']}%")

        with col3:
            st.metric("Final Risk Score", f"{result['final_score']}%")

        st.markdown("---")
        st.subheader("Analysis Details")

        detail_col1, detail_col2, detail_col3, detail_col4, detail_col5 = st.columns(5)

        with detail_col1:
            st.metric("Has Link", result["has_link"])

        with detail_col2:
            st.metric("Attachment Mentioned", result["has_attachment"])

        with detail_col3:
            st.metric("Urgency Score", result["urgency_score"])

        with detail_col4:
            st.metric("Spelling Errors", result["spelling_errors"])

        with detail_col5:
            st.metric("Word Count", result["email_length_words"])

        st.markdown("---")
        st.subheader("Why this result?")

        reasons = []

        if result["has_link"] == 1:
            reasons.append("The email contains a link, which can be risky when paired with urgent language.")

        if result["has_attachment"] == 1:
            reasons.append("The email mentions an attachment, file, invoice, or document.")

        if result["urgency_score"] >= 5:
            reasons.append("The email uses pressure-based or urgent wording.")

        if result["spelling_errors"] >= 3:
            reasons.append("The email contains multiple possible spelling issues.")

        if result["email_length_words"] < 20:
            reasons.append("The email is very short, which can appear in simple phishing attempts.")

        if len(reasons) == 0:
            st.write("No major phishing indicators were detected.")

        for reason in reasons:
            st.write("- " + reason)

        st.markdown("---")
        st.caption(
            "Note: This is an educational cybersecurity project. It should not be used as the only method for deciding whether an email is safe."
        )
