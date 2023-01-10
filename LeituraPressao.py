#------------ Bobliotecas
import yfinance as yf
import pandas as pd
from datetime import datetime

#------------ Funções personalizadas
import getStocksCode
import checkPressao
import ADR

#----------------------------------------------------------
#--------------------- VARIAVEIS GLOBAIS ------------------
#----------------------------------------------------------
source         = 'ACTV'

periodo_maior   = '2y'
intervalo_maior = '1wk'
periodo_menor   = '4d'
intervalo_menor = '1d'
#----------------------------------------------------------

start_time = datetime.now()

if source == 'ACTV':
    companies_list = getStocksCode.get_activtrades_stocks(margem=0.20)
elif source == 'RUBENS':
    companies_list = getStocksCode.get_gsheets_rubens()
else:
    print('ORIGEM DESCONHECIDA ou EM CONSTRUÇÃO')

lista_menor = yf.download( companies_list,
                             period=periodo_menor, 
                             interval=intervalo_menor,
                             group_by="ticker",
                             auto_adjust=True,
                             rounding=True
                             #progress=False
                             #show_errors=False
                            )
lista_maior = yf.download( companies_list,
                             period=periodo_maior, 
                             interval=intervalo_maior,
                             group_by="ticker",
                             auto_adjust=True,
                             rounding=True
                             #progress=False
                            )

lista_adr = yf.download( companies_list,
                             period="1y", 
                             interval="1d",
                             group_by="ticker",
                             auto_adjust=True,
                             rounding=True
                             #progress=False
                            )


stocks_rank_list = pd.DataFrame([], columns=['Ticker',
                                             'Valor Pressão',
                                             '% Pressão',
                                             'ADR',
                                             'Pressão / ADR',
                                             'Pressão Tempo Maior Aberta',
                                             'YF Check'
                                             ]
                                )

for company in companies_list:
    stock_data_menor = lista_menor[company]
    stock_data_maior = lista_maior[company]
    stock_data_maior = stock_data_maior[stock_data_maior['Open'].notna()]
    valor_pressao_menor, perc_pressao = checkPressao.pressao_menor(stock_data_menor)

    if valor_pressao_menor > 0.0:
        #adr = ADR.get_ADR(lista_adr[company])
        pressao_aberta_maior = False
        pressao_aberta_maior = checkPressao.pressao_maior(stock_data_maior,print_log=False)
        adr = 1.0
        stocks_rank_list.loc[len(stocks_rank_list)] = [ company, #Ticker
                                                        valor_pressao_menor,
                                                        perc_pressao,#%Pressão
                                                        adr,#ADR
                                                        round(perc_pressao / adr,2),#Pressão / ADR
                                                        pressao_aberta_maior,
                                                        False
                                                    ]  


#---------------------- LOG DE PROCESSAMENTO
end_time = datetime.now()
proc_time = end_time - start_time
print('---------- LOG DE PROCESSAMENTO ----------')
print('Tempo de Processamento: ', str(proc_time))
print('------------------------------------------')
if (len(stocks_rank_list)>0):
    lista_pressao = stocks_rank_list['Ticker']
    saida = ''
    saida = ','.join(map(str,lista_pressao))
    print('Pressão Diário.........: ',saida)
    print('')
    com_pressao_list = stocks_rank_list.loc[(stocks_rank_list['Pressão Tempo Maior Aberta'] == True)]['Ticker']
    saida = ''
    saida = ','.join(map(str,com_pressao_list))
    print('Pressão Aberta Semanal.: ',saida)
    print('')
    print('------- Sem Pressão Aberta Semanal -------')
    sem_pressao_list = stocks_rank_list.loc[(stocks_rank_list['Pressão Tempo Maior Aberta'] == False)][['Ticker','% Pressão']]
    sem_pressao_list.sort_values(by=['% Pressão'],ascending=False,inplace=True)
    print(sem_pressao_list)
    print('------------------------------------------')
else:
    print('------------------------------------------')
    print('DIA DE FOLGA!!!')
    print('------------------------------------------')