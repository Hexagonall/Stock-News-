import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

MY_API = " 9HVAUJXFB9RM2C7A"
account_sid = "ACcf455b5ac3d9f37f5ed7c2abb00ee400"
auth_token = "b4b385ba816636d0ace0e27d6b573a57"

PARAMETER = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": MY_API
}

MY_NEWS_API = "9a2da226d1294298bfdaa057afc3fde6"

NEWS_PARAMETER = {
    "q": COMPANY_NAME,
    "from":"2023-01-18",
    "sortBy": "popularity",
    "apiKey": MY_NEWS_API
}

with requests.get(STOCK_ENDPOINT, params=PARAMETER) as response:
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]

    data_list = [value for (key,value) in data.items()]

    yesterday_data = data_list[0]
    yesterday_closing_price = float(yesterday_data["4. close"])

    day_before = data_list[1]
    day_before_closing_price = float(day_before["4. close"])

    difference = yesterday_closing_price - day_before_closing_price
    up_down = None
    if difference>0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    percentage = round((difference/yesterday_closing_price)*100)

    if abs(percentage)>1:
        print(percentage)
        with requests.get(
                "https://newsapi.org/v2/everything?q=Tesla Inc&from=2023-01-18&sortBy=popularity&apiKey=9a2da226d1294298bfdaa057afc3fde6") as objects:
            objects.raise_for_status()
            shows_data = objects.json()["articles"]

            tree_articles = shows_data[:3]

            # print(tree_articles)

            send_message_list = [f"{STOCK}:{up_down}{percentage}% \nHeadline:{a['title']}.\nBrief:{a['description']}" for a in tree_articles]
            print(send_message_list)
            for article in send_message_list:
                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                    body=article,
                    from_='+13393561927',
                    to='+905452971956'
                )




