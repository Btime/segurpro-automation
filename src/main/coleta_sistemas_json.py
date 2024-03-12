import pandas as pd
import requests
from openpyxl import Workbook

def coletar_dados_segurpro():
    url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

    response = requests.get(url)

    contagem = 1
    
    nome_excel = 'SISTEMAS_SEGURPRO.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = "SISTEMAS SEGURPRO"

    headers = ["SISTEMAS"]
    ws.append(headers)

    if response.status_code == 200:
        dados = response.json()
    
        for dado in dados:
            try:

                response = {
                    'SISTEMA': dado['SISTEMA']
                }

                try:
                    ws.append([dado['SISTEMA']])

                    print(f'Total de atividades cadastradas: {contagem}')
                    contagem += 1
                except Exception as e:
                        print("Erro ao inserir dados:", e)

            except Exception as e:
                # print(e)
                 ...

        wb.save(nome_excel)

def tratar_repetidos():
    df = pd.read_excel('SISTEMAS_SEGURPRO.xlsx', usecols=['SISTEMAS'])
    repetidos = df[df.duplicated(subset=['SISTEMAS'], keep=False)]
    retirar_repetidos = df.drop_duplicates(subset=['SISTEMAS'], keep='first')
    retirar_repetidos.to_excel('SISTEMA_TIRAR_REPETIDOS.xlsx', index=False)

    print('Tratamento de locais concluído')
            
coletar_dados_segurpro()
tratar_repetidos()


# CFTV ID 38
# ALARME ID 39
# CONTROLE DE ACESSO ID 40