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

                if response.ok:
                    data = response.json()
                    
                    return data
                else:
                    raise 'Erro ao coletar dados'
                
            except Exception as e:
                raise e