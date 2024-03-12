import pandas as pd

def tratar_repetidos():
    df = pd.read_excel('SERGURPRO_EM_ABERTO.xlsx', usecols=['NOME_SITE'])
    repetidos = df[df.duplicated(subset=['NOME_SITE'], keep=False)]
    retirar_repetidos = df.drop_duplicates(subset=['NOME_SITE'], keep='first')
    retirar_repetidos.to_excel('SEGURPRO_NOME_SITE_SEM_REPETIR.xlsx', index=False)

    print('Tratamento de locais concluído')