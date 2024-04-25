#!/bin/python3

import requests

def getAverageTemperatureForUser(userId):
    base_url = "https://jsonmock.hackerrank.com/api/medical_records"
    page = 1
    total_temps = 0
    total_records = 0

    while True:
        response = requests.get(f"{base_url}?userid={userId}&page={page}").json()
        data = response["data"]

        if not data:
            break

        page += 1
        for record in data:
            body_temperature = record["vitals"]["bodyTemperature"]
            total_temps += body_temperature
            total_records += 1

            if total_records == 0:
                return "0"

    average_temp = round(total_temps / total_records, 1)
    #print(userId, total_temps, total_records)
    return str(average_temp)

def main():
    userId = 1
    print(getAverageTemperatureForUser(userId))

if __name__ == "__main__":
    main()
