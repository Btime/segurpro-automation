from datetime import datetime, timezone, timedelta

def datetime_brasilia_format():
    brasilia_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=0)))
    return brasilia_time.strftime("%Y-%m-%dT%H:%M:%SZ")