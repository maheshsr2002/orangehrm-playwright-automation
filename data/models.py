from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

try:
    from pydantic import BaseModel
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


@dataclass
class UserCredentials:
    username: str
    password: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class NegativeLoginCase:
    case_id: str
    description: str
    username: str
    password: str
    expected_error: str
    error_type: str
    target_field: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EmployeePayload:
    firstName: str
    lastName: str
    middleName: str = ""
    employeeId: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CandidatePayload:
    firstName: str
    lastName: str
    email: str
    middleName: str = ""
    contactNumber: str = ""
    vacancy: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BuzzAnnouncementPayload:
    topic: str
    template: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FormInputs:
    employee: dict
    admin: dict
    leave: dict
    time: dict
    recruitment: dict
    buzz: dict
    auth_invalid: dict
    known_defects: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExpectedMessages:
    invalid_credentials: str
    required_field: str
    successfully_saved: str
    dashboard_breadcrumb: str
    reset_password: str
    admin_role: str
    ess_role: str

    def to_dict(self) -> dict:
        return asdict(self)
