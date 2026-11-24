import json
import time
import random
import string
from pathlib import Path
from data.config import Config
from data.models import (
    UserCredentials,
    NegativeLoginCase,
    EmployeePayload,
    CandidatePayload,
    BuzzAnnouncementPayload,
    ExpectedMessages,
)


def load_payload_document(file_name: str) -> dict | list:
    """Loads a raw JSON document from the data/payloads directory."""
    target_path = Config.PAYLOADS_DIR / file_name
    if not target_path.exists():
        raise FileNotFoundError(f"Test data document not found: {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        return json.load(f)


class DataLoader:
    """
    Central Data Access Layer.
    Fetches all credentials, negative scenarios, employee payloads,
    and expected messages from their dedicated JSON documents.
    """

    @staticmethod
    def get_valid_credentials() -> UserCredentials:
        """Fetches valid confidential credentials from .env via Config."""
        Config.validate()
        return UserCredentials(
            username=Config.ADMIN_USERNAME,
            password=Config.ADMIN_PASSWORD
        )

    @staticmethod
    def get_negative_login_cases() -> list[NegativeLoginCase]:
        """Fetches negative login scenarios from data/payloads/users.json."""
        raw_data = load_payload_document("users.json")
        cases = []
        for item in raw_data.get("negative_login_cases", []):
            username = Config.ADMIN_USERNAME if item.get("username_env_ref") else item.get("username", "")
            password = Config.ADMIN_PASSWORD if item.get("password_env_ref") else item.get("password", "")
            cases.append(NegativeLoginCase(
                case_id=item["case_id"],
                description=item["description"],
                username=username,
                password=password,
                expected_error=item["expected_error"],
                error_type=item["error_type"],
                target_field=item.get("target_field")
            ))
        return cases

    @staticmethod
    def get_system_user_search_data() -> dict:
        """Fetches system user search query data from users.json."""
        raw_data = load_payload_document("users.json")
        return raw_data.get("system_user_search", {})

    @staticmethod
    def get_employee_samples() -> list[EmployeePayload]:
        """Fetches employee onboarding samples from data/payloads/employees.json."""
        raw_data = load_payload_document("employees.json")
        return [EmployeePayload(**item) for item in raw_data.get("onboarding_samples", [])]

    @staticmethod
    def get_profile_update_data() -> dict:
        """Fetches personal details profile update data from employees.json."""
        raw_data = load_payload_document("employees.json")
        return raw_data.get("profile_update_sample", {})

    @staticmethod
    def get_candidate_samples() -> list[CandidatePayload]:
        """Fetches candidate samples from data/payloads/candidates.json."""
        raw_data = load_payload_document("candidates.json")
        return [CandidatePayload(**item) for item in raw_data.get("recruitment_candidates", [])]

    @staticmethod
    def get_buzz_announcements() -> list[BuzzAnnouncementPayload]:
        """Fetches buzz announcements from data/payloads/buzz_posts.json."""
        raw_data = load_payload_document("buzz_posts.json")
        return [BuzzAnnouncementPayload(**item) for item in raw_data.get("announcements", [])]

    @staticmethod
    def get_navigation_search_samples() -> list[dict]:
        """Fetches sidebar menu search samples from data/payloads/navigation.json."""
        raw_data = load_payload_document("navigation.json")
        return raw_data.get("search_filter_samples", [])

    @staticmethod
    def get_expected_messages() -> ExpectedMessages:
        """Fetches expected validation and alert messages from data/payloads/expected_messages.json."""
        raw_data = load_payload_document("expected_messages.json")
        alerts = raw_data.get("alerts", {})
        titles = raw_data.get("titles", {})
        roles = raw_data.get("roles", {})
        return ExpectedMessages(
            invalid_credentials=alerts.get("invalid_credentials", "Invalid credentials"),
            required_field=alerts.get("required_field", "Required"),
            successfully_saved=alerts.get("successfully_saved", "Successfully Saved"),
            dashboard_breadcrumb=titles.get("dashboard_breadcrumb", "Dashboard"),
            reset_password=titles.get("reset_password", "Reset Password"),
            admin_role=roles.get("admin", "Admin"),
            ess_role=roles.get("ess", "ESS")
        )

    @staticmethod
    def get_form_inputs() -> dict:
        """Fetches common form text box inputs from data/payloads/form_inputs.json."""
        return load_payload_document("form_inputs.json")

    @staticmethod
    def get_known_defects_data() -> dict:
        """Fetches known defect test cases & edge case data from form_inputs.json."""
        form_data = load_payload_document("form_inputs.json")
        return form_data.get("known_defects", {})

    # Dynamic payload generator for unique runs
    @staticmethod
    def generate_unique_employee() -> EmployeePayload:
        suffix = "".join(random.choices(string.ascii_uppercase, k=4))
        emp_id = str(int(time.time()))[-6:]
        return EmployeePayload(
            firstName=f"Auto{suffix}",
            lastName=f"Test{suffix}",
            middleName="M",
            employeeId=emp_id
        )

    @staticmethod
    def generate_unique_candidate() -> CandidatePayload:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
        timestamp = int(time.time())
        return CandidatePayload(
            firstName=f"Cand{suffix.capitalize()}",
            lastName="Lead",
            email=f"candidate_{timestamp}_{suffix}@example.com",
            contactNumber="+1-555-019-2831",
            vacancy="Senior QA Lead"
        )

    @staticmethod
    def generate_unique_buzz_post() -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        run_id = random.randint(1000, 9999)
        return f"Automation Quality Verification completed successfully at {timestamp} [RunID: {run_id}]"
