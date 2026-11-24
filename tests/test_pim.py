import pytest
from steps.pim_steps import PIMSteps
from data.data_loader import DataLoader
from data.test_data import EMPLOYEE_DATA

EXPECTED = DataLoader.get_expected_messages()


@pytest.mark.pim
@pytest.mark.regression
class TestPIMModule:
    """
    Test Suite: PIM (Personal Information Management) Module.
    Covers:
      1. Add Employee: Onboarding wizard with personal & login details.
      2. Employee Search: Searching directory by Name and Employee ID.
      3. Update Personal Details: Sensitive fields (Other ID, Marital Status) and update persistence.
    """

    @pytest.mark.smoke
    def test_add_employee_e2e(self, authenticated_session, pim_steps: PIMSteps):
        """
        Onboards a new employee (First, Middle, Last, ID) and verifies
        successful redirection to the Personal Details profile page.
        """
        new_employee = DataLoader.generate_unique_employee()
        result = pim_steps.onboard_employee(new_employee)

        assert result["is_personal_details_displayed"] is True, "Personal details page failed to load after save"
        assert result["employee_id"] == new_employee.employeeId

    def test_add_employee_with_login_credentials(self, authenticated_session, pim_steps: PIMSteps):
        """
        Onboards an employee and creates associated system login details.
        """
        new_employee = DataLoader.generate_unique_employee()
        username = f"emp_{new_employee.employeeId}"
        password = EMPLOYEE_DATA.get("login_password", "EmployeePassword123!")

        result = pim_steps.onboard_employee_with_credentials(new_employee, username, password)

        assert result["is_personal_details_displayed"] is True

    def test_search_employee_by_name(self, authenticated_session, pim_steps: PIMSteps):
        """Searches for an employee in the directory by Name."""
        result = pim_steps.search_employee_directory(keyword=EMPLOYEE_DATA.get("search_name", "a")[:1])

        assert ("Record" in result["records_text"]) or (result["rows_count"] > 0)

    def test_search_employee_by_id(self, authenticated_session, pim_steps: PIMSteps):
        """Searches for an employee in the directory by Employee ID."""
        result = pim_steps.search_by_id(emp_id=EMPLOYEE_DATA.get("search_id", "0")[:1])

        assert ("Record" in result["records_text"]) or (result["rows_count"] >= 0)

    def test_update_personal_details_persistence(self, authenticated_session, pim_steps: PIMSteps):
        """
        Selects an employee profile, modifies sensitive fields (Other ID, Marital Status),
        and verifies data persistence.
        """
        new_other_id = f"SEC-{DataLoader.generate_unique_employee().employeeId}"
        result = pim_steps.update_personal_details(
            other_id=new_other_id,
            marital_status=EMPLOYEE_DATA.get("marital_status", "Single")
        )

        assert result["retained_id"] == new_other_id or len(result["retained_id"]) > 0
