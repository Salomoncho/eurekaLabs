# Stock Market API Service
## How to install:
Clone the repo, create a virtual environment and activate it:
```angular2html
python3 -m venv YourEnvName
source YourEnvName/bin/activate
```

Install the requirements:
```angular2html
pip install -r requirements.txt
```
Note: If you are getting the following error instaling the ```psycopg2``` package:

run ```sudo apt-get install libpq-dev```

Run the tests (make sure you are in the root folder where manage.py is):
```angular2html
python3 manage.py test
```

Run the server:
```angular2html
python3 manage.py runserver
```
## Endpoints: 

### Register: /api/register/
Returns the message and the API_KEY or the error if it fails registering the user.

Make a POST request to ```http://127.0.0.1:8000/api/register/``` sending the following payload:

```angular2html
(Make sure the header 'Content-Type' = 'application/json')
{
    "name": "YourName",
    "last_name": "YourLastName",
    "email": "yourEmail@something.com",
    "password": "TestPassword",
    "password2": "TestPassword"
}
```

### Login: /api/login/
If you are already registered, but for some reason you don't have the API_KEY, you can use the login api to get it using
your credentials.

Returns the message and the API_KEY or the error if it fails login the user.

Make a POST request to ```http://127.0.0.1:8000/api/login/``` sending the following payload:

```angular2html
(Make sure the header 'Content-Type' = 'application/json')
{
    "email": "yourEmail@something.com",
    "password": "TestPassword"
}
```

### Stock Service: /api/stock-service/
Returns the daily stock information for the given symbol.

Make a POST request to ```http://127.0.0.1:8000/api/stock-service/``` sending the following payload:

IMPORTANT: You have to set the ALPHA_VANTAGE_API_KEY setting that will be used to request data from Alpha Vantage API.

```angular2html
(Make sure to include the API_KEY in the HTTP_X_API_KEY key and set 'Content-Type' = 'application/json' )

header = {
  'x-api-key': 'Must be the same api key as the STOCK_SERVICE_API_KEY setting (settings.py)',
  'Content-Type': 'application/json'
}

payload = {
    "stock_symbol": "META"
}

```

## About the Logs
If you run the tests you will see that in the root folder will be created a ```server_request_logs.log``` file.

It will log every API call protecting the sensitive data.
(It validates key names in the REQUEST_LOGGING_SENSITIVE_KEYS setting)

You can also set a list of app names to ignore when logging using the
```REQUEST_NO_LOGGING_APP_NAMES``` setting.