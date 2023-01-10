from datetime import datetime
from this import d
import yfinance as yf
import pandas as pd
import pytz

import LeituraPressaoBeta

#df_hist = yf.Ticker('JNJ').history(period="2d", interval="1h",auto_adjust=True,back_adjust=True,rounding=True)
#print(df_hist)

# Ler dados do Google Sheets
sheet_id = '1Xd6BNpm7aYmE5CwQYvyMQ_R5OxD0L8V8GNT6dF3i0Qg'
sheet_name = '1651690612'
data_companies = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_name}',index_col=0, header=None)
#print(data_companies)
companies = data_companies.index.values.tolist()

#cur_date = datetime.now().strftime('%d/%m/%Y')
#print("------------- DOWNLOAD UNITARIO -------------")
#start_time = datetime.now()

#for company in companies:
#    yf_download = yf.download(company,period="4d", interval="1d",group_by="ticker",auto_adjust=True,rounding=True,progress=False)
#    yf_download_S = yf.download(company,period="2y", interval="1wk",group_by="ticker",auto_adjust=True,rounding=True,progress=False)
#end_time = datetime.now()
#proc_time = (end_time - start_time)

#print("UNITARIO INICIO : ", str(start_time.strftime('%H:%M:%S')))
#print("UNITARIO FIM    : ", str(end_time.strftime('%H:%M:%S')))
#print("UNITARIO DURAÇÃO: ", str(proc_time))

#pd.set_option('display.max_rows',None)

#print("------------- DOWNLOAD EM MASSA -------------")
#start_time = datetime.now()

#yf_download = yf.download(companies,period="4d", interval="1d",group_by="ticker",auto_adjust=True,rounding=True,progress=False)
#yf_download_S = yf.download(companies,period="2y", interval="1wk",group_by="ticker",auto_adjust=True,rounding=True,progress=False)
#yf_download_S= yf_download_S[yf_download_S['Open'].notna()]
#print(yf_download_S)
#end_time = datetime.now()
#proc_time = (end_time - start_time)

#print("UNITARIO INICIO : ", str(start_time.strftime('%H:%M:%S')))
#print("UNITARIO FIM    : ", str(end_time.strftime('%H:%M:%S')))
#print("UNITARIO DURAÇÃO: ", str(proc_time))

#yf_download['BR_time'] = yf_download.index.tz_convert('America/Sao_Paulo')
#print(yf_download)

#df = yf_download["CPB"]
#print(df)

#timezone_BR = pytz.timezone('America/Sao_Paulo')

#for index,row in df.iterrows():
#    current_time_in_BR = index.tz_convert('America/Sao_Paulo')
#    cur_date = current_time_in_BR.strftime('%d/%m/%Y')
#    cur_time = current_time_in_BR.strftime('%H:%M')
#    print(str(cur_date)," - ",str(cur_time))

# tickers = ['CSTX','IBM']

# stock_info = yf.Ticker('CSTX').info
# print(stock_info)
# market_price = stock_info['regularMarketPrice']
# print(market_price)
# if (market_price  is None):
#      print("Fora")
# else:
#      print("OK")


df = pd.DataFrame(yf.download(['CME','PDD'],
                                period='2d',
                                interval="60m",
                                group_by='ticker',
                                rounding=True,
                                progress=False,
                                auto_adjust=True
                           )
                )
print(df)
df_split = df
df_split.reset_index()

df = df['PDD']

b1 = df.iloc[:4]
b2 = df.iloc[4:7]
b3 = df.iloc[7:11]
b4 = df.iloc[11:14]
print(b1)
print(b2)
print(b3)
print(b4)

h4 = pd.DataFrame(data=None, columns=df.columns, index=df.index)
h4 = h4.reset_index()
h4.drop(h4.index,inplace=True)
print(h4)
last_idx = len(b1.index) - 1
h4.loc[len(h4.index)] = [b1.index[0],b1.iloc[0]['Open'],b1['High'].max(),b1['Low'].min(),b1.iloc[last_idx]['Close'],b1['Volume'].sum()]
last_idx = len(b2.index) - 1
h4.loc[len(h4.index)] = [b2.index[0],b2.iloc[0]['Open'],b2['High'].max(),b2['Low'].min(),b2.iloc[last_idx]['Close'],b2['Volume'].sum()]
last_idx = len(b3.index) - 1
h4.loc[len(h4.index)] = [b3.index[0],b3.iloc[0]['Open'],b3['High'].max(),b3['Low'].min(),b3.iloc[last_idx]['Close'],b3['Volume'].sum()]
last_idx = len(b4.index) - 1
h4.loc[len(h4.index)] = [b4.index[0],b4.iloc[0]['Open'],b4['High'].max(),b4['Low'].min(),b4.iloc[last_idx]['Close'],b4['Volume'].sum()]
h4.set_index("Datetime", inplace = True)
print(h4)
# start_time = datetime.now()
# print('DIARIO')
# print(LeituraPressaoBeta.leitura_pressao('ACTV','DIARIO',True))
# print('H1')
# print(LeituraPressaoBeta.leitura_pressao('ACTV','H1',False))
# print('H4')
# print(LeituraPressaoBeta.leitura_pressao('ACTV','H4',True))
#---------------------- LOG DE PROCESSAMENTO
# end_time = datetime.now()
# proc_time = end_time - start_time
# print(proc_time)
# print('---------- LOG DE PROCESSAMENTO ----------')
# print('Tempo de Processamento: ', str(proc_time))
# print('------------------------------------------')
# if (len(stocks_rank_list)>0):
#     lista_pressao = stocks_rank_list['Ticker']
#     saida = ''
#     saida = ','.join(map(str,lista_pressao))
#     print('Pressão Diário.........: ',saida)
#     print('')
#     com_pressao_list = stocks_rank_list.loc[(stocks_rank_list['Pressão Tempo Maior Aberta'] == True)]['Ticker']
#     saida = ''
#     saida = ','.join(map(str,com_pressao_list))
#     print('Pressão Aberta Semanal.: ',saida)
#     print('')
#     print('------- Sem Pressão Aberta Semanal -------')
#     sem_pressao_list = stocks_rank_list.loc[(stocks_rank_list['Pressão Tempo Maior Aberta'] == False)][['Ticker','% Pressão']]
#     sem_pressao_list.sort_values(by=['% Pressão'],ascending=False,inplace=True)
#     print(sem_pressao_list)
#     print('------------------------------------------')
# else:
#     print('------------------------------------------')
#     print('DIA DE FOLGA!!!')
#     print('------------------------------------------')