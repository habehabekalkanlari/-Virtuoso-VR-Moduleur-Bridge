"""
Virtuoso VR -> Moduleur Brain Bridge Server
- Listens OSC on UDP 9003 from Virtuoso
- Forwards to Web UI via WebSocket (port 8765)
- Listens Autoconnect broadcasts on UDP 9002

Install: pip install python-osc websockets

Usage:
  python bridge_server.py

Virtuoso Settings:
  - Enable Remote Control in Track Settings
  - Set IP to this computer's IP
  - Or use Autoconnect (this server listens on UDP 9002)
"""

import asyncio
import json
import socket
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import websockets

OSC_IP = "0.0.0.0"
OSC_PORT = 9003
BROADCAST_PORT = 9002
WS_PORT = 8765

connected_clients = set()

PARAM_MAP = {
    1: {"name": "CTRL1", "cc": 73, "module": "ADSR_A"},
    2: {"name": "CTRL2", "cc": 75, "module": "ADSR_D"},
    3: {"name": "CTRL3", "cc": 76, "module": "ADSR_S"},
    4: {"name": "CTRL4", "cc": 72, "module": "ADSR_R"},
    5: {"name": "CTRL5", "cc": 7,  "module": "MIXER_CH1"},
    6: {"name": "CTRL6", "cc": 8,  "module": "MIXER_CH2"},
    7: {"name": "L_TILT_Z", "cc": 20, "module": "VCO_COARSE"},
    8: {"name": "R_TILT_Z", "cc": 74, "module": "VCF_CUTOFF"},
    11: {"name": "WAVEMIN_LX", "cc": 20, "module": "VCO_COARSE"},
    12: {"name": "WAVEMIN_LY", "cc": 21, "module": "VCO_FINE"},
    13: {"name": "WAVEMIN_LZ", "cc": 22, "module": "VCO_WAVE"},
}


async def broadcast_ws(message):
    if connected_clients:
        await asyncio.gather(
            *[ws.send(message) for ws in connected_clients],
            return_exceptions=True,
        )


def osc_handler(address, *args):
    print(f"[OSC] {address} {args}")
    parts = address.strip("/").split("/")
    if len(parts) < 3:
        return
    _, instrument, method = parts[0], parts[1], parts[2]

    msg = {
        "type": "osc",
        "address": address,
        "instrument": instrument,
        "method": method,
        "args": args,
    }

    midi_events = []
    if method == "noteon":
        velocity = args[0] if len(args) > 0 else 0.8
        channel = int(args[1]) if len(args) > 1 else 1
        note = int(args[2]) if len(args) > 2 else 60
        midi_events.append({
            "type": "noteon", "note": note, "vel": velocity,
            "ch": channel, "module": f"{instrument.upper()}_PITCH",
        })
    elif method == "noteoff":
        channel = int(args[1]) if len(args) > 1 else 1
        note = int(args[2]) if len(args) > 2 else 60
        midi_events.append({"type": "noteoff", "note": note, "ch": channel})
    elif method.startswith("param") or method == "control":
        param_id = int(args[0]) if len(args) > 0 else 0
        value = args[1] if len(args) > 1 else 0
        mapping = PARAM_MAP.get(param_id)
        if mapping:
            midi_events.append({
                "type": "cc", "cc": mapping["cc"], "value": value,
                "module": mapping["module"], "param": mapping["name"],
            })

    msg["midi"] = midi_events
    asyncio.create_task(broadcast_ws(json.dumps(msg)))


async def ws_handler(websocket):
    connected_clients.add(websocket)
    print(f"[WS] Client connected, total {len(connected_clients)}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)


async def broadcast_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((OSC_IP, BROADCAST_PORT))
    except OSError:
        print(f"[WARN] Could not bind broadcast port {BROADCAST_PORT}")
        return
    sock.setblocking(False)
    loop = asyncio.get_event_loop()
    print(f"[BROADCAST] Listening on UDP {BROADCAST_PORT}")
    while True:
        try:
            data, addr = await loop.sock_recvfrom(sock, 1024)
            text = data.decode(errors="ignore")
            if text.startswith("VirtuosoCompanion:"):
                ip = text.split(":")[1]
                print(f"[BROADCAST] Virtuoso found at {ip}")
        except Exception:
            await asyncio.sleep(0.1)


async def main():
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(osc_handler)

    server = AsyncIOOSCUDPServer(
        (OSC_IP, OSC_PORT), dispatcher, asyncio.get_event_loop()
    )
    transport, protocol = await server.create_serve_endpoint()

    ws_server = await websockets.serve(ws_handler, "0.0.0.0", WS_PORT)

    print(f"""
+----------------------------------------------+
|  Virtuoso -> Moduleur Bridge Running         |
|  OSC: {OSC_IP}:{OSC_PORT}                           |
|  WS: ws://localhost:{WS_PORT}                  |
|  Web: http://localhost:8000                  |
|  Set Virtuoso Remote IP to this PC's IP      |
+----------------------------------------------+
    """)

    await asyncio.gather(broadcast_listener(), ws_server.wait_closed())


if __name__ == "__main__":
    asyncio.run(main())
