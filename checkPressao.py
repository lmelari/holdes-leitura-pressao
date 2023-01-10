from datetime import datetime

def pressao_menor(stock_info):
    df = stock_info

    df = df.reset_index() # make sure indexes pair with number of rows
    df.sort_values(by='Date', inplace=True, ascending=True) # sort instruction
    #df['Diff']     = df['Adj Close'].diff()
    df['Diff']     = df['Close'].diff()
    #df['Bar_diff'] = df['Adj Close'] - df['Open']
    df['Bar_diff'] = df['Close'] - df['Open']
    df['Diff']     = df['Diff'].fillna(0)
    df['Bar_diff'] = df['Bar_diff'].fillna(0)

    seq_pressao = 0
    delta_pressao = 0.0
    abertura_pressao = 0.0
    fechamento_pressao = 0.0
    valor_pressao = 0.0
    perc_pressao = 0.0

    for index, row in df.iterrows():
        #print(str(row['Date']) + ' ' + str(row['Bar_diff']) + ' ' + str(row['Diff']))
        if (row['Bar_diff'] > 0):
            if (row['Diff'] > 0):
                seq_pressao +=1
                delta_pressao += row['Bar_diff']
                #fechamento_pressao = row['Adj Close']
                fechamento_pressao = row['Close']
                if abertura_pressao == 0.0:
                    abertura_pressao = row['Open']
            else:
                seq_pressao = 1
                delta_pressao = row['Bar_diff']
                abertura_pressao = row['Open']
        else:
            seq_pressao = 0
            delta_pressao = 0
            abertura_pressao = 0.0
            fechamento_pressao = 0.0

    if (seq_pressao == 3):
        #adr = get_ADR(company)
        #print(company,end=" - ")
        #print('Valor Pressão: ' + str(round((fechamento_pressao - abertura_pressao),2)),end=" - ")
        #print('% Pressão: ' + str(round(((fechamento_pressao - abertura_pressao)/abertura_pressao)*100, 2)),end=" - ")
        #print('ADR: ' + str(round(adr,2)),end=' - ')
        #print('Pressão em NG: ' + str(round((((fechamento_pressao - abertura_pressao)/abertura_pressao)*100)/adr, 2)))
        #pressao.append(company)
        #pressaoS = pressaoSemanalV02.check_pressao_S(Ticker=company,print_log=False)
        #pressaoS_sem_adjust = pressaoSemanalV02.check_pressao_S(Ticker=company,print_log=False,auto_adjust=False)
        #if ( pressaoS == True & pressaoS_sem_adjust == True ):
        #    pressaoSemAberta.append(company)
        #    check_yfinance = 'OK'
        #elif( pressaoS == False & pressaoS_sem_adjust == False ):
        #    pressaoSemFechada.append(company)
        #    check_yfinance = 'OK'
        #else:
        #    pressaoSDivergencia.append(company)
        #    check_yfinance = 'NOK'

        valor_pressao = round((fechamento_pressao - abertura_pressao),2) # Valor Pressão
        perc_pressao = round(((fechamento_pressao - abertura_pressao) / abertura_pressao) * 100,2) # %Pressão

    return valor_pressao, perc_pressao;

