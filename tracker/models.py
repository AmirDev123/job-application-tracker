"""Domain model for a job application."""
from dataclasses import dataclass, field
from datetime import date
from typing import Literal

STATUS = Literal["applied", "phone_screen", "interview", "offer", "rejected", "withdrawn"]


@dataclass
class JobApplication:
    company: str
    role: str
    status: STATUS = "applied"
    applied_date: str = field(default_factory=lambda: date.today().isoformat())
    url: str = ""
    notes: str = ""
    id: int | None = None

    def is_active(self) -> bool:
        return self.status not in ("rejected", "withdrawn")
