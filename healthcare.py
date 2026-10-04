import requests
import csv
import os
import time
from datetime import datetime

# ==================================================
# SMART HEALTHCARE BLYNK DATA COLLECTOR
# ==================================================

# Paste your NEW Blynk Auth Token here
BLYNK_AUTH_TOKEN = "8mLWjvkp2v-MjGTi4OwXzx3Vc0xxWUeS"

# CSV file name
CSV_FILE = "healthcare_data.csv"


# ==================================================
# CREATE CSV FILE
# ==================================================

if not os.path.exists(CSV_FILE):

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Time",
            "Heart Rate (BPM)",
            "SpO2 (%)",
            "Body Temperature (C)",
            "Room Temperature (C)",
            "Humidity (%)",
            "Gas/Smoke",
            "Motion Detected",
            "Fall Detection",
            "SOS Status",
            "Emergency Status"
        ])

    print("CSV file created successfully!")


# ==================================================
# GET DATA FROM BLYNK
# ==================================================

def get_blynk_data(pin):

    try:

        url = (
            f"https://blynk.cloud/external/api/get"
            f"?token={BLYNK_AUTH_TOKEN}&{pin}"
        )

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.text.strip()

        print(f"Error reading {pin}")
        print("Status Code:", response.status_code)

        return "ERROR"

    except requests.exceptions.RequestException as error:

        print(f"Connection Error for {pin}: {error}")

        return "ERROR"


# ==================================================
# SAVE DATA
# ==================================================

def save_data():

    # Get current date and time
    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")


    # ==============================================
    # READ ALL BLYNK DATASTREAMS
    # ==============================================

    heart_rate = get_blynk_data("V0")

    spo2 = get_blynk_data("V1")

    body_temp = get_blynk_data("V2")

    room_temp = get_blynk_data("V3")

    humidity = get_blynk_data("V4")

    gas = get_blynk_data("V5")

    motion = get_blynk_data("V6")

    fall = get_blynk_data("V7")

    sos = get_blynk_data("V8")

    emergency_status = get_blynk_data("V9")


    # ==============================================
    # SAVE DATA TO CSV
    # ==============================================

    try:

        with open(
            CSV_FILE,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                date,
                current_time,
                heart_rate,
                spo2,
                body_temp,
                room_temp,
                humidity,
                gas,
                motion,
                fall,
                sos,
                emergency_status
            ])

        print("\n==============================================")
        print("HEALTHCARE DATA SAVED SUCCESSFULLY")
        print("==============================================")

        print("Date:", date)
        print("Time:", current_time)
        print("Heart Rate:", heart_rate)
        print("SpO2:", spo2)
        print("Body Temperature:", body_temp)
        print("Room Temperature:", room_temp)
        print("Humidity:", humidity)
        print("Gas/Smoke:", gas)
        print("Motion Detected:", motion)
        print("Fall Detection:", fall)
        print("SOS Status:", sos)
        print("Emergency Status:", emergency_status)


    except PermissionError:

        print("\n⚠ ERROR: Cannot save the CSV file.")
        print("Please close healthcare_data.csv if it is open in Excel.")


    except Exception as error:

        print("\nCSV Error:", error)


# ==================================================
# MAIN PROGRAM
# ==================================================

print("==============================================")
print("SMART HEALTHCARE DATA COLLECTOR STARTED")
print("==============================================")

print("Collecting data from Blynk...")
print("Press CTRL + C to stop the program.")


try:

    while True:

        save_data()

        print("\nWaiting 60 seconds...\n")

        time.sleep(60)


except KeyboardInterrupt:

    print("\n==============================================")
    print("HEALTHCARE DATA COLLECTION STOPPED SAFELY")
    print("==============================================")