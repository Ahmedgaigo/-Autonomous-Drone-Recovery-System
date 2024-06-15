import csv
from datetime import datetime
import threading
import time
from communicationAndTelemetry import getTelemetryData


# Logs telemetry data
def logTelemetryData(data):
    with open('telemetry_log.csv', 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'altitude', 'speed', 'coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write telemetry data
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'altitude': data['altitude'],
            'speed': data['speed'],
            'coordinates': data['coordinates']
        })


# Simulates real-time logging of telemetry data
def telemetryLogging():
    while not stop_event.is_set():
        telemetry_data = getTelemetryData()
        logTelemetryData(telemetry_data)
        time.sleep(1)  # Log data every second


# Function to analyze logged telemetry data
def analyzeTelemetryData():
    with open('telemetry_log.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        altitudes = []
        speeds = []
        for row in reader:
            altitudes.append(float(row['altitude']))
            speeds.append(float(row['speed']))

        if altitudes and speeds:
            avg_altitude = sum(altitudes) / len(altitudes)
            avg_speed = sum(speeds) / len(speeds)
            print(f"Average Altitude: {avg_altitude}")
            print(f"Average Speed: {avg_speed}")


if __name__ == "__main__":
    # Event to signal threads to stop
    stop_event = threading.Event()

    # Start telemetry logging in a separate thread
    logging_thread = threading.Thread(target=telemetryLogging)
    logging_thread.start()

    try:
        # Let the logging run for some time (e.g., 10 seconds)
        time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping telemetry logging...")

    # Signal thread to stop
    stop_event.set()
    logging_thread.join()


    # Analyze the logged telemetry data
    analyzeTelemetryData()
