import yfinance as yf


def get_stock_info(stock_name): return yf.Ticker(stock_name).info # return the stock info


# Returns the current stock price of stock_name
def get_stock_price_current(stock_name):
    info = get_stock_info(stock_name)
    price = info['currentPrice']
    currency = ' ' + str(info['financialCurrency']) # the ' ' is for the message be looking later afterwards
    return (str(price) + currency)


# Returns the [stock price today, stock price a month ago, stock price change between these dates]
def get_stock_price_monthly_change(stock_name, month_ago_date):
    stock_current_price = get_stock_price_current(stock_name)
    currency = ' ' + stock_current_price[-3:] # slicing out the 3 last letters as it is the currency
    # getting the current (today's) price of the stock
    current_price = float(get_stock_price_current(stock_name)[:-3])
    # get the price of the stock last month (there is some code from pandas lib)
    last_month_price = float(round(yf.download(stock_name, month_ago_date)['Adj Close'].head(1)[0], 2))
    # calculate the percentage change between the dates
    change = round((current_price - last_month_price) / last_month_price * 100, 2)  

    return [str(current_price) + currency, str(last_month_price) + currency, change]


# returns buy/sell, etc.. based on the stock (analysts' opinions)
def get_stock_analysis(stock_name):
    info = get_stock_info(stock_name)
    return info['recommendationKey']


# returns a list of tuples which contains:
# 3 links and titles of relevant news about the stock_name (via yahoo finance - the API I am using)
def get_stock_news(stock_name):
    stock_ticker = yf.Ticker(stock_name)
    num_of_news_to_output = 3 # this is the number I chose :)    
    news = stock_ticker.news # returns news data about the stock on yahoo finance

    links_and_titles = list()
    for i in range (min(num_of_news_to_output, len(news))):
        # extracting links and titles from the news response
        link = news[i]['link']
        title = news[i]['title']

        links_and_titles.append(tuple((title,link)))

    return links_and_titles        