# ECM1400 Flask Covid Dashboard

This is a Flask app that displays a dashboard of COVID-19-related data and news.

## Installation

Clone and extract the repository and run the command
```bash
pip3 -r requirements.txt
```
from the top directory to install the requirements for this app.

Then, navigate to the services folder and run
```bash
flask run
```
to start the server.

Then, in your browser, navigate to 127.0.0.1:5000 to run the frontend and view the dashboard.

## Usage

### Startup and during runtime

The left-hand widget titled "Scheduled updates" displays the stored scheduled update events, their intervals, whether they repeat, and whether they update the COVID data, the news listings, or both. To stop a scheduled update, click the "X" by its box in the list.

The central element displays various COVID data, provided by the UK's COVID API. To schedule a new update, use the form in the centre of the UI. The time field represents the number of hours and minutes between the firings of the particular update. E.g. 12:15 means "every 12 hours and 15 minutes" if the event is repeating, and "In 12 hours and 15 minutes" if it is not.

The file services/updates.csv is NOT to be modified by anything but the app itself! Modification of this file may lead to undefined and undesired behaviour.

### Configuration

TODO
Please use config.json to configure the program.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.