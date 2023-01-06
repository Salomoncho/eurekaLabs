# Stock Market API Service

Expose an API endpoint where I can POST my data and sign up for an API key that will be used later.

Expose an API endpoint where I can hit and get stock market information, as a security mechanism use the API key obtained previously in order to validate user and make sure that no authorized user will consume the service (use request header for that purpose).

Here are some examples of stock symbols

- Facebook (META)
- Apple (AAPL)
- Microsoft (MSFT)
- Google (GOOGL)
- Amazon (AMZN)

The system will make use of a web service called Alpha Vantage, this will provide stock market information.

Information that will be retrieved in the response of the service as json format will contain:

- Open price
- Higher price
- Lower price
- Variation between last 2 closing price values.

**Alpha Vantage API**

```
https://www.alphavantage.co/documentation/
API Key: X86NOH6II01P7R24
```

API call sample to get stock prices from Facebook:

`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=META&outputsize=compact&apikey=X86NOH6II01P7R24`

**Considerations:**

- API URL structure is up to you.
- Initial data for sign up: name, last name, email.
- Validation rules for signup data are up to you.
- Json structure is up to you.
- It will be a big plus if you deploy the services somewhere in the cloud (heroku, gcloud, aws, azure, etc). It's ok if you just do it locally.
- Use github (or other git repo).
- Programming language: Python.
- BONUS: If you can implement API throttling, that's a big one. Throttling rules are up to you (1 API call per second allowed or 10 API calls per minute, etc).
- Log every API call received, log format is up to you.
- Place a README.md file with instructions in the github repo so test can be performed and checked.
