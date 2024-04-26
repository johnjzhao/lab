import requests
import json

def getTemperature(name):
    # Create the URL with the provided city name
    url = f"https://jsonmock.hackerrank.com/api/weather?name={name}"

    try:
        # Perform an HTTP GET request to fetch weather information
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            # Deserialize the JSON response
            weatherData = json.loads(response.text)

            # Extract the temperature from the first weather record
            weather = weatherData['data'][0]['weather']
            temperature = int(weather.split(' ')[0])  # Extract integer part

            return temperature
        else:
            raise Exception(f"Failed to fetch weather data for {name}. Status code: {response.status_code}")
    except Exception as ex:
        # Handle any exceptions and return -1 indicating failure
        print(f"An error occurred: {ex}")
        return -1

name = input()
result = getTemperature(name)
print(result)
