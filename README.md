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
{
    "name": "YourName",
    "last_name": "YourLastName",
    "email": "yourEmail@something.com",
    "password": "TestPassword",
    "password2": "TestPassword"
}
```
