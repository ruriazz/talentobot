import pytz
from typing import Optional
from datetime import datetime


indonesia_tz = pytz.timezone('Asia/Jakarta')
def is_weekday_in_indonesia() -> bool:
    now_in_indonesia = datetime.now(indonesia_tz)
    return now_in_indonesia.weekday() < 5

def datetime_from_str(date_string: str, tz=pytz.UTC) -> Optional[datetime]:
    possible_formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
    ]

    for date_format in possible_formats:
        try:
            parsed_datetime = (datetime
                               .strptime(date_string, date_format)
                               .replace(tzinfo=pytz.UTC))
            return parsed_datetime.astimezone(tz)
        except ValueError:
            continue