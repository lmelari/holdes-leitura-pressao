# Get pricing data
import yfinance as yahooFinance
import pandas as pd

def get_ADR(stock_info):
    # Get the previous 6 months pricing data
    #ticker = yahooFinance.Ticker(Ticker).history(period='1y', interval="1d")[["High", "Low"]]
    ticker = stock_info
    # Calculate Daily Range for each period and normalize as pct change
    ticker['dr_pct'] = ticker.apply(lambda x: 100 * ((x["High"] / x["Low"]) - 1), axis=1)
    # Calculate the average daily range over a 120-period interval
    ticker["mod_adr"] = ticker['dr_pct'].rolling(window=120).mean()
    # View Result
    #print(ticker)

    df = pd.DataFrame(ticker)
    df = df.reset_index()
    df = df.drop(df[df.Date != '2022-07-01'].index)
    #print(df)
    for index, row in df.iterrows():
        ADR = row['mod_adr']

    return(ADR)