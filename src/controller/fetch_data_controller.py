import requests
from typing import Dict, Union
from src.utils.logs import Log, log_wrapper

logger = Log()


class FetchData:

    def fetch_data(self) -> list[Dict[str, Union[str, int]]]:
            try:
                url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

                response = requests.get(url)

                if response.ok:
                    data = response.json()
                    return data
                
            except Exception as ex:
                logger.exception(
                    status=response.status_code,
                    error=ex
                )
