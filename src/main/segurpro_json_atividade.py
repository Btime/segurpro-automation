import requests
from ..model.table_json_segurpro import create_table, insert_data_json, table_exist
from ..utils.excel_infos_json import ExcelCollector
from src.enum.sistema_enum import SistemaEnum
from openai import OpenAI
from src.config.configuration import API_KEY_GPT

class ColetaSegurPro:
    def __init__(self) -> None:
        self.excel = ExcelCollector()
        self.__api_chatgpt = API_KEY_GPT

    def chatgpt(self, texto: str, triagem: bool = False):
        self.client = OpenAI(api_key=self.__api_chatgpt)


        prompt_texto =  """
                            faça a analise com o que mandei de input e traga o texto que criou de resumo. 
                            Separe a análise em tópicos e traga o texto formatado em markdown. 
                            Tire "\n" e quebre a linha por cada tópico.
                        """. strip()
        
        prompt_triagem = """
                            Faça uma analise do que mandei de input e retorne True se existir as palavras chave: 
                            offiline, inoperante, off-line.
                         """.strip()

        self.completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        
        messages=[
            {
                "role": "system", 
                "content": prompt_triagem if triagem else prompt_texto
            },
            {
                "role": "user", 
                "content": texto
            }
        ])

        return self.completion.choices[0].message.content
        
    def coletar_dados_segurpro(self):
        url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

        if not table_exist():
            create_table()

        response = requests.get(url)

        self.excel.create_excel()

        contagem_com_sistema = 1
        contagem_sem_sistema = 1

        if response.status_code == 200:
            dados = response.json()

            # O uso do self em um for não é recomendado
            for self.dado in dados:
                try:
                    if self.dado['STATUS'].startswith('EM ABERTO - '):

                        response = {
                            'ROV': self.dado['ROV'],
                            'STATUS': self.dado['STATUS'],
                            'NOME_SITE': self.dado['NOME_SITE'],
                            'SISTEMA': self.dado['SISTEMA'],
                        }

                        try:
                            
                            insert_data_json(
                                self.dado['ROV'], 
                                self.dado['STATUS'], 
                                self.dado['NOME_SITE'], 
                                self.dado['SISTEMA']
                            )


                            self.excel.append_info(
                                self.dado['ROV'], 
                                self.dado['STATUS'], 
                                self.dado['NOME_SITE'], 
                                self.dado['SISTEMA']
                            )

                            triagem = self.chatgpt(
                                str(self.dado['MOTIVO_ABERTURA']).lower(), 
                                triagem = True
                            )
                            
                            self.tratar_dados_questionario(triagem = triagem)

                            # Criar uma função para retorno de logs, não usar print para debug/info
                            print(f'Total de atividades cadastradas: {contagem_com_sistema}')
                            contagem_com_sistema += 1

                        except Exception as e:
                            print(e)

                except KeyError as key:
                    self.dado[f'{key.args[0]}'] = None if str(key.args[0]) == 'NOME_SITE' else self.dado['NOME_SITE']
                    self.dado[f'{key.args[0]}'] = 'SEM SISTEMA' if str(key.args[0]) == 'SISTEMA' else self.dado['SISTEMA']

                    insert_data_json(self.dado['ROV'], self.dado['STATUS'], self.dado['NOME_SITE'], self.dado['SISTEMA'])
                    self.excel.append_info(self.dado['ROV'], self.dado['STATUS'], self.dado['NOME_SITE'], self.dado['SISTEMA'])

                    # self.tratar_dados_questionario()
                    # print(f'Total de atividades SEM SISTEMA cadastradas: {contagem_sem_sistema}')
                    # contagem_sem_sistema += 1
                    contagem_com_sistema += 1

                    # Criar uma função para retorno de logs, não usar print para debug/info
                    print(f'Total de atividades cadastradas: {contagem_com_sistema}')
                    continue

                except Exception as e:
                    raise e

            print('Extração de TODOS JSON concluído')

            self.excel.save_excel()
        else:
            print('Erro na requisição JSON')

    
    def tratar_dados_questionario(self, triagem: bool = False):
        # Não é uma boa pratica utilizar if
        # Repetir muitas vezes a mesma linha de código alterando apenas 1 parametro.

        sistema = SistemaEnum.DEFAULT.value
        if triagem:
            sistema = SistemaEnum.TRIAGEM.value
        else:
            for s in SistemaEnum:
                if s.name in self.dado['SISTEMA']:
                    sistema = s.value
                    break
    
        # self.inserir_atividade_btime(self.dado['ROV'], sistema, self.dado['STATUS'], self.dado['NOME_SITE'])


    def inserir_atividade_btime(self, rov, checklist, status, nome_site):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsInJvbGVJZCI6MSwid29ya3NwYWNlIjoianVsaWEiLCJhdWQiOiJKb2tlbiIsImV4cCI6MTc0MTI4ODMwNSwiaWF0IjoxNzA5NzUyMzA1LCJpc3MiOiJKb2tlbiIsImp0aSI6IjJ1dDQ1YWRxOW4zcjR1YWczODBhOHY1MSIsIm5iZiI6MTcwOTc1MjMwNX0.7Rn3iL0yky4yGe0eQ8ufYOURuoYYEAQ9_LdNeJJ1TmQ',
            'content-type': 'application/json',
            'origin': 'https://julia.btime.io',
            'projectid': '1',
            'referer': 'https://julia.btime.io/',
            'requestid': 'oZe9oYkM3L',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'workspace': 'julia',
        }

        json_data = {
            'operationName': 'UpsertServiceOrder',
            'variables': {
                'input': {
                    'userId': 11,
                    'checklistId': checklist,
                    'placeId': 19,
                    'assetId': None,
                    'scheduling': '2024-03-15T19:44:00Z',
                    'priorityId': 1,
                    'address': {
                        'address': None,
                        'city': 'São Paulo',
                        'state': 'São Paulo',
                        'neighborhood': None,
                        'country': 'Brasil',
                        'number': None,
                        'postcode': None,
                        'latitude': -23.5557714,
                        'longitude': -46.6395571,
                        'search': 'São Paulo, SP, Brasil',
                    },
                    'description': self.chatgpt(self.dado["MOTIVO_ABERTURA"]),
                    'documents': [],
                    'groupId': None,
                    'events': [
                        {
                            'statusId': 1,
                            'eventDate': '2024-03-11T19:44:48Z',
                        },
                    ],
                    'fieldValues': [],
                },
            },
            'query': 'mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://api.btime.io/new/service-orders/api', headers=headers, json=json_data)

    def start(self):
        # faltando tratar os possíveis erros
        self.coletar_dados_segurpro()