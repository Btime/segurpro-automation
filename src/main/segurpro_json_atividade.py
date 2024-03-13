import requests
from ..model.table_json_segurpro import create_table, insert_data_json, table_exist
from ..utils.excel_infos_json import ExcelCollector
from src.enum.sistema_enum import SistemaEnum
from openai import OpenAI 
from src.config.configuration import API_KEY_GPT, AUTHORIZATION
from typing import Dict, Union, List

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
                            Análise do Problema: Avaliar o conteúdo do texto recebido para identificar a natureza do problema com o equipamento ou sistema.
                            Condições de Resposta: Se o texto indicar que o problema pode ser diagnosticado ou resolvido remotamente (equipamento inoperante, offline, ou problemas de conectividade), devo retornar TRUE. Se o texto sugerir a necessidade de ações físicas como instalação, remanejamento, reposicionamento, ou presença física de um técnico, devo retornar FALSE.
                            Resultado da Análise: Retornar TRUE para situações que requerem triagem e possíveis soluções remotas. Retornar FALSE para situações que necessitam de ação direta de um técnico no local.
                            Observação: A necessidade de acompanhamento implica ações presenciais, pois geralmente envolve instalação ou supervisão física.
                            Traga apenas o resultado TRUE ou FALSE, nenhum texto adicional pois vou utilizar api
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


        message = self.completion.choices[0].message.content

        if triagem:
            if message.lower() == "false":
                return False
            else:
                return True
        return message

        # teste = bool(message)
        # return message
    
    def coletar_dados_segurpro(self):
        try:
            url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

            if not table_exist():
                create_table()

            response = requests.get(url)

            self.excel.create_excel()

            if response.ok:
                dados = response.json()

                response = list(
                    filter(
                        lambda dado: dado.get('STATUS').startswith('EM ABERTO'), dados
                    )
                )
                
                list(
                    map(
                        lambda dado: (
                            x := self.verificacao_triagem(dado),
                            insert_data_json(
                                dado.get("ROV"), 
                                dado.get("STATUS"), 
                                dado.get("NOME_SITE"), 
                                dado.get("SISTEMA"),
                                dado.get("MOTIVO_ABERTURA"),
                                x
                            ), 
                            self.excel.append_info(
                                dado.get("ROV"), 
                                dado.get("STATUS"), 
                                dado.get("NOME_SITE"), 
                                dado.get("SISTEMA"),
                                dado.get("MOTIVO_ABERTURA"),
                                x
                            ),
                            self.tratar_dados_questionario(
                                dado, 
                                triagem=x
                            )
                        ), 
                        response
                    )
                )
                

                
                self.excel.save_excel()
                # self.tratar_dados_questionario(triagem = triagem)

                list(
                    map(
                        lambda dado: self.tratar_dados_questionario(dado, triagem=self.verificacao_triagem(dado)), response
                    )
                )

            else:
                raise response.status_code
            
            # triagem = self.chatgpt(str(self.dado['MOTIVO_ABERTURA']).lower(), triagem = True)
            # self.tratar_dados_questionario(triagem = triagem)
            
        except Exception as ex:
            raise ex
        
    def verificacao_triagem(self, dado):
        motivo_abertura = dado.get('MOTIVO_ABERTURA')
        verificacao: bool = bool(self.chatgpt(texto=motivo_abertura, triagem=True))
        
        return verificacao

    def tratar_dados_questionario(
        self, 
        dado: Dict[str, Union[str, int]], 
        triagem: bool = False
    ) -> None:
        """
        Treat data from the questionnaire.

        Args:
            dado (Dict[str, Union[str, int]]): The data from the questionnaire.
            triagem (bool, optional): Flag indicating if it is a triage. Defaults to False.
        """
        
        checklist = (
            SistemaEnum.TRIAGEM.value  # type: ignore
            if triagem
            else next(
                map(
                    lambda s: s.value, 
                    filter(lambda s: s.name  in (dado.get('SISTEMA') or ""), SistemaEnum)
                ),
                SistemaEnum.DEFAULT.value
            )
        )

        self.inserir_atividade_btime(
            motivo_abertura=dado.get('MOTIVO_ABERTURA'), 
            rov=dado.get('ROV'), 
            checklist=checklist, 
            nome_site=dado.get('NOME_SITE')
        )  # NOME_SITE = LOCAL NA BTIME


    def inserir_atividade_btime(self, motivo_abertura: str, rov: str, checklist: str, nome_site: str):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': AUTHORIZATION,
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
                    'placeId': 19, # nome_site
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
                    'description': self.chatgpt(motivo_abertura),
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