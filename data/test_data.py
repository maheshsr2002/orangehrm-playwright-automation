"""
Centralized Test Data Module for Form Text Box Inputs.
Fetches all required data (names, IDs, dates, passwords, notes) from data/payloads/form_inputs.json.
Import and call wherever needed in tests and step definitions.
"""
from data.data_loader import DataLoader

# Primary form data container
FORM_DATA = DataLoader.get_form_inputs()

# Module-specific shortcuts
EMPLOYEE_DATA = FORM_DATA.get("employee", {})
ADMIN_DATA = FORM_DATA.get("admin", {})
LEAVE_DATA = FORM_DATA.get("leave", {})
TIME_DATA = FORM_DATA.get("time", {})
RECRUITMENT_DATA = FORM_DATA.get("recruitment", {})
BUZZ_DATA = FORM_DATA.get("buzz", {})
AUTH_INVALID_DATA = FORM_DATA.get("auth_invalid", {})
KNOWN_DEFECTS_DATA = FORM_DATA.get("known_defects", {})
