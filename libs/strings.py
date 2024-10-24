import re
import random
import pytz
from typing import Optional
from libs.times import datetime_from_str

def is_email_address(email: str) -> Optional[str]:
    pattern = r'^[\w\.-]+@[a-zA-Z\d]+\.[a-zA-Z]{2,}$'
    if bool(re.match(pattern, email)):
        return email.strip()

def shuffle_texts(*texts: str, seed=42) -> str:
    random.seed(seed)
    combined_texts = ''.join(texts)
    return ''.join(random.sample(combined_texts, len(combined_texts)))

def format_message_history(str_checktime: str, checktype: str, location_coordinate: str, location_name: str) -> str:
    check_time = datetime_from_str(str_checktime, pytz.timezone('Asia/Jakarta'))
    check_type = 'Clock-in' if checktype == 'checkin' else 'Clock-out'
    return f'### ⏰ {check_type} [{check_time.strftime("%d-%m-%Y %H:%M")} WIB]\nCoordinate: **{location_coordinate}**\nLocation: **{location_name}**\n\n'