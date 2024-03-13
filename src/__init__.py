from src.controller.created_activity_controller import CreateActivityBtime
from src.controller.created_activity_children_controller import CreatedActivityChildren
from src.controller.fetch_data_controller import FetchData

handle_fetch_data = FetchData()


def run():
    data = handle_fetch_data.fetch_data()
    handle_created_activity = CreateActivityBtime(data=data)
    handle_created_activity_children = CreatedActivityChildren(data=data)


    handle_created_activity_children.run()
    handle_created_activity.run()