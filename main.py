import geocoder
import json
import requests
import socket
import sys

# Get local user IP address, use this for location information (latlong)
geo = geocoder.ip('me')
geolocation = geo.latlng

# Clean geolocation information of whitespace, brackets
geolocation = str(geolocation)
geolocation = geolocation.lstrip("[")
geolocation = geolocation.rstrip("]")
geolocation = geolocation.replace(" ", "")

locationcity = geo.city
locationstate = geo.state

APIString = 'https://api.weather.gov/points/' + geolocation

response = requests.get(APIString)

print(f"\nCurrent Location: ", locationcity, ", ", locationstate, "\n")
print(f"\nGeolocation: ", geolocation, "\n\n")

# Creating menu system
def display_menu(menu):
    for k, function in menu.items():
        print(k, function.__name__)


# Operation for ending session
def done():
    print("Goodbye")
    sys.exit()


# Get daily (next 24 hours) weather report
def get_daily_report():
    if response.status_code == 200:
        data = response.json()

    # Extract forecast URL from the response
    hourly_forecast_url = data['properties']['forecastHourly']
    
    print(f"Hourly forecast URL: {hourly_forecast_url}")
    
    # Make a request to the hourly forecast URL
    hourly_forecast_response = requests.get(hourly_forecast_url)
    
    if hourly_forecast_response.status_code == 200:
        hourly_forecast_data = hourly_forecast_response.json()
        
        # Print out the forecast
        print("\nHourly Weather Forecast:\n")
        for period in hourly_forecast_data['properties']['periods'][:25]: # Limit total output to 24 entries (representing 24 hours from the request time)
            print(f"{period['startTime']}: {period['temperature']}°F, {period['shortForecast']}, {period['windSpeed']}\n")
    else:
        print("Failed to retrieve hourly forecast data.")


# Get weekly weather report
def get_weekly_report():
    if response.status_code == 200:
        data = response.json()

    # Extract forecast URL from the response
    forecast_url = data['properties']['forecast']
    
    print(f"Forecast URL: {forecast_url}")
    
    # Make a request to the 'forecast' URL
    forecast_response = requests.get(forecast_url)
    
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        
        # Print out the forecast
        print("\nWeather forecast:\n")
        for period in forecast_data['properties']['periods']:
            print(f"{period['name']}: {period['detailedForecast']}\n")
    else:
        print("Failed to retrieve forecast data.")


# View current alerts
def get_current_alerts():
    pass


######


# Creates a menu dictionary where the key is a number and the value is a function name
def main():
    functions_names = [get_daily_report, get_weekly_report, get_current_alerts, done]
    menu_items = dict(enumerate(functions_names, start=1))

    while True:
        display_menu(menu_items)
        selection = int(input("Please enter your selection: "))
        selected_value = menu_items[selection]  # Get the function names
        selected_value()


if __name__ == "__main__":
    main()