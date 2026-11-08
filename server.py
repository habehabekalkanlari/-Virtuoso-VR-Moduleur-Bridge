"""
Launcher: starts both the HTTP server (port 8000) and the
Virtuoso OSC-to-WebSocket bridge (bridge_server.py) together.

Usage: python server.py
"""

import subprocess
import http.server
import socketserver
import sys
import os

HTTP_PORT = 8000


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    bridge = subprocess.Popen(
        [sys.executable, "bridge_server.py"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    print(f"[HTTP] Serving on http://localhost:{HTTP_PORT}")
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", HTTP_PORT), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        bridge.terminate()
        bridge.wait()
        print("\nStopped.")


if __name__ == "__main__":
    main()
