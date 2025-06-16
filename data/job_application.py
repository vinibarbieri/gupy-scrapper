from dataclasses import dataclass
from datetime import datetime


@dataclass
class JobApplication:
    company: str
    job_title: str
    job_url: str
    date_applied: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
