import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(".env")  # loads the environment file
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")  # alpha advantage api key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")    # news api key
account_sid = os.getenv("ACCOUNT_SID")      # account sid for twilio
auth_token = os.getenv("AUTH_TOKEN")        # auth token for twilio
up_down = ""

# Step 1: Using https://www.alphavantage.co
# If  the stock price increase/decreases by 5% between yesterday and the day before yesterday then send alert.

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()

stock_data = response.json()

print(stock_data['Time Series (Daily)'])

stock_daily = [value for (key, value) in stock_data['Time Series (Daily)'].items()]  # taps into the daily stock prices
# for a particular stock and it returns a list of dictionaries

print(stock_daily)
yesterday_stock = float(stock_daily[0]['4. close'])  # takes in the closing price for the stock
day_before_stock = float(stock_daily[1]['4. close'])  # takes in the closing price for the stock

percent_difference = int(abs(((yesterday_stock - day_before_stock) / yesterday_stock) * 100))

if percent_difference > 5:
    news_parameters = {
        "q": "tesla",
        "language": "en",
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    # Step 2: Using https://newsapi.org
    # We get the first 3 news pieces for the COMPANY_NAME.
    response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news_data = response.json()
    recent_articles = news_data['articles'][0:3]  # list made of the three latest new articles about the stock

    # Step 3: Using https://www.twilio.com
    # We send a separate message with the percentage change and each article's title and description

    client = Client(account_sid, auth_token)  # creates a Twilio client
    if yesterday_stock - day_before_stock > 0:  # depending on whether the difference is positive or negative
        up_down = "🔺"
    else:
        up_down = "🔻"
    for article in recent_articles:
        message = client.messages \
            .create(
            body=f"{STOCK}: {up_down}{percent_difference}% \n"
                 f"Headline: {article['title']} \n"
                 f"Brief: {article['description']}",
            from_='+******',  # here is a Twilio phone number
            to='+********'  # the phone number to which the message is to be sent
        )
        print(message.status)
