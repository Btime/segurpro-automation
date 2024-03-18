import requests
from src.utils.logs import Log
from src.utils.chatgpt_utils import ChatGPT
from src.utils.time_utc import datetime_brasilia_format
from src.utils.headers_utils import get_headers
from src.enum.sistema_enum import SistemaEnum
from src.model.db.repository.segurpro_repository import SegurproRepository
from src.config.configuration import STATUS_OPEN

class ActivityDataController:
    def __init__(self, data) -> None:
        self.data = data
        self.chatGPT = ChatGPT()
        self.segurpro_repository = SegurproRepository()
        self.log = Log()
        self.headers = get_headers()

    def filter_data(self, response):
        data = list(
            map(
                lambda data: (
                    {
                        "ROV": data.get("ROV"),
                        "SISTEMA": data.get("SISTEMA"),
                        "ENDERECO": data.get("ENDERECO"),
                        "BAIRRO": data.get("BAIRRO"),
                        "MUNICIPIO": data.get("MUNICIPIO"),
                        "MOTIVO_ABERTURA": data.get("MOTIVO_ABERTURA"),
                        "NOME_SITE": data.get("NOME_SITE"),
                        "STATUS": data.get("STATUS"),
                        "MOTIVO_REPROVA_EPS": data.get("MOTIVO_REPROVA_EPS")
                    }
                ),
                filter(
                    lambda data: data.get("STATUS").startswith("EM ABERTO"),
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

        status_id = STATUS_OPEN

        status_verified = None if data is None else True if data in status_id else False

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_status_activity.__name__}. Status da Atividade Pai validado.",
            data={response.content},
        )

        return status_verified

    def request_created_activity(
            self,
            opening_reason, 
            rov, 
            checklist, 
            site_name, 
            recused_reason, 
            address,
            neiborhood,
            municipio
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
                    "description": self.chatGPT.prompt(opening_reason, address, neiborhood, municipio, site_name) + '\n\n ## Motivo Reprova:\n\n' + recused_reason,
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

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_created_activity.__name__} . Atividade Pai criada.",
            data={response.content},
        )

        if response.ok:
            data = response.json()
            return data["data"]["upsertServiceOrder"]["id"]

    def request_created_activity_children(
            self, 
            id_activity, 
            checklist, 
            opening_reason, 
            site_name, 
            recused_reason, 
            address, 
            neiborhood, 
            municipio
        ):
        
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
                    "description":  self.chatGPT.prompt(opening_reason, address, neiborhood, municipio, site_name) + '\n\n ## Motivo Reprova:\n\n' + recused_reason,
                    "parentId": id_activity,
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

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_created_activity_children.__name__} . Atividade Filha criada.",
            data={response.content},
        )

        if response.ok:
            data = response.json()
            id_children = data["data"]["upsertServiceOrder"]["id"]
            return id_children

    def request_status_activity_children(self, id_activity):
        json_data = {
            "operationName": "ServiceOrders",
            "variables": {
                "page": 1,
                "sort": {
                    "field": "ID",
                    "type": "ASC",
                },
                "filter": {
                    "parentIds": id_activity,  # id_activity (id da atividade pai)
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

        status_id = STATUS_OPEN

        status_verified = (
            None if status is None else True if status in status_id else False
        )

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_status_activity_children.__name__}. Status da Atividade Filha validado.",
            data={response.content},
        )

        return status_verified

    def request_edit_activity(self, id, checklist, opening_reason, recused_reason, address, neiborhood, municipio, site_name):
        json_data = {
            "operationName": "UpsertServiceOrder",
            "variables": {
                "input": {
                    "id": id,
                    "name": None,
                    "userId": 11,
                    "checklistId": checklist,
                    "placeId": 18,
                    "assetId": None,
                    "scheduling": None,
                    "priorityId": 1,
                    "address": None,
                    "description": self.chatGPT.prompt(opening_reason, address, neiborhood, municipio, site_name) + '\n\n ## Motivo Reprova:\n\n' + recused_reason,
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

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_edit_activity.__name__} . Atividade Pai editada com sucesso.",
            data={response.content},
        )

        return response

    def request_edit_activity_children(self, id_children, checklist, opening_reason, recused_reason, address, neiborhood, municipio, site_name):
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
                    "description": self.chatGPT.prompt(opening_reason, address, neiborhood, municipio, site_name) + '\n\n ## Motivo Reprova:\n\n' + recused_reason,
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

        self.log.info(
            status_code=response.status_code,
            descricao=f"{self.request_edit_activity_children.__name__} . Atividade Filha editada com sucesso.",
            data={response.content},
        )

    def match_status_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        results = results.status_btime if results else None

        return results

    def match_id_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        results = results.id_activity if results else None

        return results

    def match_id_children(self, rov):
        results_children = self.segurpro_repository.filter_by_rov_children(rov)
        results_children = results_children.id_children if results_children else None
        return results_children

    def validate_status_father(self, status_btime_api: int, status_btime_db: str):
        try:
            status_btime_db = (
                int(status_btime_db) if status_btime_db.isdigit() else status_btime_db
            )
            is_valid = True if status_btime_api == status_btime_db else False
            return is_valid
        except:
            return None

    def verify_triage(self, data):
        opening_reason = data.get("MOTIVO_ABERTURA")
        verification = bool(self.chatGPT.prompt(address=data.get("ENDERECO") ,neiborhood=data.get("BAIRRO"), municipio=data.get("MUNICIPIO"),site_name=data.get("NOME_SITE") ,texto=opening_reason, triagem=True))
        return verification

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

    def created_activity(
        self,
        opening_reason,
        rov,
        checklist,
        site_name,
        id_activity,
        children_id,
        status,
        system,
        triage,
        recused_reason,
        address,
        neiborhood,
        municipio
    ):

        # Criar atividade
        activity_id = self.request_created_activity(
            opening_reason,
            rov, 
            checklist, 
            site_name, 
            recused_reason, 
            address,
            neiborhood,
            municipio
        )

        # Checar status na plataforma Btime
        status_btime_api = self.request_status_activity(id_activity=activity_id)

        # Inserir dados no banco de dados
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

    def edit_activity(
            self, 
            id_activity, 
            children_id, 
            validate_status_father, 
            checklist,
            opening_reason, 
            recused_reason,
            address,
            neiborhood,
            municipio,
            site_name):

        # Se id da atividade pai existir e a atividade filha não existir e o status da atividade pai retornar false, então edita a atividade pai existente
        if id_activity is not None and validate_status_father is True:
            self.request_edit_activity(
                id=id_activity,
                checklist=checklist,
                opening_reason=opening_reason,
                recused_reason=recused_reason,
                site_name=site_name,
                address=address,
                neiborhood=neiborhood,
                municipio=municipio
            )

            return True
        return False

    def created_activity_children(
        self,
        id_activity,
        children_id,
        opening_reason,
        checklist,
        site_name,
        rov,
        validate_status_children,
        validate_status_father,
        recused_reason,
        address,
        neiborhood,
        municipio
    ):

        # Se existir o id pai e não existir a id filha e o status da pai retornar False (fechado) então cria uma nova atividade
        if (
            id_activity is not None
            and children_id is None
            and validate_status_father is False
        ):
            children_id = self.request_created_activity_children(
                id_activity=id_activity,
                opening_reason=opening_reason,
                checklist=checklist,
                recused_reason=recused_reason,
                address=address,
                neiborhood=neiborhood,
                municipio=municipio,
                site_name=site_name
            )

            self.segurpro_repository.update(
                column="id_children",
                id=id_activity,
                value=children_id,
            )

            return children_id

        # Se existir o id pai e existir id filha e o status da filha retornar False (id 1,2 5 ou 6) cria uma nova atividade filha
        elif (
            id_activity is not None
            and children_id is not None
            and validate_status_children == False
        ):
            children_id = self.request_created_activity_children(
                id_activity=id_activity,
                opening_reason=opening_reason,
                checklist=checklist,
                recused_reason=recused_reason,
                address=address,
                neiborhood=neiborhood,
                municipio=municipio,
                site_name=site_name
            )

            self.segurpro_repository.update(
                column="id_children",
                id=id_activity,
                value=children_id,
            )

            return children_id

        return False

    def edit_activity_children(
        self,
        children_id,
        checklist,
        opening_reason,
        validate_status_children,
        validate_status_father,
        id_activity,
        recused_reason,
        address,
        neiborhood,
        municipio,
        site_name
    ):

        # Se id da atividade filha existir e o status retornar true (id 1,2 5 ou 6) então edita a atividade já existente
        if children_id is not None and validate_status_children:
            self.request_edit_activity_children(
                id_children=children_id,
                checklist=checklist,
                opening_reason=opening_reason,
                recused_reason=recused_reason,
                address=address,
                neiborhood=neiborhood,
                municipio=municipio,
                site_name=site_name
            )

            return True

        return False

    def handle_process_activity(
            self,
            id_activity,
            children_id,
            checklist,
            opening_reason,
            validate_status_children,
            rov,
            status,
            site_name,
            system,
            triage,
            validate_status_father,
            recused_reason,
            address,
            neiborhood,
            municipio
        ):

        edit_activity = self.edit_activity(
            id_activity=id_activity,
            children_id=children_id,
            validate_status_father=validate_status_father, 
            checklist=checklist,
            opening_reason=opening_reason,
            recused_reason=recused_reason,
            address=address,
            neiborhood=neiborhood,
            municipio=municipio,
            site_name=site_name
        )

        created_activity_children = self.created_activity_children(
            id_activity=id_activity,
            children_id=children_id,
            opening_reason=opening_reason,
            checklist=checklist,
            rov=rov,
            validate_status_children=validate_status_children,
            validate_status_father=validate_status_father,
            recused_reason=recused_reason,
            address=address,
            neiborhood=neiborhood,
            municipio=municipio,
            site_name=site_name
        )

        edit_activity_children = self.edit_activity_children(
            children_id=children_id,
            checklist=checklist,
            opening_reason=opening_reason,
            validate_status_children=validate_status_children,
            validate_status_father=validate_status_father,
            id_activity=id_activity,
            recused_reason=recused_reason,
            address=address,
            neiborhood=neiborhood,
            municipio=municipio,
            site_name=site_name
        )

        if (
            not created_activity_children
            and not edit_activity_children
            and not edit_activity
        ):
            if validate_status_father == None:
                self.created_activity(
                    opening_reason=opening_reason,
                    rov=rov,
                    checklist=checklist,
                    site_name=site_name,
                    id_activity=id_activity,
                    children_id=children_id,
                    status=status,
                    system=system,
                    triage=triage,
                    recused_reason=recused_reason,
                    address=address,
                    neiborhood=neiborhood,
                    municipio=municipio
                    )   
            else:
                self.edit_activity_children(
                    children_id=id_activity,
                    checklist=checklist,
                    opening_reason=opening_reason,
                    validate_status_children=validate_status_children,
                    validate_status_father=validate_status_father,
                    id_activity=id_activity,
                    recused_reason=recused_reason,
                    address=address,
                    neiborhood=neiborhood,
                    municipio=municipio,
                    site_name=site_name
                )

    def handle_process(self):
        try:
            data = self.filter_data(self.data)
            for item in data:
                # variables
                rov = item.get("ROV")
                address = item.get("ENDERECO")
                neiborhood = item.get("BAIRRO")
                municipio = item.get("MUNICIPIO")
                rov = item.get("ROV")
                opening_reason = item.get("MOTIVO_ABERTURA")
                status = item.get("STATUS")
                site_name = item.get("NOME_SITE")
                system = item.get("SISTEMA")
                recused_reason = item.get("MOTIVO_REPROVA_EPS")


                # validate if exists in database
                children_id = self.match_id_children(rov)
                id_activity = self.match_id_activity(rov)
                status_btime_api = self.request_status_activity(id_activity=id_activity)
                status_btime_db = self.match_status_activity(rov)

                # Request return status
                validate_status_children = self.request_status_activity_children(
                    id_activity
                )
                validate_status_father = self.validate_status_father(
                    status_btime_api=status_btime_api,
                    status_btime_db=status_btime_db,
                )

                # validate
                is_triage = self.verify_triage(item)
                checklist = self.verify_checklist(item, triage=is_triage)

                self.handle_process_activity(
                    id_activity=id_activity,
                    children_id=children_id,
                    checklist=checklist,
                    opening_reason=opening_reason,
                    validate_status_children=validate_status_children,
                    rov=rov,
                    status=status,
                    site_name=site_name,
                    system=system,
                    triage=is_triage,
                    validate_status_father=validate_status_father,
                    recused_reason=recused_reason,
                    address=address,
                    neiborhood=neiborhood,
                    municipio=municipio
                )
        except Exception as ex:
            print(ex.__traceback__.tb_lineno)
            self.log.exception(error=ex)
            raise ex

    def run(self):
        self.handle_process()
