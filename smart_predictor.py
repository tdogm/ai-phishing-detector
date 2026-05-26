import re
import pandas as pd
import tensorflow as tf
import joblib

from textblob import TextBlob

# Load saved AI model
model = tf.keras.models.load_model("phishing_model.keras")
scaler = joblib.load("scaler.pkl")

print("\n=== Smart Phishing Detector ===")

print("\nPaste the email text below.")
print("When finished, type DONE on a new line and press Enter.\n")

lines = []

while True:
    line = input()
    if line.strip().upper() == "DONE":
        break
    lines.append(line)

email_text = "\n".join(lines)
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
# Approximate spelling issues
words = email_text.split()

spelling_errors = 0

for word in words:
    corrected = str(TextBlob(word).correct())
    if corrected.lower() != word.lower():
        spelling_errors += 1

# Email length
email_length_words = len(words)

# Build dataframe
sample_email = pd.DataFrame([{
    "has_link": has_link,
    "has_attachment": has_attachment,
    "urgency_score": urgency_score,
    "spelling_errors": spelling_errors,
    "email_length_words": email_length_words
}])

# Scale data
sample_scaled = scaler.transform(sample_email)

# Predict
prediction = model.predict(sample_scaled)[0][0]

print("\n=== Analysis ===")
print("Has Link:", has_link)
print("Has Attachment:", has_attachment)
print("Urgency Score:", urgency_score)
print("Spelling Errors:", spelling_errors)
print("Email Length:", email_length_words)

risk_score = round(float(prediction) * 100, 2)

print("\n=== Final Result ===")
print("Risk Score:", risk_score, "%")

if risk_score >= 70:
    print("Risk Level: High")
    print("Result: Likely phishing")
elif risk_score >= 40:
    print("Risk Level: Medium")
    print("Result: Suspicious")
else:
    print("Risk Level: Low")
    print("Result: Likely safe")

print("\n=== Why this result? ===")

if has_link == 1:
    print("- The email contains a link.")

if has_attachment == 1:
    print("- The email mentions an attachment or file.")

if urgency_score >= 5:
    print("- The email uses urgent or pressure-based language.")

if spelling_errors >= 3:
    print("- The email has multiple possible spelling errors.")

if email_length_words < 20:
    print("- The email is very short, which can be common in simple phishing attempts.")