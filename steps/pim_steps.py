from pages.pim_page import PIMPage
from data.models import EmployeePayload


class PIMSteps:
    """
    Step Definitions / Test Logic Layer: PIM Employee Management.
    Chains onboarding wizard and directory search flows.
    Contains NO final assertions.
    """

    def __init__(self, pim_page: PIMPage):
        self.pim_page = pim_page

    def onboard_employee(self, employee: EmployeePayload) -> dict:
        """Chains navigation to Add Employee, form filling, and submission."""
        self.pim_page.navigate_to_pim()
        self.pim_page.click_add_employee_tab()
        self.pim_page.enter_first_name(employee.firstName)
        if employee.middleName:
            self.pim_page.enter_middle_name(employee.middleName)
        self.pim_page.enter_last_name(employee.lastName)
        if employee.employeeId:
            self.pim_page.enter_employee_id(employee.employeeId)

        self.pim_page.click_save()

        return {
            "is_personal_details_displayed": self.pim_page.is_personal_details_displayed(),
            "employee_id": employee.employeeId,
            "employee_name": f"{employee.firstName} {employee.lastName}"
        }

    def onboard_employee_with_credentials(self, employee: EmployeePayload, username: str, password: str) -> dict:
        """Onboards an employee and creates login credentials."""
        self.pim_page.navigate_to_pim()
        self.pim_page.click_add_employee_tab()
        self.pim_page.enter_first_name(employee.firstName)
        self.pim_page.enter_last_name(employee.lastName)
        if employee.employeeId:
            self.pim_page.enter_employee_id(employee.employeeId)
        self.pim_page.toggle_create_login_details(username, password)
        self.pim_page.click_save()

        return {
            "is_personal_details_displayed": self.pim_page.is_personal_details_displayed(),
            "employee_id": employee.employeeId
        }

    def search_employee_directory(self, keyword: str) -> dict:
        """Navigates to employee list, executes search, and returns matches."""
        self.pim_page.navigate_to_pim()
        self.pim_page.click_employee_list_tab()
        self.pim_page.enter_search_name(keyword)
        self.pim_page.click_search()

        return {
            "records_text": self.pim_page.get_records_text(),
            "rows_count": self.pim_page.get_employee_rows_count()
        }

    def search_by_id(self, emp_id: str) -> dict:
        """Searches directory by employee ID."""
        self.pim_page.navigate_to_pim()
        self.pim_page.click_employee_list_tab()
        self.pim_page.enter_search_id(emp_id)
        self.pim_page.click_search()

        return {
            "records_text": self.pim_page.get_records_text(),
            "rows_count": self.pim_page.get_employee_rows_count()
        }

    def update_personal_details(self, other_id: str, marital_status: str = "Single") -> dict:
        """Navigates to an employee's personal details, updates sensitive fields, and returns retained state."""
        self.pim_page.navigate_to_pim()
        self.pim_page.click_edit_first_employee()
        self.pim_page.update_personal_sensitive_details(other_id=other_id, marital_status=marital_status)

        return {
            "retained_id": self.pim_page.get_other_id_value(),
            "submitted_id": other_id
        }
