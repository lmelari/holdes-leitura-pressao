#------------ Bobliotecas
import yfinance as yf
import pandas as pd
from datetime import datetime

#------------ Funções personalizadas
import getStocksCode
import checkPressao
import h4

#----------------------------------------------------------
#--------------------- VARIAVEIS GLOBAIS ------------------
#----------------------------------------------------------
source         = 'ACTV'

periodo_menor   = '2d'
intervalo_menor = '60m'
#----------------------------------------------------------

start_time = datetime.now()

if source == 'ACTV':
    companies_list = getStocksCode.get_activtrades_stocks(margem=0.20)
elif source == 'RUBENS':
    companies_list = getStocksCode.get_gsheets_rubens()
else:
    print('ORIGEM DESCONHECIDA ou EM CONSTRUÇÃO')

lista_menor = pd.DataFrame(yf.download( companies_list,
                                        period=periodo_menor, 
                                        interval=intervalo_menor,
                                        group_by="ticker", 
                                        auto_adjust=True,
                                        rounding=True
                                        #progress=False
                                        #show_errors=False
                                    )
                            )   
stocks_rank_list = pd.DataFrame([], columns=['Ticker',
                                             'Valor Pressão',
                                             '% Pressão'
                                             ]
                                )

for company in companies_list:
    stock_data_menor = h4.get_h4(lista_menor[company])
    valor_pressao_menor, perc_pressao = checkPressao.pressao_menor(stock_data_menor)

    if valor_pressao_menor > 0.0:
        stocks_rank_list.loc[len(stocks_rank_list)] = [ company, #Ticker
                                                        valor_pressao_menor,
                                                        perc_pressao,#%Pressão
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
    print('Lista Pressão H4.........: ',saida)
    print('')
    stocks_rank_list.sort_values(by=['% Pressão'],ascending=False,inplace=True)
    print(stocks_rank_list)
else:
    print('------------------------------------------')
    print('DIA DE FOLGA!!!')
    print('------------------------------------------')