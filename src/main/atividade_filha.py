import requests
from src.config.configuration import AUTHORIZATION

def inserir_atividade_filha(self, motivo_abertura: str, rov: str, checklist: str, nome_site: str):
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
                'checklistId': 39,
                'placeId': 14,
                'assetId': None,
                'scheduling': None,
                'priorityId': None,
                'address': None,
                'description': None,
                'parentId': 590,
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
    print(response.json())