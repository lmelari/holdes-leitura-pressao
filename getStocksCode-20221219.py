from lxml import html
from bs4 import BeautifulSoup

import requests
import pandas as pd

def get_gsheets_rubens():
    # Ler dados do Google Sheets
    sheet_id = '1Xd6BNpm7aYmE5CwQYvyMQ_R5OxD0L8V8GNT6dF3i0Qg'
    sheet_name = '1651690612'
    data_companies = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_name}',index_col=0, header=None)
    #print(data_companies)
    companies_list = data_companies.index.values.tolist()
    return companies_list

def get_activtrades_stocks(margem = 0.20):
    pagina = requests.get('https://www.activtrades.com/en/shares-trading/shares-margins#section_1_2').text
    soup = BeautifulSoup(requests.get('https://www.activtrades.com/en/shares-trading/shares-margins#section_1_2').content, "html.parser")

    yf_x_tv=[['BFB','BF.B','BF-B'],
             ['UBNT','UI','UI'],
             ['LUL','LULU','LULU'],
             ['DISCK','',''],
             ['ANTM','',''],
             ['HFC','',''],
             ['VIAC','',''],
             ['CTXS','',''], #SEM DADOS EM 03/10/2022
             ['TWTR','',''], #SEM DADOS EM 31/10/2022
             ['BLL','BALL','BALL'], #Ball Corporation (BALL)
             ['JEC','J','J'],   #Jacobs Solutions Inc. (J)
             ['BRKB','BRK.B','BRK-B'], #Berkshire Hathaway Inc. (BRK-B)
             ['BKB','BK','BK'], #The Bank of New York Mellon Corporation (BK)
             ['COG','CTRA','CTRA'], #Coloterra Energy(CTRA)
             ['WLTW','WTW','WTW'] #Willis Towers Watson Public Limited Company (WTW)
            ]
    
    replace_stock_code = pd.DataFrame(yf_x_tv,columns=['Activtrades','TradingView','YahooFinance'])

    percentage_holds = margem

    #pd.set_option('display.max_rows',None)

    new_york = soup.find("table",attrs={'id':'newYork'})
    df = pd.read_html(str(new_york))[0]

    activ_list = df.drop(df.columns[[3,4]],axis=1)
    new_header = activ_list.iloc[0]
    activ_list = activ_list[1:]
    activ_list.columns = new_header

    #activ_list['Code'] = activ_list['Code'].str.rstrip(".US")
    activ_list['Code'] = activ_list['Code'].str.removesuffix('.US')

    activ_list.rename(columns = {'Margin 1(*)':'Margem'},inplace = True)

    activ_list.sort_values(by='Code',inplace=True)

    activ_list['Margem'] = activ_list['Margem'].str.rstrip('%').astype('float')/100.0

    activ_list_SST = activ_list[activ_list['Margem'] <= percentage_holds] 

    for index, row in activ_list_SST.iterrows():
        tv_code = replace_stock_code[replace_stock_code['Activtrades']==row['Code']]
        if len(tv_code == 1):
            if (tv_code.iloc[0]['YahooFinance'] != ''):
                activ_list_SST.loc[index,'Code'] = tv_code.iloc[0]['YahooFinance']
            else:
                activ_list_SST.loc[index,'Code'] = ''
    
    lista_saida = activ_list_SST[activ_list_SST.Code != ''].Code.tolist()
    lista_saida.sort()
    
    return lista_saida

    #print(len(lista_saida))
    #saida = ','.join(map(str,lista_saida))
    #saida = saida[1:]
    #print(saida)