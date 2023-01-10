import pandas as pd

def get_h4(ticker_data):
    df = ticker_data
    #print(df)
    df_split = df
    df_split.reset_index()

    b1 = df.iloc[:4]
    b2 = df.iloc[4:7]
    b3 = df.iloc[7:11]
    b4 = df.iloc[11:14]
    #print(b1)
    #print(b2)
    #print(b3)
    #print(b4)

    h4 = pd.DataFrame(data=None, columns=df.columns, index=df.index)
    h4 = h4.reset_index()
    h4.drop(h4.index,inplace=True)
    #print(h4)
    last_idx = len(b1.index) - 1
    h4.loc[len(h4.index)] = [b1.index[0],b1.iloc[0]['Open'],b1['High'].max(),b1['Low'].min(),b1.iloc[last_idx]['Close'],b1['Volume'].sum()]
    last_idx = len(b2.index) - 1
    h4.loc[len(h4.index)] = [b2.index[0],b2.iloc[0]['Open'],b2['High'].max(),b2['Low'].min(),b2.iloc[last_idx]['Close'],b2['Volume'].sum()]
    last_idx = len(b3.index) - 1
    h4.loc[len(h4.index)] = [b3.index[0],b3.iloc[0]['Open'],b3['High'].max(),b3['Low'].min(),b3.iloc[last_idx]['Close'],b3['Volume'].sum()]
    last_idx = len(b4.index) - 1
    h4.loc[len(h4.index)] = [b4.index[0],b4.iloc[0]['Open'],b4['High'].max(),b4['Low'].min(),b4.iloc[last_idx]['Close'],b4['Volume'].sum()]
    h4.set_index("Datetime", inplace = True)
    #print(h4)
    return h4