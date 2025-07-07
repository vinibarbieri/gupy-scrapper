from dataclasses import dataclass
from typing import List


@dataclass
class Profile:
    name: str
    cpf: str
    email: str
    phone: str
    education: str
    experience: str
    resume_path: str  # caminho do PDF
