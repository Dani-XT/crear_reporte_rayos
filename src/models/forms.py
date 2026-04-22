from dataclasses import dataclass

from datetime import date

@dataclass
class HomeFormData:
    start_date: date
    end_date: date