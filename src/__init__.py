import concurrent.futures
from src.controller.activity_data_controller import ActivityDataController
from src.controller.fetch_data_controller import FetchData

def run(num_threads=3):
    handle_fetch_data = FetchData()
    data = handle_fetch_data.fetch_data()

    data_split = [data[i::num_threads] for i in range(num_threads)]

    # for i in range(num_threads):
    #     print(len(data_split[i]))

    # all_rov_values = []
    # repeated_rovs = set()
    # for split in data_split:
    #     rov_set = set()
    #     for item in split:
    #         if 'ROV' in item:
    #             rov = item['ROV']
    #             if rov in rov_set:
    #                 repeated_rovs.add(rov)
    #             else:
    #                 rov_set.add(rov)
    #     all_rov_values.extend(rov_set)

    # if len(repeated_rovs) == 0:
    #     print("Não há repetições de 'ROV' em todos os threads.")
    # else:
    #     print("ROVs repetidos em todos os threads:")
    #     for rov in repeated_rovs:
    #         print(rov)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for split in data_split:
            handle_activity_data_controller = ActivityDataController(data=split)
            futures.append(executor.submit(handle_activity_data_controller.run))


# -import threading
# -from src.controller.activity_data_controller import ActivityDataController
# -from src.controller.fetch_data_controller import FetchData
# -
# -def run():
# -    handle_fetch_data = FetchData()
# -    data = handle_fetch_data.fetch_data()
# -    handle_activity_data_controller = ActivityDataController(data=data)
# -
# -    threads = []
# -
# -    for _ in range(1):
# -        thread = threading.Thread(target=handle_activity_data_controller.run)
# -        threads.append(thread)
# -        thread.start()
# -
# -    for thread in threads:
# -        thread.join()
