import requests
from typing import Dict, Union
from src.utils.logs import Log, log_wrapper

logger = Log()


class FetchData:

    @log_wrapper
    def fetch_data(self) -> list[Dict[str, Union[str, int]]]:
            try:
                url = 'https://us-central1-mse-digital.cloudfunctions.net/relatorioChamados'

                response = requests.get(url)

                if response.ok:
                    logger.info(
                        status=response.status_code,
                        response=response.headers,
                        body=response.json()[0]
                    )
                    data = response.json()
                    return data
                
            except Exception as ex:
                logger.exception(
                    status=response.status_code,
                    error=ex
                )
