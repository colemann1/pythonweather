## Python Weather Program

Program for retrieving weather information from https://api.weather.gov

Functions defined, working:
- Close program
- Daily "next 24 hour" report
- Weekly report
- Current alerts


## Requirements
- geocoder
- json
- requests
- socket
- sys

## Updates (as of 10/12/2024)
- Added alerts, search by state abbreviation (NC, CA, NY,)
    - Added user input checking
    - Uses 'try / except' for errors with retrieving information
- Added 'try / except' to menu system
- Removed comments no longer needed (debugging / todo)
- Updated variable names again for more consistent naming
- Updated whitespacing for more consistency and readability
- Improved output readability

- Updated README.md correctly this time

## Updates (as of 10/11/2024)
- Changed naming of variable 'ip' to 'geo' for more consistent naming
- Added weekly report
- Added daily (next 24 hours) report (due to similar code to weekly report)

## Known Issues (as of 10/12/2024)
- Precipitation chance not listed in hourly report