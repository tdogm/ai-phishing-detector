import pandas as pd
import tensorflow as tf
import joblib

model = tf.keras.models.load_model("phishing_model.keras")
scaler = joblib.load("scaler.pkl")

print("\nEnter email details:")

has_link = int(input("Does the email have a link? 1 = yes, 0 = no: "))
has_attachment = int(input("Does the email have an attachment? 1 = yes, 0 = no: "))
urgency_score = int(input("Urgency score from 1-10: "))
spelling_errors = int(input("Number of spelling errors: "))
email_length_words = int(input("Approximate email length in words: "))

sample_email = pd.DataFrame([{
    "has_link": has_link,
    "has_attachment": has_attachment,
    "urgency_score": urgency_score,
    "spelling_errors": spelling_errors,
    "email_length_words": email_length_words
}])

sample_scaled = scaler.transform(sample_email)

prediction = model.predict(sample_scaled)[0][0]

print("\nPhishing Probability:", round(float(prediction), 2))

if prediction > 0.5:
    print("Result: Likely phishing")
else:
    print("Result: Likely safe")