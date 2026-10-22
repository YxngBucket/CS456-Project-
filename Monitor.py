import socket
import time
from datetime import datetime

HOST = "127.0.0.1"
PORT = 6000

# If the heartbeat is not arriving within seconds,
# the service might not be working
TIMEOUT = 3

monitor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monitor.bind((HOST, PORT))

#This allows us to periodically check whether the service is timing out.
monitor.settimeout(1)


last_heartbeat = None
failure_reported = False

print("Heartbeat monitor started...:")
print(f"Listening on {HOST}:{PORT}")

while True:
    try:
        data, addr = monitor.recvfrom(1024)
        message = data.decode()

        if message == "HEARTBEAT":
            last_heartbeat = time.time()
            failure_reported = False
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] HEARTBEAT recieved")

    except socket.timeout:
        #no packet arrived during this check
        pass
    # Make sure to check whether the heartbeat has stopped
    if last_heartbeat is not None:
        elapsed = time.time() - last_heartbeat

        if elapsed > TIMEOUT and not failure_reported:
            timestamp = datatime.now().strftime("%H:%M:%S")

            alert = (
                f"[{timestamp}] ALERT: Authentication "
                f"service failure detected"
            )

            print(alert)

            with open("incident.log", "a") as log:
                log.write(alert + "|n")

            failure_reported = True
