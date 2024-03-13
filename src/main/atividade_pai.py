import requests
from src.config.configuration import AUTHORIZATION

def inserir_atividade_pai(self, motivo_abertura: str, rov: str, checklist: str, nome_site: str):
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