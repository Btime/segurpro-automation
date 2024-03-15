import requests
from src.utils.logs import Log, log_wrapper
from src.utils.chatgpt_utils import ChatGPT
from src.utils.excel_infos_json import ExcelCollector
from src.utils.time_utc import datetime_brasilia_format
from src.utils.headers_utils import get_headers
from src.enum.sistema_enum import SistemaEnum
from src.model.db.repository.segurpro_repository import SegurproRepository


class CreatedActivityChildren:
    def __init__(self, data) -> None:
        self.data = data
        self.chatGPT = ChatGPT()
        self.excel = ExcelCollector()
        self.segurpro_repository = SegurproRepository()
        self.log = Log()
        self.headers = get_headers()

    @log_wrapper
    def filter_data(self, response):
        data = list(
            map(
                lambda data: (
                    {
                        "ROV": data.get("ROV"),
                        "SISTEMA": data.get("SISTEMA"),
                        "MOTIVO_ABERTURA": data.get("MOTIVO_ABERTURA"),
                        "NOME_SITE": data.get("NOME_SITE"),
                        "STATUS": data.get("STATUS"),
                    }
                ),
                filter(
                    lambda data: data.get("STATUS").startswith(
                        "EM ABERTO - RETORNO TECNICO"
                    ),
                    response,
                ),
            )
        )
        return data

    def request_status_activity(self, id_activity):
        data = (
            '{"operationName":"Events","variables":{"serviceOrderIds":[%s]},"query":"query Events($serviceOrderIds: [Int]) {\\n events(filter: {serviceOrderIds: $serviceOrderIds}) {\\n id\\n eventDate\\n status {\\n id\\n name\\n color\\n __typename\\n }\\n reason {\\n id\\n name\\n __typename\\n }\\n description\\n user {\\n id\\n name\\n __typename\\n }\\n __typename\\n }\\n}\\n"}'
            % id_activity
        )

        response = requests.post(
            "https://api.btime.io/new/service-orders/api",
            headers=self.headers,
            data=data,
        )
        data = (
            response.json()["data"]["events"][0]["status"]["id"]
            if id_activity
            else None
        )

        return data

    @log_wrapper
    def request_created_activity(
        self, opening_reason: str, rov: str, checklist: str, site_name: str
    ):
        json_data = {
            "operationName": "UpsertServiceOrder",
            "variables": {
                "input": {
                    "userId": 11,
                    "checklistId": checklist,
                    "placeId": 19,  # nome_site
                    "assetId": None,
                    "scheduling": None,
                    "priorityId": 1,
                    "address": {
                        "address": None,
                        "city": "São Paulo",
                        "state": "São Paulo",
                        "neighborhood": None,
                        "country": "Brasil",
                        "number": None,
                        "postcode": None,
                        "latitude": -23.5557714,
                        "longitude": -46.6395571,
                        "search": "São Paulo, SP, Brasil",
                    },
                    "description": self.chatGPT.prompt(opening_reason),
                    "documents": [],
                    "groupId": None,
                    "events": [
                        {
                            "statusId": 1,
                            "eventDate": datetime_brasilia_format(),
                        },
                    ],
                    "fieldValues": [],
                },
            },
            "query": "mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n",
        }

        response = requests.post(
            "https://api.btime.io/new/service-orders/api",
            headers=self.headers,
            json=json_data,
        )

        self.log.info(data=response.json(), status_code=response.status_code)

        if response.ok:
            data = response.json()
            return data["data"]["upsertServiceOrder"]["id"]

    @log_wrapper
    def request_created_activity_children(self, parent_id, checklist, opening_reason):
        json_data = {
            "operationName": "UpsertServiceOrder",
            "variables": {
                "input": {
                    "userId": 11,
                    "checklistId": checklist,
                    "placeId": 14,
                    "assetId": None,
                    "scheduling": None,
                    "priorityId": None,
                    "address": None,
                    "description": self.chatGPT.prompt(opening_reason),
                    "parentId": parent_id,
                    "parentDependent": False,
                    "documents": [],
                    "groupId": None,
                    "events": [
                        {
                            "statusId": 1,
                            "eventDate": datetime_brasilia_format(),
                        },
                    ],
                    "fieldValues": [],
                },
            },
            "query": "mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n",
        }
        response = requests.post(
            "https://api.btime.io/new/service-orders/api",
            headers=self.headers,
            json=json_data,
        )
        self.log.info(data=response.json(), status_code=response.status_code)

        if response.ok:
            data = response.json()
            id_children = data["data"]["upsertServiceOrder"]["id"]
            return id_children

    @log_wrapper
    def request_get_status(self, parent_id):
        json_data = {
            "operationName": "ServiceOrders",
            "variables": {
                "page": 1,
                "sort": {
                    "field": "ID",
                    "type": "ASC",
                },
                "filter": {
                    "parentIds": parent_id,  # id_activity (id da atividade pai)
                },
            },
            "query": "query ServiceOrders($page: Int, $search: String, $searchType: ServiceOrderSearchType, $sort: ServiceOrderSort, $filter: ServiceOrderFilter) {\n  serviceOrders(\n    page: $page\n    search: $search\n    searchType: $searchType\n    sort: $sort\n    filter: $filter\n  ) {\n    id\n    name\n    yearlyId\n    insertedAt\n    endDate\n    scheduling\n    childrenCount\n    priority {\n      id\n      name\n      __typename\n    }\n    status {\n      id\n      name\n      label\n      color\n      __typename\n    }\n    checklist {\n      id\n      name\n      __typename\n    }\n    place {\n      id\n      name\n      resume\n      __typename\n    }\n    asset {\n      id\n      name\n      type {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    group {\n      id\n      name\n      __typename\n    }\n    user {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        response = requests.post(
            "https://api.btime.io/new/service-orders/api",
            headers=self.headers,
            json=json_data,
        )
        data = response.json()

        service_orders = data["data"]["serviceOrders"] if data else None
        status = service_orders[-1]["status"]["id"] if service_orders else None

        status_id = [1, 2, 5, 6]

        status_verified = True if status in status_id else False

        self.log.info(data=data, status=status, status_code=response.status_code)

        return status_verified

    @log_wrapper
    def request_edit_activity(self, id):
        json_data = {
            'operationName': 'UpsertServiceOrder',
            'variables': {
                'input': {
                    'id': id,
                    'name': None,
                    'userId': 11,
                    'checklistId': 33,
                    'placeId': 18,
                    'assetId': None,
                    'scheduling': None,
                    'priorityId': 1,
                    'address': None,
                    'description': 'teste real funcionando',
                    'documents': [],
                    'groupId': None,
                    'fieldValues': [],
                },
            },
            'query': 'mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://api.btime.io/new/service-orders/api', headers=self.headers, json=json_data)

        print(response.status_code)

        return response

    @log_wrapper
    def request_edit_activity_children(self, id_children, checklist, opening_reason):
        json_data = {
            "operationName": "UpsertServiceOrder",
            "variables": {
                "input": {
                    "id": id_children,
                    "name": None,
                    "userId": 10,
                    "checklistId": checklist,
                    "placeId": 5,
                    "assetId": None,
                    "scheduling": None,
                    "priorityId": None,
                    "address": None,
                    "description": opening_reason,
                    "documents": [],
                    "groupId": None,
                    "fieldValues": [],
                },
            },
            "query": "mutation UpsertServiceOrder($input: ServiceOrderInput) {\n  upsertServiceOrder(input: $input) {\n    id\n    __typename\n  }\n}\n",
        }

        response = requests.post(
            "https://api.btime.io/new/service-orders/api",
            headers=self.headers,
            json=json_data,
        )

        self.log.info(data=response.text, status_code=response.status_code)

    @log_wrapper
    def match_status_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        results = results.status_btime if results else None

        return results

    @log_wrapper
    def match_id_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        results = results.id_activity if results else None

        return results

    @log_wrapper
    def match_id_children(self, rov):
        results_children = self.segurpro_repository.filter_by_rov_children(rov)
        results_children = results_children.id_children if results_children else None
        return results_children

    @log_wrapper
    def validate_status(self, status_btime_api: int, status_btime_db: str):
        try:
            status_btime_db = int(status_btime_db) if status_btime_db.isdigit() else status_btime_db
            is_valid = True if status_btime_api == status_btime_db else False
            return is_valid
        except:
            return False

    @log_wrapper
    def verify_triage(self, data):
        opening_reason = data.get("MOTIVO_ABERTURA")
        verification = bool(self.chatGPT.prompt(texto=opening_reason, triagem=True))
        return verification

    @log_wrapper
    def verify_checklist(self, data, triage=False):
        checklist = (
            SistemaEnum.TRIAGEM.value
            if triage
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

    @log_wrapper
    def created_activity_children(
        self,
        parent_id,
        children_id,
        opening_reason,
        checklist,
        rov,
        verification_status,
        validate_status,
    ):
        if parent_id is not None and children_id is None and validate_status is True:
            children_id = self.request_created_activity_children(
                parent_id=parent_id, opening_reason=opening_reason, checklist=checklist
            )

            self.segurpro_repository.update(
                column="id_children",
                id=parent_id,
                value=children_id,
            )

            return children_id

        elif parent_id is not None and children_id is not None and verification_status == False:
            children_id = self.request_created_activity_children(
                parent_id=parent_id, opening_reason=opening_reason, checklist=checklist
            )

            self.segurpro_repository.update(
                column="id_children",
                id=parent_id,
                value=children_id,
            )

            return children_id
        
        elif parent_id is not None and children_id is None and validate_status == False:
            children_id = self.request_created_activity_children(
                parent_id=parent_id, opening_reason=opening_reason, checklist=checklist
            )

            self.segurpro_repository.update(
                column="id_children",
                id=parent_id,
                value=children_id,
            )

            return children_id

        return False

    @log_wrapper
    def edit_activity_children(
        self,
        children_id,
        checklist,
        opening_reason,
        verification_status,
        validate_status,
        parent_id,
    ):

        if children_id is not None and verification_status:
            self.request_edit_activity_children(
                id_children=children_id,
                checklist=checklist,
                # opening_reason=opening_reason,
                opening_reason="Testando pausada",
            )

            return True

        if parent_id is not None and children_id is None and validate_status is False:
            self.request_edit_activity(
                id=parent_id,
            )

            return True

        return False

    @log_wrapper
    def created_activity(
        self,
        opening_reason,
        rov,
        checklist,
        site_name,
        parent_id,
        children_id,
        status,
        system,
        triage,
    ):

        activity_id = self.request_created_activity(
            opening_reason, rov, checklist, site_name
        )

        status_btime_api = self.request_status_activity(id_activity=activity_id)

        self.segurpro_repository.insert(
            id_activity=activity_id,
            rov=rov,
            id_children=children_id,
            status_mse=status,
            site_name=site_name,
            system=system,
            opening_reason=opening_reason,
            status_btime=status_btime_api,
            triage=triage,
        )

        return activity_id

    @log_wrapper
    def handle_process_activity(
        self,
        parent_id,
        children_id,
        checklist,
        opening_reason,
        verification_status,
        rov,
        status,
        site_name,
        system,
        triage,
        validate_status,
    ):

        created_activity_children = self.created_activity_children(
            parent_id=parent_id,
            children_id=children_id,
            opening_reason=opening_reason,
            checklist=checklist,
            rov=rov,
            verification_status=verification_status,
            validate_status=validate_status,
        )

        edit_activity_children = self.edit_activity_children(
            children_id=children_id,
            checklist=checklist,
            opening_reason=opening_reason,
            verification_status=verification_status,
            validate_status=validate_status,
            parent_id=parent_id,
        )

        if not created_activity_children and not edit_activity_children:
            if validate_status:
                self.created_activity(
                    opening_reason=opening_reason,
                    rov=rov,
                    checklist=checklist,
                    site_name=site_name,
                    parent_id=parent_id,
                    children_id=children_id,
                    status=status,
                    system=system,
                    triage=triage,
                )
            else:
                self.edit_activity_children(
                    children_id=parent_id,
                    checklist=checklist,
                    opening_reason=opening_reason,
                    verification_status=verification_status,
                    validate_status=validate_status,
                    parent_id=parent_id,
                )

    @log_wrapper
    def handle_process(self):
        try:
            data = self.filter_data(self.data)
            for item in data:
                # variables
                rov = item.get("ROV")
                opening_reason = item.get("MOTIVO_ABERTURA")
                status = item.get("STATUS")
                site_name = item.get("NOME_SITE")
                system = item.get("SISTEMA")

                # validate if exists in database
                children_id = self.match_id_children(rov)
                parent_id = self.match_id_activity(rov)
                status_btime_api = self.request_status_activity(id_activity=parent_id)
                status_btime_db = self.match_status_activity(rov)

                # Request return status
                verification_status = self.request_get_status(parent_id)
                validate_status = self.validate_status(
                    status_btime_api=status_btime_api,
                    status_btime_db=status_btime_db,
                )

                # validate
                is_triage = self.verify_triage(item)
                checklist = self.verify_checklist(item, triage=is_triage)

                self.handle_process_activity(
                    parent_id=parent_id,
                    children_id=children_id,
                    checklist=checklist,
                    opening_reason=opening_reason,
                    verification_status=verification_status,
                    rov=rov,
                    status=status,
                    site_name=site_name,
                    system=system,
                    triage=is_triage,
                    validate_status=validate_status,
                )
        except Exception as ex:
            print(ex.__traceback__.tb_lineno)
            raise ex
            self.log.exception(ex)

    def run(self):
        self.handle_process()
