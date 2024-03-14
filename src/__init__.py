from src.controller.created_activity_controller import CreateActivityBtime
from src.controller.created_activity_children_controller import CreatedActivityChildren
from src.controller.fetch_data_controller import FetchData
import threading

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