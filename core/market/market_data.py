
def get_stocks_data(stocks):
    stocks_data = []
    for stock in stocks:
        stocks_data.append(get_stock_data(stock))
    return stocks_data

def get_stock_data(stock):
    return []
