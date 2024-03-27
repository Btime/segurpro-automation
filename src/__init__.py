import concurrent.futures
from src.controller.activity_data_controller import ActivityDataController
from src.controller.fetch_data_controller import FetchData

def run(num_threads=10):
    handle_fetch_data = FetchData()
    data = handle_fetch_data.fetch_data()

    data_split = [data[i::num_threads] for i in range(num_threads)]

    # for i in range(num_threads):
    #     print(len(data_split[i]))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for split in data_split:
            handle_activity_data_controller = ActivityDataController(data=split)
            futures.append(executor.submit(handle_activity_data_controller.run))