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

    soup = BeautifulSoup(requests.get('https://activtrades.com.br/go/suporte/base-conhecimento/margens-de-acoes/?target=print').content, "html.parser")
    
    #DE-PARA DE CODIGOS DE AÇÔES - USADO TBM PARA REMOVER AÇÔES QUE NÃO EXISTEM MAIS
    yf_x_tv=[['BFB','BF.B','BF-B'],
             ['UBNT','UI','UI'],
             ['LUL','LULU','LULU'],
             ['DISCK','',''],
             ['ANTM','',''],
             ['HFC','',''],
             ['VIAC','',''],
             ['PFPT','',''], #Proofpoint Inc - EMPRESA PRIVADA
             ['XLNX','',''], #Xilinx Inc - EMPRESA PRIVADA
             ['FB','META','META'], #Facebook -> META
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

    #OPçÂO DO PANDAS PARA EXIBIR TODAS AS LINHAS QUANDO EXECUTAR A FUNçÂO PRINT
    #pd.set_option('display.max_rows',None)

    #LOCALIZA A TABELA DENTRO DO CODIGO HTML QUE CONTÉM OS DADOS
    new_york = soup.find("table",attrs={'id':'tablepress-12'})
      
    df = pd.read_html(str(new_york))[0]

    #CONVERTE AS COLUNAS DE OBJECT PARA STRING
    df['Classe']   = df['Classe'].astype('string', errors = 'raise')
    df['Ativo']    = df['Ativo'].astype('string', errors = 'raise')
    
    # FILTRA AS LINHAS QUE SÃO DE NEW YORK
    activ_list = df[df['Classe'] == 'New York'].copy()
    
    #REMOVE % DAS LINHAS QUE TÊM E DIVIDE POR 100
    activ_list.loc[activ_list['Margem 1'].astype(str).str.contains('%'),'Margem 1'] = activ_list['Margem 1'].str.rstrip('%').astype('float')/100
    #print(activ_list)
    
    #REMOVE O SUFIXO ".US" DOS CODIGOS DAS AÇÔES
    activ_list['Ativo'] = activ_list['Ativo'].str.removesuffix('.US')

    #FILTRA OS REGISTROS ONDE A COLUNA MARGEM 1 FOR MENOR QUE O VALOR DEFINIDO (DEFAULT = 0.20)
    activ_list_SST = activ_list[activ_list['Margem 1'].astype('float') <= percentage_holds] 
    #print(activ_list_SST)

    for index, row in activ_list_SST.iterrows():
        #VERIFICA SE EXISTE REGISTRO NA TABELA DE DE-PARA (VER ACIMA)
        tv_code = replace_stock_code[replace_stock_code['Activtrades'] == row['Ativo']]
        if len(tv_code == 1): # SE ENCONTROU REGISTRO
            if (tv_code.iloc[0]['YahooFinance'] != ''): # SE EXISTE UM CODIGO DO YAHOO FINANCE CADASTRADO, ALTERA O CODIGO DA AÇÃO
                activ_list_SST.loc[index,'Ativo'] = tv_code.iloc[0]['YahooFinance']
            else: # SE NÃO EXISTE UM CODIGO, MOVE VAZIO
               activ_list_SST.loc[index,'Ativo'] = ''

    #CONVERTE OS VALORES DA COLUNA "ATIVO" PARA LISTA, REMOVENDO OS REGISTROS EM BRANCO
    lista_saida = activ_list_SST[activ_list_SST.Ativo != ''].Ativo.tolist()
    #ORDENA A LISTA
    lista_saida.sort()
    #RETORNA PARA A SAÍDA DA FUNÇÂO
    return lista_saida

########################## TESTE ########################################
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#companies_list = get_activtrades_stocks(margem=0.20)
#print((companies_list)) # FORMATO DE LISTA
#print(len(companies_list))
#saida = ','.join(map(str,companies_list))
#print(saida) # FORMATO DE STRING