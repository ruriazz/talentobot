import contextlib
from enum import Enum
from typing import Optional

class TalentaAuthStep(Enum):
    INIT            = 0
    USERNAME        = 1
    PASSWORD        = 2
    AUTHENTICATED   = 3

    @staticmethod
    def from_value(val: int) -> Optional["TalentaAuthStep"]:
        with contextlib.suppress(Exception):
            return TalentaAuthStep(val)
        
class Activity(Enum):
    AUTH_INPUT_USERNAME = 0
    AUTH_INPUT_PASSWORD = 1