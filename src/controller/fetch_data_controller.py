import requests
from typing import Dict, Union
from src.model.table_json_segurpro import create_table, table_exist



class FetchData:
    def fetch_data(self) -> list[Dict[str, Union[str, int]]]:
            try:
                url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

                if not table_exist():
                    create_table()

                response = requests.get(url)

                # self.excel.create_excel()

                if response.ok:
                    dados = response.json()

                    response = list(
                        filter(
                            lambda dado: dado.get('STATUS').startswith('EM ABERTO') and not dado.get('STATUS').startswith('EM ABERTO - RETORNO TECNICO'), dados
                        )
                    )
                    return response
                else:
                    raise 'Erro ao coletar dados'
                
            except Exception as e:
                raise e