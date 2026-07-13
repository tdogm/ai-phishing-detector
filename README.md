# AI Phishing Email Detector

A cybersecurity machine-learning project that combines a TensorFlow model with security rules to estimate the phishing risk of pasted email text.

## Download the desktop app

Download the newest packaged version from [GitHub Releases](https://github.com/tdogm/ai-phishing-detector/releases/latest):

- **macOS:** Download `AI-Phishing-Detector-macOS.zip`, unzip it, and open `AI Phishing Detector.app`.
- **Windows:** Download `AI-Phishing-Detector-Windows.zip`, unzip it, and open `AI Phishing Detector.exe` inside the folder.

The desktop package starts a private local server and opens the interface in your default browser. Email text stays on the computer and is not sent to a hosted service by this application.

Unsigned applications can trigger a macOS Gatekeeper or Windows SmartScreen warning. Review the public source code before running the download.

## Features

- Scores pasted email text with a trained TensorFlow model.
- Checks links, attachments, urgency, account wording, spelling, and length.
- Shows the machine-learning score, supporting rule score, and detected signals.
- Includes phishing and safe-message examples for quick testing.
- Provides Streamlit and packaged desktop interfaces.

## Run from source

Python 3.11 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Build desktop packages

The `Build desktop apps` GitHub Actions workflow builds separate macOS and Windows packages and publishes them to a GitHub Release. It runs when packaging files change, when a version tag is pushed, or when manually started from the Actions tab.

To test a local package:

```bash
pip install pyinstaller
pyinstaller --noconfirm --clean desktop.spec
```

## Technology

Python, TensorFlow, pandas, scikit-learn, Streamlit, TextBlob, joblib, PyInstaller, and GitHub Actions.

## Responsible use

This project is an educational portfolio tool, not a replacement for professional email-security controls. Do not treat its score as the only basis for opening, deleting, or reporting a message.