def pressao_maior(stock_info,estrategia,print_log=True):

    ticker = stock_info

    ticker = ticker.reset_index()

    #Busca pela linha que tem o maior valor no período
    idx = ticker.loc[ticker['Open'].idxmax()]
    #Pega qual a data da linha selecionada acima
    max_date = getattr(idx,"Date")
    #max_date = getattr(idx,"Datetime")
    # Elimina todas as linhas anteriores a data do maior valor do periodo
    lista_pressao = ticker.drop(ticker[ticker.Date < max_date].index)
    #Elimina as linha que náo tem dados - coluna Open = Nan
    lista_pressao = lista_pressao[lista_pressao['Open'].notna()]
    #Ordena por data
    lista_pressao.sort_values(by='Date', inplace=True, ascending=True) # sort instruction
    #lista_pressao.sort_values(by='Datetime', inplace=True, ascending=True) # sort instruction
    #Calucula diferença entre os fechamentos
    lista_pressao['Diff']     = lista_pressao['Close'].diff()
    #Calcula tamanho do corpo da barra
    lista_pressao['Bar_diff'] = lista_pressao['Close'] - lista_pressao['Open']
    #Preenche com 0 os campos calculados acima que estão com Nan
    lista_pressao['Diff']     = lista_pressao['Diff'].fillna(0)
    lista_pressao['Bar_diff'] = lista_pressao['Bar_diff'].fillna(0)

    if (print_log == True):
        print('------ INICIO LEITURA PRESSÃO ------')

    lista = lista_pressao

    seq_barras_neg = mc_count = seq_pressao = 0
    max_ant = min_ant = max_qq = valor_stop_qq = 0.0
    pressao_aberta = alvo = nova_min = False
    abertura_pressao = 0.0
    fechamento_pressao = 0.0

    for index, row in lista.iterrows():

        # IGNORA DATAS QUE NÃO FOREM SEGUNDAS (ISOWEEKDAY = 1)
        time = datetime.date(row['Date'])
        #time = datetime.date(row['Datetime'])
        if (estrategia =='DIARIO'):
            if (time.isoweekday() != 1):
                continue

        #print(row)


        #CONTAGEM SEQUENCIA DE BARRAS NEGATIVAS
        if (row['Bar_diff'] < 0):
            seq_barras_neg += 1
        else:
            seq_barras_neg = 0

        #CONTAGEM DE BARRAS EM MICROCANAL

        if ((min_ant > row['Low']) & (max_ant > row['High'])):
            mc_count += 1
        else:
            mc_count = 1
        #print(str(mc_count) + '/' + str(min_ant) + '/' + str(row['Low']) + '--' + str(max_ant) + '/' + str(row['High']))

        if (pressao_aberta == False): # NÃO TEM PRESSÃO ABERTA
            if (row['Bar_diff'] < 0): # Se for barra negativa
                if (row['Diff'] < 0): # Se a diferença do dia for negativa - fechamento menor que dia anterior
                    seq_pressao += 1
                    fechamento_pressao = row['Close']
                    if abertura_pressao == 0.0: # Se for a primeira barra da pressão, guarda valor da abertura do dia
                        abertura_pressao = row['Open']
                    if (seq_pressao == 3): # Se for a barra 3 da pressão - ENCONTROU PRESSÃO
                        alvo_pressao = fechamento_pressao + (fechamento_pressao - abertura_pressao)
                        pressao_aberta = True
                        if (alvo_pressao < 0): # Se alvo da pressão for < 0 - fixa em 0.0 o alvo (aconteceu em PARA)
                            alvo_pressao = 0.0

                        if (print_log == True):
                            print(time.strftime(("%d/%m/%Y")) + ' - PRESSÃO DE VENDA ABERTA', end=" ")
                            print('| Fechamento Pressão: ' + str("%.2f" %fechamento_pressao), end=" ")
                            #print('Abertura Pressão: ' + str(abertura_pressao))
                            print('| Alvo da Pressão: ' + str("%.2f" %alvo_pressao))
                            #print('Max Alvo: ' + str(max_alvo))

                        min_min = row['Low']
                        seq_qq = 0
                else: # Se for um fechamento acima da anterior, começa a contar a partir da barra atual
                    seq_pressao = 1
                    abertura_pressao = row['Open']
            else: # Se for barra positiva, zera a contagem de barras
                seq_pressao = 0
                abertura_pressao = 0.0
                fechamento_pressao = 0.0
        else: # PRESSÃO ABERTA
            if (alvo == False): #PRESSÃO NÃO ATINGIU ALVO
                # print(time.strftime(("%d/%m/%Y")) + ': MaxAnt: ' + str(max_ant) + '/ Max atual: ' + str(row['High']) + ' / Max QQ: ' + str(max_qq) + ' / Min Min: ' + str(min_min) + ' / Min Atual: ' + str(row['Low']))
                if ((valor_stop_qq > 0.0) & (valor_stop_qq < row['High'])):
                    if (print_log == True):
                        print(time.strftime(("%d/%m/%Y")) + ' - FIM DA PRESSÃO - Stop QQ ')
                    pressao_aberta = False
                    if (row['Bar_diff'] < 0):
                        seq_pressao = 1
                        seq_qq = 0
                        valor_stop_qq = 0.0
                        abertura_pressao = row['Open']
                    else:
                        seq_pressao = 0
                        seq_qq = 0
                        valor_stop_qq = 0.0
                else:
                    #if ((max_ant < row['High']) & (fechamento_pressao < row['High']) & (nova_min == False)): # MOD 28/09/2022
                    if ((max_ant < row['High']) & (fechamento_pressao < row['High'])):
                        seq_qq += 1
                        max_qq = row['High']

                        if (seq_qq == 1):
                            if (print_log == True):
                                print(time.strftime(("%d/%m/%Y")) + ' - ' + str(seq_qq) + ' Quebra')
                            # TESTE -
                            if (min_min > row['Low']):
                                min_min = row['Low']
                                seq_qq = 0
                                if (print_log == True):
                                    print(time.strftime(("%d/%m/%Y")) + ' - Nova Minima')
                            # TESTE                    
                        if (seq_qq == 2):
                            valor_stop_qq = row['High']
                            if (print_log == True):
                                print(time.strftime(("%d/%m/%Y")) + ' - ' + str(seq_qq) + ' Quebra', end=" ")
                                print('| Valor Stop QQ: ' + str("%.2f" %valor_stop_qq))
                    else:
                        nova_min = False
                        if (min_min > row['Low']):
                            min_min = row['Low']
                            seq_qq = 0
                            max_qq = fechamento_pressao
                            nova_min = True
                            if (print_log == True):
                                print(time.strftime(("%d/%m/%Y")) + ' - Nova Minima')


                    if (row['Low'] <= alvo_pressao):  # Atingiu alvo da pressão
                        alvo = True
                        max_alvo = row['High']
                        min_min = row['Low']
                        seq_qq = 0 # 2022-10-14
                        # Se tem 3 ou mais barras de pressão em sequencia - Microcanal

                        if (mc_count >= 3):
                            microcanal = True
                            if (print_log == True):
                                print(time.strftime(("%d/%m/%Y")) + ' - Alvo Pressão atingido - MICROCANAL')
                        else:
                            microcanal = False
                            if (print_log == True):
                                print(time.strftime(("%d/%m/%Y")) + ' - Alvo Pressão atingido')
            else: # PRESSÃO ATINGIU ALVO
                if (microcanal == False): # GESTÃO BARRA-A-BARRA (BÊBADO)
                    if (max_ant < row['High']):
                        if (print_log == True):
                            print(time.strftime(("%d/%m/%Y")) + ' - FIM DA PRESSÃO - BAR-BY-BAR ')
                        pressao_aberta = False
                        alvo = False
                        if (row['Bar_diff'] < 0):
                            seq_pressao = 1
                            abertura_pressao = row['Open']
                            seq_qq = 0
                            valor_stop_qq = 0.0
                        else:
                            seq_pressao = 0
                            seq_qq = 0
                            valor_stop_qq = 0.0
                else: # GESTÃO MICROCANAL - QUEBRA-QUEBRA ou 2a TENTATIVA
                    #print("Pressão Alvo  MC")
                    if ((valor_stop_qq > 0.0) & (valor_stop_qq < row['High'])):
                        if (print_log == True):
                            print(time.strftime(("%d/%m/%Y")) + ' - FIM DA PRESSÃO - Stop QQ')
                        pressao_aberta = False
                        alvo = False
                        if (row['Bar_diff'] < 0):
                            seq_pressao = 1
                            abertura_pressao = row['Open']
                            seq_qq = 0
                            valor_stop_qq = 0.0
                        else:
                            seq_pressao = 0
                            seq_qq = 0
                            valor_stop_qq = 0.0
                    else:
                        if (max_ant < row['High']):
                            seq_qq += 1
                            max_qq = row['High']
                            if (seq_qq == 1):
                                if (print_log == True):
                                    print(time.strftime(("%d/%m/%Y")) + ' - ' + str(seq_qq) + ' Quebra')
                                # TESTE -
                                if (min_min > row['Low']):
                                    min_min = row['Low']
                                    seq_qq = 0
                                    if (print_log == True):
                                        print(time.strftime(("%d/%m/%Y")) + ' - Nova Minima')
                                # TESTE  
                            if (seq_qq == 2):
                                valor_stop_qq = row['High']
                                if (print_log == True):
                                    print(time.strftime(("%d/%m/%Y")) + ' - ' + str(seq_qq) + ' Quebra', end=" ")
                                    print('| Valor Stop QQ: ' + str("%.2f" % valor_stop_qq))
                        else:
                            nova_min = False
                            if (min_min > row['Low']):
                                min_min = row['Low']
                                seq_qq = 0
                                #max_qq = fechamento_pressao
                                nova_min = True
                                if (print_log == True):
                                    print(time.strftime(("%d/%m/%Y")) + ' - ALVO - Nova Minima QQ')
                            if ((nova_min == False) & (min_ant > row['Low'])):
                                microcanal = False

        min_ant = row['Low']
        max_ant = row['High']

    return pressao_aberta