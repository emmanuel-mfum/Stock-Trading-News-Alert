# Stock-Trading-News-Alert
Python program that sends an SMS alert to the user about stock price.

We first use the Alpha Advantage API in order to get data/information about a stock.
https://www.alphavantage.co

This program is hardcoded for the Tesla stock, but the user is free to change to whatever is the acronym of the stock he is
interesred in on the stock exchange.

I had to make an accounr with Alpha Advantage and obtain the necessary credential in order to make an API request and obtain
data about the Tesla stock.

The data goes across the last 100 day of stock prices and records for every day the highest value of the day, the lowest value of the day,
as well as the opening and closing prices of the stock for a day.

In the case of this project I use and compare closing prices for the Tesla stock.

So, we generate a list of dictionaries containing the entries of stock prices for the last 100 days.
Then, we can tap into the stock price of yesterday at index 0 and the day before yesterday at index 1.
Each indices has the four types of prices I mentionned earlier and we can tap into the closing price of the stock with the key '4. close'.

Once we have two prices we find the percent difference between them. If the percent difference found is greater than 5% we trigger an alert,
which will send an SMS to the user alerting him on his mobile phone that the stock price has either risen or fallen by the percent difference found as
well as three news atricles related to the current stock.

In such case, we need to make a call to another API, the News API (https://newsapi.org) and extract from the response we get the three recent articles 
about the current stock.

Then, we need to call the Twilio API (https://www.twilio.com) in order to send an SMS to the user's phone. We check if the percent difference was positive or negative
in order to send the appropriate emoji to the user (Up or Down) and we send 3 custom text messages using the news data we got earlier as well as the percent difference.
The goal is to inform the user about a rise or fall in stock price and to provide some news pertaining to the stock about why such difference has occurred.
