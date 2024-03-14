import requests
from src.utils.chatgpt_utils import ChatGPT
from src.utils.excel_infos_json import ExcelCollector
from src.config.configuration import AUTHORIZATION
from src.enum.sistema_enum import SistemaEnum
from src.model.db.repository.segurpro_repository import SegurproRepository

class CreatedActivityChildren:
    def __init__(self, data) -> None:
        self.chatGPT = ChatGPT()
        self.excel = ExcelCollector()
        self.data = data
        self.segurpro_repository = SegurproRepository()

    def get_rov_response(self, response):
        list_rov = list(
            map(
                lambda data: (
                    {
                        "ROV": data.get("ROV"),    
                        "SISTEMA": data.get("SISTEMA"),
                        "MOTIVO_ABERTURA": data.get("MOTIVO_ABERTURA"),
                        "NOME_SITE": data.get("NOME_SITE"),
                        "STATUS": data.get("STATUS")   
                    }
                ),
                filter(
                    lambda data: data.get(
                        'STATUS'
                    ).startswith(
                        'EM ABERTO - RETORNO TECNICO'
                    ), response
                )
            )
        )
        return list_rov

    
    def created_activity(self, opening_reason: str, rov: str, checklist: str, site_name: str):
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
                    'description': self.chatGPT.prompt(opening_reason),
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

    def created_activity_children(self, parent_id, checklist, opening_reason):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInJvbGVJZCI6MSwid29ya3NwYWNlIjoianVsaWEiLCJhdWQiOiJKb2tlbiIsImV4cCI6MTc0MTg2OTg3OCwiaWF0IjoxNzEwMzMzODc4LCJpc3MiOiJKb2tlbiIsImp0aSI6IjJ1dTU3NmVmaThuaGFtanZxczBoNWMzaSIsIm5iZiI6MTcxMDMzMzg3OH0.xoaHmJ9Za3wzf_E5w0glOEbSiwfwIcz2zrLfY4GCXmE',
            'content-type': 'application/json',
            'origin': 'https://julia.btime.io',
            'projectid': '1',
            'referer': 'https://julia.btime.io/',
            'requestid': 'H1rHDb1bRe',
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
                    'placeId': 14,
                    'assetId': None,
                    'scheduling': None,
                    'priorityId': None,
                    'address': None,
                    'description': self.chatGPT.prompt(opening_reason),
                    'parentId': parent_id,
                    'parentDependent': False,
                    'documents': [],
                    'groupId': None,
                    'events': [
                        {
                            'statusId': 1,
                            'eventDate': '2024-03-13T16:52:41Z',
                        },
                    ],
                    'fieldValues': [],
                },
            },
            'query': 'mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n',
        }
        response = requests.post('https://api.btime.io/new/service-orders/api', headers=headers, json=json_data)
        if response.ok:
            return response.json()
        
    def match_id_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        return results
    
    def verify_triage(self, data):
        opening_reason = data.get('MOTIVO_ABERTURA')
        verification = bool(self.chatGPT.prompt(texto=opening_reason, triagem=True))
        
        return verification
    
    def verify_checklist(self, data, triage = False):
        checklist = (
            SistemaEnum.TRIAGEM.value
            if triage
            else next(
                map(
                    lambda s: s.value, 
                    filter(lambda s: s.name  in (data.get('SISTEMA') or ""), SistemaEnum)
                ),
                SistemaEnum.DEFAULT.value
            )
        )
        return checklist
    
    def run(self):
        
        data = self.get_rov_response(self.data)
        for dado in data:
            parent_id = self.match_id_activity(dado.get("ROV"))
            is_triage = self.verify_triage(dado)
            checklist = self.verify_checklist(dado, triage=is_triage)
            
            if parent_id is not None:
                self.created_activity_children(
                    parent_id=parent_id,
                    opening_reason=dado.get("MOTIVO_ABERTURA"),
                    checklist=checklist
                )
            else:
                parent_id = self.created_activity(
                    rov= dado.get("ROV"),
                    opening_reason=dado.get("MOTIVO_ABERTURA"),
                    site_name=dado.get("NOME_SITE"),
                    checklist=checklist,
                )
            
            self.segurpro_repository.insert(
                id_activity=parent_id,
                rov=dado["ROV"],
                status=dado["STATUS"],
                site_name=dado["NOME_SITE"],
                system=dado["SISTEMA"],
                description=dado["MOTIVO_ABERTURA"],
                triage=is_triage
            )