from concurrent.futures import ThreadPoolExecutor
from src.controller.created_activity_controller import CreateActivityBtime
from src.controller.created_activity_children_controller import CreatedActivityChildren
from src.controller.fetch_data_controller import FetchData

def run():
    handle_fetch_data = FetchData()
    data = handle_fetch_data.fetch_data()

    handle_created_activity = CreateActivityBtime(data=data)
    handle_created_activity_children = CreatedActivityChildren(data=data)

    handle_created_activity.run()

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit(handle_created_activity_children.run)
        # executor.submit(handle_created_activity.run)