import requests
from src.utils.excel_infos_json import ExcelCollector
from src.utils.chatgpt_utils import ChatGPT
from src.enum.sistema_enum import SistemaEnum
from src.config.configuration import AUTHORIZATION
from src.model.db.repository.segurpro_repository import SegurproRepository
from typing import Dict, Union
from src.utils.headers_utils import get_headers



class CreateActivityBtime:
    def __init__(self, data) -> None:
        self.data = data
        self.excel = ExcelCollector()
        self.chatGPT = ChatGPT()
        self.segurpro_repository = SegurproRepository()
        self.headers = get_headers()


    def request_insert_btime(
        self,
        motivo_abertura: str,
        rov: str,
        checklist: str,
        nome_site: str,
    ) -> int:
        json_data = {
            "operationName": "UpsertServiceOrder",
            "variables": {
                "input": {
                    "userId": 11,
                    "checklistId": checklist,
                    "placeId": 19,  # nome_site
                    "assetId": None,
                    "scheduling": "2024-03-15T19:44:00Z",
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
                    "description": self.chatGPT.prompt(motivo_abertura),
                    "documents": [],
                    "groupId": None,
                    "events": [
                        {
                            "statusId": 1,
                            "eventDate": "2024-03-11T19:44:48Z",
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

        if response.ok:
            data = response.json()

            return data["data"]["upsertServiceOrder"]["id"]

    def filter_data(self):
        data = list(
            filter(
                lambda dado: dado.get("STATUS").startswith("EM ABERTO")
                and not dado.get("STATUS").startswith("EM ABERTO - RETORNO TECNICO"),
                self.data,
            )
        )
        return data

    def verify_triage(self, data: Dict[str, Union[str, int]]):
        motivo_abertura = data.get("MOTIVO_ABERTURA")
        verificacao = bool(self.chatGPT.prompt(texto=motivo_abertura, triagem=True))
        return verificacao


    def obtain_checklist(
        self, data: Dict[str, Union[str, int]], triagem: bool = False
    ) -> int:
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
    
    def match_id_activity(self, rov):
        results = self.segurpro_repository.filter_by_rov(rov)
        results = results.id_activity if results else None
        return results

    def created_activity(self, data: Dict[str, Union[str, int]], checklist: int) -> int:
        id_activity = self.request_insert_btime(
            motivo_abertura=data.get("MOTIVO_ABERTURA"),
            rov=data.get("ROV"),
            checklist=checklist,
            nome_site=data.get("NOME_SITE"),
        )
        return id_activity

    def handle_process(self, data: Dict[str, Union[str, int]]) -> None:
        for dado in data:
            triagem = self.verify_triage(dado)
            checklist = self.obtain_checklist(dado, triagem=triagem)
            activity_id = self.created_activity(dado, checklist)
            validate_rov = self.match_id_activity(dado.get("ROV"))
            
            if validate_rov is None:
                self.created_activity(dado, checklist)

                self.segurpro_repository.insert(
                    id_activity=activity_id,
                    rov=dado.get("ROV"),
                    status=dado.get("STATUS"),
                    site_name=dado.get("NOME_SITE"),
                    system=dado.get("SISTEMA"),
                    description=dado.get("MOTIVO_ABERTURA"),
                    triage=triagem,
                )

    def run(self):
        data = self.filter_data()
        self.handle_process(data)
