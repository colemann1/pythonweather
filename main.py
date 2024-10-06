import geocoder
import json
import requests
import socket
import sys

# Get local user IP address and use this for location information
ip = geocoder.ip('me')
geolocation = ip.latlng # coordinates - latitude and longitude - REMOVE WHITE SPACES - Used to format URL for API request

# Clean geolocation information of whitespace, brackets
geolocation = str(geolocation)
geolocation = geolocation.lstrip("[")
geolocation = geolocation.rstrip("]")
geolocation = geolocation.replace(" ", "")

locationcity = ip.city
locationstate = ip.state

APIString = 'https://api.weather.gov/points/' + geolocation

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
    pass

# Get weekly weather report
def get_weekly_report():
    pass

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