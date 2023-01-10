from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import LeituraPressaoBeta as lp
from datetime import datetime

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1C8Z1bxOld1OwCKVl6pHbkVYwIm0zHDNIm8nFgJaS99o'
DIARIO_RANGE_NAME = 'Diário!A:Z'
H4_RANGE_NAME = 'H4!A:Z'




def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__))) #Muda para o diretorio de onde o arquivo está sendo executado
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
           token.write(creds.to_json())

    lista_pressao_saida = ''
    lista_com_pressao_saida = ''
    lista_sem_pressao_saida = ''

    print('------- Inicio Leitura Pressão Diário --------')

    pressao_D = lp.leitura_pressao('ACTV','DIARIO',True)
    if (len(pressao_D) > 0):
        lista_pressao = pressao_D['Ticker']
        lista_pressao_saida = ''
        lista_pressao_saida = ','.join(map(str,lista_pressao))
        print('Pressão Diário.........: ',lista_pressao_saida)
    
        lista_com_pressao = pressao_D.loc[(pressao_D['Pressão Tempo Maior Aberta'] == True)]['Ticker']
        if (len(lista_com_pressao)>0):
            lista_com_pressao_saida = ''
            lista_com_pressao_saida = ','.join(map(str,lista_com_pressao))
            print('Pressão Aberta Semanal.: ',lista_com_pressao_saida)
        else:
            lista_com_pressao_saida = ''
    
        lista_sem_pressao = pressao_D.loc[(pressao_D['Pressão Tempo Maior Aberta'] == False)][['Ticker','% Pressão']]
        if (len(lista_sem_pressao)>0):
            print('------- Sem Pressão Aberta Semanal -------')
            lista_sem_pressao.sort_values(by=['% Pressão'],ascending=False,inplace=True)
            lista_sem_pressao_saida = ''
            lista_sem_pressao_saida = ','.join(map(str,lista_sem_pressao['Ticker']))
            print('Sem Pressão Aberta Semanal.: ',lista_sem_pressao_saida)
            print(lista_sem_pressao)
    else:
        lista_pressao_saida = 'DIA DE FOLGA'
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME).execute()
        # print(result['values'])
        now = datetime.now()
        rows = [
                [now.strftime("%d/%m/%Y"),
                 now.strftime("%H:%M:%S"),
                 lista_pressao_saida, 
                 lista_com_pressao_saida,
                 lista_sem_pressao_saida
                ]
            ]

        resource = {
            "majorDimension": "ROWS",
            "values": rows
        }

        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=DIARIO_RANGE_NAME,
                                body=resource,
                                valueInputOption="USER_ENTERED").execute()
    except HttpError as err:
        print(err)

    print('--------- Fim Leitura Pressão Diário ---------')

    print('--------- Inicio Leitura Pressão H4 ----------')

    pressao_H4 = lp.leitura_pressao('ACTV','H4',True)
    #print(pressao_H4)
    if (len(pressao_H4)>0):
        lista_pressao = pressao_H4['Ticker']
        lista_pressao_saida = ''
        lista_pressao_saida = ','.join(map(str,lista_pressao))
        print('Pressão H4................: ',lista_pressao_saida)
        
        lista_com_pressao = pressao_H4.loc[(pressao_H4['Pressão Tempo Maior Aberta'] == True)]['Ticker']
        if (len(lista_com_pressao)>0):
            lista_com_pressao_saida = ''
            lista_com_pressao_saida = ','.join(map(str,lista_com_pressao))
            print('Pressão Aberta Diário.....: ',lista_com_pressao_saida)
        else:
            lista_com_pressao_saida = ''
        
        
        lista_sem_pressao = pressao_H4.loc[(pressao_H4['Pressão Tempo Maior Aberta'] == False)][['Ticker','% Pressão']]
        if (len(lista_sem_pressao)>0):
            print('------- Sem Pressão Aberta Diário -------')
            lista_sem_pressao.sort_values(by=['% Pressão'],ascending=False,inplace=True)
            lista_sem_pressao_saida = ''
            lista_sem_pressao_saida = ','.join(map(str,lista_sem_pressao['Ticker']))
            print('Sem Pressão Aberta Diário.: ',lista_sem_pressao_saida)
            print(lista_sem_pressao)
    else:
        lista_pressao_saida = 'DIA DE FOLGA H4'

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME).execute()
        # print(result['values'])
        now = datetime.now()
        rows = [
                [now.strftime("%d/%m/%Y"),
                 now.strftime("%H:%M:%S"),
                 lista_pressao_saida, 
                 lista_com_pressao_saida,
                 lista_sem_pressao_saida
                ]
            ]

        resource = {
            "majorDimension": "ROWS",
            "values": rows
        }

        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=H4_RANGE_NAME,
                                body=resource,
                                valueInputOption="USER_ENTERED").execute()
    except HttpError as err:
        print(err)

    print('----------- Fim Leitura Pressão H4 -----------')
    
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    proc_time = end_time - start_time
    print('---------- LOG DE PROCESSAMENTO ----------')
    print('Tempo de Processamento: ', str(proc_time))
    print('------------------------------------------')