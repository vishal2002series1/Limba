import requests
import json
from datetime import date, timedelta
import logging
import os

logger = logging.getLogger(__name__)

POLYGON_MARKET_DATA_API_ENDPOINT = os.getenv("ZZ_POLYGON_MARKET_DATA_API_ENDPOINT")
POLYGON_MARKET_DATA_API_KEY = os.getenv("ZZ_POLYGON_MARKET_DATA_API_KEY")

def most_recent_weekday():
    logger.info('Getting most recent weekday date')
    today = date.today()
    # If today is Monday, go back to the previous Friday
    if today.weekday() == 0:
        return today - timedelta(days=3)
    # If today is Sunday, go back to the previous Friday
    elif today.weekday() == 6:
        return today - timedelta(days=2)
    # Otherwise, just go back one day
    else:
        return today - timedelta(days=1)

def fetch_aggregate_bars(stock_ticker, from_date, to_date):
    logger.info('Inside the fetch_aggregate_bars funtion')
    url = f"{POLYGON_MARKET_DATA_API_ENDPOINT}/v2/aggs/ticker/{stock_ticker}/range/1/day/{from_date}/{to_date}?apiKey={POLYGON_MARKET_DATA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        logger.info('fetch_aggregate_bars function failed')
        return f"Failed to fetch data: {response.content}"

def fetch_financial_data(stock_ticker):
    logger.info('Inside the fetch_aggregate_bars funtion')
    try:
        url = f"{POLYGON_MARKET_DATA_API_ENDPOINT}/vX/reference/financials?ticker={stock_ticker}&apiKey={POLYGON_MARKET_DATA_API_KEY}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.info('fetch_financial_data function failed '+str(e))

def formatNum(value):
    num = value
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    result = round(value / (1000**magnitude),2)
    return '${}{}'.format(result, ['', ' K', ' M', ' B', ' T'][magnitude])

def fetch_financial_metrics(stock_ticker):
    financial_metrics={}
    try:
        if stock_ticker=='NA':
            financial_metrics = {
                'stock_price': 'N/A',
                'sales': 'N/A',
                'net_income': 'N/A',
                'EPS': 'N/A',
                'net_profit_margin': 'N/A'
            }
            return financial_metrics
        else:
            most_recent_date = most_recent_weekday()
            from_date = to_date = most_recent_date.strftime('%Y-%m-%d')

            aggregate_data = fetch_aggregate_bars(stock_ticker, from_date, to_date)
            last_close = aggregate_data.get('results', [{}])[-1].get('c', "N/A")

            data = fetch_financial_data(stock_ticker)

            # Fetch the most recent financial record (here I assume it's the second in the list)
            most_recent_record = data.get('results', [{}])[1]
            financials = most_recent_record.get('financials', {})
            income_statement = financials.get('income_statement', {})

            # Extract the necessary financial metrics
            revenue = income_statement.get('revenues', {}).get('value', "N/A")
            net_income = income_statement.get('net_income_loss', {}).get('value', "N/A")
            eps = income_statement.get('diluted_earnings_per_share', {}).get('value', "N/A")

            # Calculate Net Profit Margin
            try:
                net_profit_margin = (float(net_income) / float(revenue)) * 100
            except (ValueError, ZeroDivisionError):
                net_profit_margin = "N/A"

            financial_metrics = {
                'stock_price': formatNum(last_close),
                'sales': formatNum(revenue),
                'net_income': formatNum(net_income),
                'EPS': eps,
                'net_profit_margin': "{:.2f}".format(net_profit_margin)+"%"
            }

            return financial_metrics
    except Exception as e:
        logger.info('Market data api call failed '+str(e))
        return financial_metrics