"""Launch the Streamlit detector from a packaged desktop application."""

from __future__ import annotations

import os
import socket
import sys
import threading
import webbrowser
from pathlib import Path

from streamlit.web import cli as streamlit_cli


def bundle_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        return int(server.getsockname()[1])


def main() -> None:
    app_dir = bundle_dir()
    port = available_port()

    os.chdir(app_dir)
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

    threading.Timer(
        1.5,
        lambda: webbrowser.open(f"http://127.0.0.1:{port}"),
    ).start()

    sys.argv = [
        "streamlit",
        "run",
        str(app_dir / "app.py"),
        "--server.address=127.0.0.1",
        f"--server.port={port}",
        "--server.headless=true",
        "--server.fileWatcherType=none",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]
    streamlit_cli.main()


if __name__ == "__main__":
    main()
