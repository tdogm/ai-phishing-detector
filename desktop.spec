# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

project_root = Path(SPECPATH)
streamlit_data, streamlit_binaries, streamlit_hidden = collect_all("streamlit")
textblob_data, textblob_binaries, textblob_hidden = collect_all("textblob")

analysis = Analysis(
    [str(project_root / "desktop_launcher.py")],
    pathex=[str(project_root)],
    binaries=streamlit_binaries + textblob_binaries,
    datas=streamlit_data
    + textblob_data
    + [
        (str(project_root / "app.py"), "."),
        (str(project_root / "phishing_model.keras"), "."),
        (str(project_root / "scaler.pkl"), "."),
    ],
    hiddenimports=streamlit_hidden
    + textblob_hidden
    + [
        "joblib",
        "pandas",
        "sklearn",
        "streamlit.web.cli",
        "tensorflow",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(analysis.pure)

executable = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="AI Phishing Detector",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

bundle = COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AI Phishing Detector",
)

if sys.platform == "darwin":
    app = BUNDLE(
        bundle,
        name="AI Phishing Detector.app",
        icon=None,
        bundle_identifier="co.thomasmoran.ai-phishing-detector",
    )
