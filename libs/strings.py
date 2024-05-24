import re
from typing import Optional

def is_email_address(email: str) -> Optional[str]:
    pattern = r'^[\w\.-]+@[a-zA-Z\d]+\.[a-zA-Z]{2,}$'
    if bool(re.match(pattern, email)):
        return email.strip()