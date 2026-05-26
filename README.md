\# AI Phishing Email Detector



This project is a beginner-friendly cybersecurity machine learning tool that uses TensorFlow to detect possible phishing emails.



\## Features



\- Trains a TensorFlow model on phishing email data

\- Uses email features such as links, attachments, urgency, spelling errors, and word count

\- Saves the trained model for future use

\- Allows users to paste email text into a Streamlit web app

\- Displays a phishing risk score and explanation



\## Tools Used



\- Python

\- TensorFlow

\- pandas

\- scikit-learn

\- Streamlit

\- TextBlob



\## How It Works



The program analyzes an email and extracts features such as:



\- Whether the email contains a link

\- Whether it mentions an attachment

\- Whether it uses urgent language

\- Approximate spelling errors

\- Email length



These features are passed into a trained TensorFlow model, which predicts whether the email is likely safe or suspicious.



\## How to Run



Install dependencies:



```bash

pip install -r requirements.txt

