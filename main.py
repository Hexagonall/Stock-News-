import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

MY_API = " Your twilo API "
account_sid = "your twilio SID"
auth_token = "your twilio TOKEN"

PARAMETER = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": MY_API
}

MY_NEWS_API = "alphavantage API"

NEWS_PARAMETER = {
    "q": COMPANY_NAME,
    "from":"2023-01-18",
    "sortBy": "popularity",
    "apiKey": MY_NEWS_API
}

# extract the yesterday and yesterday before price and find percentage.
with requests.get(STOCK_ENDPOINT, params=PARAMETER) as response:
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]

    data_list = [value for (key,value) in data.items()]
    # yerterday data     
    yesterday_data = data_list[0]
    yesterday_closing_price = float(yesterday_data["4. close"])
    # day before data      
    day_before = data_list[1]
    day_before_closing_price = float(day_before["4. close"])

    difference = yesterday_closing_price - day_before_closing_price
    up_down = None
    if difference>0:
        up_down = "🔺"
    else:
        up_down = "🔻"
    # percentage    
    percentage = round((difference/yesterday_closing_price)*100)

    # if percentage >1 ,find reasons
    if abs(percentage)>1:
        print(percentage)
        with requests.get(
                "https://newsapi.org/v2/everything?q=Tesla Inc&from=2023-01-18&sortBy=popularity&apiKey=9a2da226d1294298bfdaa057afc3fde6") as objects:
            objects.raise_for_status()
            shows_data = objects.json()["articles"]

            tree_articles = shows_data[:3]

           
            # Send message
            send_message_list = [f"{STOCK}:{up_down}{percentage}% \nHeadline:{a['title']}.\nBrief:{a['description']}" for a in tree_articles]
            print(send_message_list)
            for article in send_message_list:
                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                    body=article,
                    from_='+13393561927',
                    to='Your Phone Number'
                )




