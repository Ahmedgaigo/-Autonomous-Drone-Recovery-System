import socket
import threading
import time
import json
import random

# Example ground station IP and port
ground_station_address = ('localhost', 8888)


# Telemetry data (altitude, speed, GPS coordinates. Simulated for demonstration)
def getTelemetryData():
    current_x, current_y = random.uniform(0, 100), random.uniform(0, 100)  # Simulated coordinates
    return {
        'altitude': random.uniform(0, 100),
        'speed': random.uniform(0, 20),
        'coordinates': (current_x, current_y)
    }


# Sends telemetry data
def sendTelemetryData():
    while not stop_event.is_set():
        telemetry_data = getTelemetryData()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(ground_station_address)
                s.sendall(json.dumps(telemetry_data).encode())
        except Exception as e:
            print(f"Failed to send telemetry data: {e}")
        time.sleep(1)  # Send telemetry data every second


# Receives commands
def receiveCommands():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ground_station_address)
        s.listen()
        while not stop_event.is_set():
            try:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while not stop_event.is_set():
                        command = conn.recv(1024)
                        if not command:
                            break
                        # Process received command (e.g., update mission parameters)
                        print(f"Received command: {command.decode()}")
            except Exception as e:
                print(f"Failed to receive commands: {e}")


if __name__ == "__main__":
    # Event to signal threads to stop
    stop_event = threading.Event()

    # Start telemetry data sending and command receiving threads
    send_thread = threading.Thread(target=sendTelemetryData)
    receive_thread = threading.Thread(target=receiveCommands)

    send_thread.start()
    receive_thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Shutting down...")

    # Signal threads to stop
    stop_event.set()

    # Wait for threads to finish
    send_thread.join()
    receive_thread.join()

    print("Shutdown complete.")
