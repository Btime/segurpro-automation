import logging
import os
from datetime import datetime
from time import perf_counter
    
class Log:
    def __init__(self):
        if not os.path.exists("./_logs/"):
            os.makedirs("./_logs/")

        self.timestamp = "{:%Y_%m_%d}".format(datetime.now())
        self.filename = './_logs/Log_{}.log'.format(self.timestamp)
        logging.basicConfig(filename=self.filename, filemode="a", level=logging.ERROR,
                            format='%(asctime)s: %(levelname)s: %(message)s')
        logging.getLogger("selenium").setLevel(logging.CRITICAL)
        logging.getLogger("selenium").propagate = False
        logging.getLogger("requests").setLevel(logging.CRITICAL)
        logging.getLogger("requests").propagate = False

        logging.getLogger("requests.packages.urllib3").setLevel(logging.CRITICAL)
        logging.getLogger("requests.packages.urllib3").propagate = False

        logging.getLogger("urllib3").setLevel(logging.CRITICAL)
        logging.getLogger("urllib3").propagate = False

        self.logger = logging.getLogger(__name__)
        
    def exception(self, **kwargs):
        message = dict()
        for k, v in zip(kwargs.keys(), kwargs.values()):
            message[k] = v

        with open(self.filename, 'a') as f:
            f.write(f'{message}\n')

    def info(self,**kwargs):
        message = dict()
        for k, v in zip(kwargs.keys(), kwargs.values()):
            v = 'Executada com sucesso ' + v if k == 'descricao' else v
            message[k] = v

        with open(self.filename, 'a') as f:
            f.write(f'{message}\n')

def log_wrapper(func):
    def wrapper(*args, **kwargs):
        instance_name = args[0].__class__.__name__
        method_name = func.__name__

        try:
            t1_start = perf_counter()
            logging.info(f"Starting {method_name} in {instance_name}")
            result = func(*args, **kwargs)
            t1_stop = perf_counter()
            logging.info(f"{method_name} completed successfully in {round(t1_stop-t1_start)} seconds")
            return result
        except Exception as ex:
            raise ex
    return wrapper