import geocoder
import json
import requests
import socket
import sys

# Get local user IP address and use this for location information
geo = geocoder.ip('me')
geolocation = geo.latlng

# Clean geolocation information of whitespace, brackets
geolocation = str(geolocation)
geolocation = geolocation.lstrip("[")
geolocation = geolocation.rstrip("]")
geolocation = geolocation.replace(" ", "")

locationcity = geo.city
locationstate = geo.state

points_url = 'https://api.weather.gov/points/' + geolocation

response = requests.get(points_url)

print(f"\nCurrent Location: ", locationcity, ", ", locationstate, "\n")
print(f"\nGeolocation: ", geolocation, "\n\n")


# Creating menu system
def display_menu(menu):
    for k, function in menu.items():
        print(k, function.__name__)


# Operation for ending session
def done():
    print("\nGoodbye\n")
    sys.exit()


# Get daily (next 24 hours) weather report
def get_daily_report():
    if response.status_code == 200:
        data = response.json()

    # Extract forecast URL from the response
    hourly_forecast_url = data['properties']['forecastHourly']
    
    print(f"Hourly forecast URL: {hourly_forecast_url}")
    
    # Make a request to the forecast URL
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

    try:
        # Extract forecast URL from the response
        forecast_url = data['properties']['forecast']
        
        print(f"Forecast URL: {forecast_url}")
        
        # Make a request to the 'forecast' URL - https://api.weather.gov/gridpoints/TOP/
        forecast_response = requests.get(forecast_url)
        
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            
            # Print out the forecast
            print("\nWeather forecast:\n")
            for period in forecast_data['properties']['periods']:
                print(f"{period['name']}: {period['detailedForecast']}\n")
        else:
            print("Failed to retrieve forecast data.")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"\nHTTP error occurred: {http_err}\n")
    except requests.exceptions.ConnectionError:
        print("\nError: Unable to connect to the weather service.\n")
    except requests.exceptions.Timeout:
        print("\nError: The request timed out.\n")
    except requests.exceptions.RequestException as err:
        print(f"\nAn error occurred: {err}\n")
    except KeyError as key_err:
        print(f"\nMissing key in the response: {key_err}\n")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}\n")


# View current alerts
def get_current_alerts():
    stateinput = input("Please enter a US 2-letter state abbreviation: ")
    stateinput = stateinput.upper() # Put into uppercase for URL, must be in upprcase for URL to work

    alert_url = 'https://api.weather.gov/alerts/active?area=' + stateinput # Generate URL for API - different address to above

    try:
        alert_response = requests.get(alert_url, timeout=15) # Timeout for response

        alert_response.raise_for_status() # Exception for non-200 status

        alert_data = alert_response.json()

        # Check for new alerts, if greater than 0, save in variables to print
        if 'features' in alert_data and len(alert_data['features']) > 0:
            for alert in alert_data['features']:
                alert_title = alert['properties']['headline']
                alert_description = alert['properties']['description']
                alert_urgency = alert['properties']['urgency']
                alert_severity = alert['properties']['severity']
                alert_area = alert['properties']['areaDesc']
                
                print("\n\n><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><")
                print(f"\nCurrent weather alerts for {stateinput}:")
                print(f"\nAlert: {alert_title}")
                print(f"\nDescription: {alert_description}")
                print(f"\nUrgency: {alert_urgency}")
                print(f"\nSeverity: {alert_severity}")
                print(f"\nArea: {alert_area}")
                print("\n><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><\n\n")
        else:
            print("\n\nNo active weather alerts.\n\n") # No alerts for state

    except requests.exceptions.HTTPError as http_err:
        print(f"\nHTTP error occurred: {http_err}\n")
    except requests.exceptions.ConnectionError:
        print("\nError: Unable to connect to the weather service.\n")
    except requests.exceptions.Timeout:
        print("\nError: The request timed out.\n")
    except requests.exceptions.RequestException as err:
        print(f"\nAn error occurred: {err}\n")
    except KeyError as key_err:
        print(f"\nMissing key in the response: {key_err}\n")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}\n")


# Creates a menu dictionary where the key is a number and the value is a function name
def main():
    functions_names = [get_daily_report, get_weekly_report, get_current_alerts, done]
    menu_items = dict(enumerate(functions_names, start=1))

    while True:
        display_menu(menu_items)
        try:
            selection = int(input("Please enter your selection: "))
            selected_value = menu_items.get(selection)

            if selected_value is not None:
                selected_value()  # Call the selected function
            else:
                print("Invalid selection, please try again.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()