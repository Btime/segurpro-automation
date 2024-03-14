import requests

from src.utils.excel_infos_json import ExcelCollector
from src.utils.chatgpt_utils import ChatGPT
from src.enum.sistema_enum import SistemaEnum
from src.config.configuration import AUTHORIZATION
from src.model.db.repository.segurpro_repository import SegurproRepository

from typing import Dict, Union

class CreateActivityBtime:
    def __init__(self, data) -> None:
        self.data = data
        self.excel = ExcelCollector()
        self.chatGPT = ChatGPT()
        self.segurpro_repository = SegurproRepository()

    def filter_data(self):
        data = list(
            filter(
                lambda dado: dado.get(
                    'STATUS'
                ).startswith(
                    'EM ABERTO'
                ) and not dado.get('STATUS').startswith('EM ABERTO - RETORNO TECNICO'), self.data
            )
        )
        return data

    def save_excel_file(self):
        return self.excel.save_excel()

    def verify_triage(self, data: Dict[str, Union[str, int]]):
        motivo_abertura = data.get('MOTIVO_ABERTURA')
        verificacao = bool(self.chatGPT.prompt(texto=motivo_abertura, triagem=True))
        return verificacao


    def export_data(self, data: Dict[str, Union[str, int]]) -> None:
        """
        Exports the given data to Btime and the JSON and Excel files.

        Args:
            data (Dict[str, Union[str, int]]): The data to be exported.

        Returns:
            None
        """
        for dado in data:
            triagem = self.verify_triage(dado)
            checklist = self.obtain_checklist(dado, triagem=triagem)
            activity_id = self.insert_data(dado, checklist)
            
            self.segurpro_repository.insert(
                id_activity=activity_id,
                rov=dado.get("ROV"),
                status=dado.get("STATUS"),
                site_name=dado.get("NOME_SITE"),
                system=dado.get("SISTEMA"),
                description=dado.get("MOTIVO_ABERTURA"),
                triage=triagem
            )

    def obtain_checklist(self, data: Dict[str, Union[str, int]], triagem: bool = False) -> int:
        checklist = (
            SistemaEnum.TRIAGEM.value  
            if triagem
            else next(
                map(
                    lambda s: s.value,
                    filter(
                        lambda s: s.name in (data.get("SISTEMA") or ""), SistemaEnum
                    ),
                ),
                SistemaEnum.DEFAULT.value,
            )
        )
        return checklist
    
    def insert_data(self, data: Dict[str, Union[str, int]], checklist: int) -> int:
        id_activity = self.request_insert_btime(
            motivo_abertura=data.get("MOTIVO_ABERTURA"),
            rov=data.get("ROV"),
            checklist=checklist,
            nome_site=data.get("NOME_SITE"),
        )
        return id_activity
    
    def request_insert_btime(
        self,
        motivo_abertura: str,
        rov: str,
        checklist: str,
        nome_site: str,
    ) -> int:
        """
        Inserts a new activity in the Btime database and returns the activity ID.

        Args:
            motivo_abertura (str): The activity description.
            rov (str): The ROV (Regional Operations Center).
            checklist (str): The checklist ID.
            nome_site (str): The site name.

        Returns:
            int: The activity ID.
        """
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
                    'description': self.chatGPT.prompt(motivo_abertura),
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
        if response.ok:
            data = response.json()

            return data["data"]['upsertServiceOrder']['id']
        
    def run(self):
        data = self.filter_data()
        self.export_data(data)