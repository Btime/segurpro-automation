from ..model.db.repository.segurpro_repository import SegurproRepository
import requests

class StatusValidation:
    def __init__(self) -> None:
        self.segurpro_repository = SegurproRepository()
        
    def request_test_status(self):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInJvbGVJZCI6MSwid29ya3NwYWNlIjoianVsaWEiLCJhdWQiOiJKb2tlbiIsImV4cCI6MTc0MTg2OTg3OCwiaWF0IjoxNzEwMzMzODc4LCJpc3MiOiJKb2tlbiIsImp0aSI6IjJ1dTU3NmVmaThuaGFtanZxczBoNWMzaSIsIm5iZiI6MTcxMDMzMzg3OH0.xoaHmJ9Za3wzf_E5w0glOEbSiwfwIcz2zrLfY4GCXmE',
            'content-type': 'application/json',
            'origin': 'https://julia.btime.io',
            'projectid': '1',
            'referer': 'https://julia.btime.io/',
            'requestid': '-0jLvWjc4N',
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
            'operationName': 'ServiceOrders',
            'variables': {
                'page': 1,
                'sort': {
                    'field': 'ID',
                    'type': 'ASC',
                },
                'filter': {
                    'parentIds': 1431, # id_activity (id da atividade pai)
                },
            },
            'query': 'query ServiceOrders($page: Int, $search: String, $searchType: ServiceOrderSearchType, $sort: ServiceOrderSort, $filter: ServiceOrderFilter) {\n  serviceOrders(\n    page: $page\n    search: $search\n    searchType: $searchType\n    sort: $sort\n    filter: $filter\n  ) {\n    id\n    name\n    yearlyId\n    insertedAt\n    endDate\n    scheduling\n    childrenCount\n    priority {\n      id\n      name\n      __typename\n    }\n    status {\n      id\n      name\n      label\n      color\n      __typename\n    }\n    checklist {\n      id\n      name\n      __typename\n    }\n    place {\n      id\n      name\n      resume\n      __typename\n    }\n    asset {\n      id\n      name\n      type {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    group {\n      id\n      name\n      __typename\n    }\n    user {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://api.btime.io/new/service-orders/api', headers=headers, json=json_data)

        status = response.json()

        label_value = status['data']['serviceOrders'][-1]['status']['label']
        print(f'Status: {label_value}')

        list_status = ['Aberta', 'Pausada', 'Execução', 'Recebida']

        if label_value in list_status:
            return True
        else:
            return False

    def request_test_create(self):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInJvbGVJZCI6MSwid29ya3NwYWNlIjoianVsaWEiLCJhdWQiOiJKb2tlbiIsImV4cCI6MTc0MTg2OTg3OCwiaWF0IjoxNzEwMzMzODc4LCJpc3MiOiJKb2tlbiIsImp0aSI6IjJ1dTU3NmVmaThuaGFtanZxczBoNWMzaSIsIm5iZiI6MTcxMDMzMzg3OH0.xoaHmJ9Za3wzf_E5w0glOEbSiwfwIcz2zrLfY4GCXmE',
            'content-type': 'application/json',
            'origin': 'https://julia.btime.io',
            'projectid': '1',
            'referer': 'https://julia.btime.io/',
            'requestid': 'IiSmBUus1G',
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
            'operationName': 'ServiceOrders',
            'variables': {
                'page': 1,
                'sort': {
                    'field': 'ID',
                    'type': 'ASC',
                },
                'filter': {
                    'parentIds': 1431,
                },
            },
            'query': 'query ServiceOrders($page: Int, $search: String, $searchType: ServiceOrderSearchType, $sort: ServiceOrderSort, $filter: ServiceOrderFilter) {\n  serviceOrders(\n    page: $page\n    search: $search\n    searchType: $searchType\n    sort: $sort\n    filter: $filter\n  ) {\n    id\n    name\n    yearlyId\n    insertedAt\n    endDate\n    scheduling\n    childrenCount\n    priority {\n      id\n      name\n      __typename\n    }\n    status {\n      id\n      name\n      label\n      color\n      __typename\n    }\n    checklist {\n      id\n      name\n      __typename\n    }\n    place {\n      id\n      name\n      resume\n      __typename\n    }\n    asset {\n      id\n      name\n      type {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    group {\n      id\n      name\n      __typename\n    }\n    user {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://api.btime.io/new/service-orders/api', headers=headers, json=json_data)

    def request_test_edit(self):
        headers = {
            'authority': 'api.btime.io',
            'accept': '*/*',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInJvbGVJZCI6MSwid29ya3NwYWNlIjoianVsaWEiLCJhdWQiOiJKb2tlbiIsImV4cCI6MTc0MTg2OTg3OCwiaWF0IjoxNzEwMzMzODc4LCJpc3MiOiJKb2tlbiIsImp0aSI6IjJ1dTU3NmVmaThuaGFtanZxczBoNWMzaSIsIm5iZiI6MTcxMDMzMzg3OH0.xoaHmJ9Za3wzf_E5w0glOEbSiwfwIcz2zrLfY4GCXmE',
            'content-type': 'application/json',
            'origin': 'https://julia.btime.io',
            'projectid': '1',
            'referer': 'https://julia.btime.io/',
            'requestid': 'OOxmz4Ags1',
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
                    'id': 1434,
                    'name': None,
                    'userId': 1,
                    'checklistId': 39,
                    'placeId': 19,
                    'assetId': None,
                    'scheduling': None,
                    'priorityId': 2,
                    'address': None,
                    'description': None,
                    'documents': [],
                    'groupId': None,
                    'fieldValues': [],
                },
            },
            'query': 'mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://api.btime.io/new/service-orders/api', headers=headers, json=json_data)


    def editar_teste(self):

        valor = self.request_test_status()

        if valor == True:
            self.segurpro_repository.update('status', 1431, 'Abri')
            self.request_test_edit()
        else:
            self.segurpro_repository.insert(1450, 1, 'Aberta', 'site', 'system', 'description', 1)
            self.request_test_edit()

    def run(self):
        self.editar_teste()


    """ 
    SE A ULTIMA ATIVIDADE FILHA FOR != DE ABERTO, ENTÃO CRIA UMA NOVA ATIVIDADE FILHA E SALVA NO DB COM O PAGE E AS INFORMAÇÕES NOVAS DE ACORDO COM O ID
    SE A ULTIMA ATIVIDADE FILHA FOR == ABERTO, ENTÃO APENAS FAREMOS UPDATE NELA PARA ATUALIZAR AS INFORMAÇÕES
    """