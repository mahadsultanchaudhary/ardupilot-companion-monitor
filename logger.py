import csv
import os
from datetime import datetime

class FlightLogger:
    def __init__(self, filename="flight_data.csv"):
        self.filename = filename
        self.headers = ["Timestamp", "CPU Load (%)", "Temperature (°C)", "System Status"]
        
        # Initialize the file with headers if it's new
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
            print(f"📄 Created new log file: {self.filename}")

    def log(self, cpu: float, temp: float, status: str = "NORMAL"):
        """
        Records flight health data with units for better readability.
        """
        timestamp = datetime.now().strftime("%H:%M:%S") # Clean time format
        
        # Formatting values with symbols as requested
        cpu_str = f"{cpu}%"
        temp_str = f"{temp}°C"
        status_str = status.upper()

        try:
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, cpu_str, temp_str, status_str])
        except PermissionError:
            print(f"⚠️ Warning: Could not write to {self.filename}. Is it open in Excel?")