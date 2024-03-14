from src.controller.created_activity_controller import CreateActivityBtime
from src.controller.created_activity_children_controller import CreatedActivityChildren
from src.controller.fetch_data_controller import FetchData
import threading
import json
from src.controller.status_validation_controller import StatusValidation

# def run(): # testes
#     handle_update = StatusValidation()
#     handle_update.run()

def run():
    handle_fetch_data = FetchData()
    data = handle_fetch_data.fetch_data()
    handle_created_activity = CreateActivityBtime(data=data)
    handle_created_activity_children = CreatedActivityChildren(data=data)
    threads = []
    for _ in range(1):
        thread = threading.Thread(target=handle_created_activity.run)
        threads.append(thread)
        thread.start()

    for _ in range(1):
        thread = threading.Thread(target=handle_created_activity_children.run)
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()

# def thread_function(data_chunk):
#     handle_created_activity = CreateActivityBtime(data=data_chunk)
#     handle_created_activity_children = CreatedActivityChildren(data=data_chunk)
    
#     handle_created_activity.run()
#     handle_created_activity_children.run()

# def run():
#     handle_fetch_data = FetchData()
#     data = handle_fetch_data.fetch_data()
#     data_chunks = divide_data(data, 4)
#     threads = []
#     for chunk in data_chunks:
#         thread = threading.Thread(target=thread_function, args=(chunk,))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()


# def divide_data(data, num_parts):
#     data_list = json.loads(data)
#     chunk_size = len(data_list) // num_parts
#     data_chunks = [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]
    
#     if len(data_list) % num_parts != 0:
#         data_chunks[-1].extend(data_list[chunk_size * num_parts:])
    
#     return data_chunks