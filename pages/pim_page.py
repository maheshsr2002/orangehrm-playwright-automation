from playwright.sync_api import Page
from pages.base_page import BasePage


class PIMPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.add_employee_tab = page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Add Employee')")
        self.employee_list_tab = page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Employee List')")
        self.first_name_input = page.locator("input[name='firstName']")
        self.middle_name_input = page.locator("input[name='middleName']")
        self.last_name_input = page.locator("input[name='lastName']")
        self.employee_id_input = page.locator("div.oxd-input-group:has(label:has-text('Employee Id')) input")
        self.save_button = page.locator("button[type='submit']")

        # Create Login Details Toggle & Fields
        self.create_login_details_toggle = page.locator(".oxd-switch-input")
        self.login_username_input = page.locator("div.oxd-input-group:has(label:has-text('Username')) input")
        self.login_password_input = page.locator("div.oxd-input-group:has(label:text-is('Password')) input, div.oxd-form-row input[type='password']").first
        self.login_confirm_password_input = page.locator("div.oxd-input-group:has(label:text-is('Confirm Password')) input, div.oxd-form-row input[type='password']").nth(1)

        # Search Filters
        self.search_employee_name = page.locator("div.oxd-input-group:has(label:has-text('Employee Name')) input")
        self.search_employee_id = page.locator("div.oxd-input-group:has(label:has-text('Employee Id')) input")
        self.search_button = page.locator("button[type='submit']")
        self.reset_button = page.locator("button:has-text('Reset')")
        self.records_found_span = page.locator(".orangehrm-horizontal-padding span")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-card")
        self.edit_employee_button = page.locator(".oxd-table-cell-actions button:has(i.bi-pencil-fill)").first
        self.personal_details_header = page.locator("h6:has-text('Personal Details'), .orangehrm-edit-employee-name")

        # Personal Details & Sensitive Fields
        self.other_id_input = page.locator("div.oxd-input-group:has(label:has-text('Other Id')) input")
        self.marital_status_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Marital Status')) .oxd-select-wrapper")
        self.nationality_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Nationality')) .oxd-select-wrapper")
        self.save_personal_details_button = page.locator("form button[type='submit']").first

        # Job & Employment Status
        self.job_tab = page.locator("a.orangehrm-tabs-item:has-text('Job')")
        self.employment_status_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Employment Status')) .oxd-select-wrapper")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_pim(self):
        self.navigate_to("/web/index.php/pim/viewEmployeeList")

    def click_add_employee_tab(self):
        self.add_employee_tab.click()

    def go_to_add_employee(self):
        self.click_add_employee_tab()

    def click_employee_list_tab(self):
        self.employee_list_tab.click()

    def go_to_employee_list(self):
        self.click_employee_list_tab()

    def click_edit_first_employee(self):
        try:
            self.edit_employee_button.click()
            self.page.wait_for_url("**/pim/viewPersonalDetails/**", timeout=15000)
        except Exception:
            pass
        self.wait_for_page_ready()

    def enter_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)

    def enter_middle_name(self, middle_name: str):
        self.middle_name_input.fill(middle_name)

    def enter_last_name(self, last_name: str):
        self.last_name_input.fill(last_name)

    def enter_employee_id(self, employee_id: str):
        self.employee_id_input.fill(employee_id)

    def toggle_create_login_details(self, username: str, password: str):
        self.create_login_details_toggle.click()
        self.login_username_input.fill(username)
        self.login_password_input.fill(password)
        self.login_confirm_password_input.fill(password)

    def click_save(self):
        self.save_button.click()
        try:
            self.page.wait_for_url("**/viewPersonalDetails/**", timeout=20000)
        except Exception:
            pass
        self.wait_for_page_ready()

    def add_employee(self, first_name: str, last_name: str, employee_id: str = "", middle_name: str = ""):
        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)
        if employee_id:
            self.enter_employee_id(employee_id)
        self.click_save()

    def is_personal_details_displayed(self) -> bool:
        try:
            if "viewPersonalDetails" in self.page.url:
                return True
            return self.personal_details_header.first.is_visible()
        except Exception:
            return False

    def enter_search_name(self, name: str):
        self.search_employee_name.fill(name)

    def enter_search_id(self, emp_id: str):
        self.search_employee_id.fill(emp_id)

    def click_search(self):
        self.search_button.click()
        self.wait_for_page_ready()

    def search_employee_by_name(self, name: str):
        self.enter_search_name(name)
        self.click_search()

    def search_employee_by_id(self, emp_id: str):
        self.enter_search_id(emp_id)
        self.click_search()

    def update_personal_sensitive_details(self, other_id: str = None, marital_status: str = None):
        if other_id:
            self.other_id_input.fill(other_id)
        if marital_status:
            try:
                self.marital_status_dropdown.click()
                self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{marital_status}')").first.click()
            except Exception:
                pass
        self.save_personal_details_button.click()
        self.wait_for_page_ready()

    def get_other_id_value(self) -> str:
        try:
            return self.other_id_input.input_value()
        except Exception:
            return ""

    def get_records_text(self) -> str:
        try:
            return self.records_found_span.first.inner_text().strip()
        except Exception:
            return ""

    def get_employee_rows_count(self) -> int:
        return self.table_rows.count()
