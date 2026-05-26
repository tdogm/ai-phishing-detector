import joblib
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import layers, models

# Load dataset
df = pd.read_csv("phishing_email_detection_2026_dataset.csv")

# Features
X = df[[
    "has_link",
    "has_attachment",
    "urgency_score",
    "spelling_errors",
    "email_length_words"
]]

# Labels
y = df["is_phishing"]

# Normalize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

# Build TensorFlow model
model = models.Sequential([
    layers.Dense(16, activation="relu", input_shape=(X_train.shape[1],)),
    layers.Dense(8, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

# Compile model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Train model
model.fit(
    X_train,
    y_train,
    epochs=20,
    validation_data=(X_test, y_test)
)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)

print("\nTest Accuracy:", round(accuracy * 100, 2), "%")

# Example prediction
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

model.save("phishing_model.keras")

import joblib

joblib.dump(scaler, "scaler.pkl")

model.save("phishing_model.keras")
joblib.dump(scaler, "scaler.pkl")

print("\nModel saved as phishing_model.keras")
print("Scaler saved as scaler.pkl")