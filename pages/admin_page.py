from playwright.sync_api import Page
from pages.base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.username_search_input = page.locator("div.oxd-input-group:has(label:has-text('Username')) input")
        self.user_role_dropdown = page.locator("div.oxd-input-group:has(label:has-text('User Role')) .oxd-select-wrapper")
        self.status_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Status')) .oxd-select-wrapper")
        self.search_button = page.locator("button[type='submit']")
        self.reset_button = page.locator("button[type='reset'], button:has-text('Reset')")
        self.add_button = page.locator("button:has-text('Add')")
        self.records_found_span = page.locator(".orangehrm-horizontal-padding span")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-card")
        self.username_cells = page.locator(".oxd-table-body .oxd-table-card div[role='cell']:nth-child(2)")

        # CRUD Form Locators
        self.employee_name_input = page.locator("div.oxd-input-group:has(label:has-text('Employee Name')) input")
        self.autocomplete_option = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option")
        self.password_input = page.locator("div.oxd-input-group:has(label:text-is('Password')) input, div.oxd-form-row input[type='password']").first
        self.confirm_password_input = page.locator("div.oxd-input-group:has(label:text-is('Confirm Password')) input, div.oxd-form-row input[type='password']").nth(1)
        self.save_user_button = page.locator("button[type='submit']")
        self.edit_user_button = page.locator(".oxd-table-cell-actions button:has(i.bi-pencil-fill)").first
        self.delete_user_button = page.locator(".oxd-table-cell-actions button:has(i.bi-trash)").first
        self.confirm_delete_button = page.locator("button:has-text('Yes, Delete')")
        self.toast_success = page.locator(".oxd-toast--success, .oxd-toast")
        self.toast_error = page.locator(".oxd-toast--error, .oxd-toast")

        # Qualifications
        self.qualifications_nav = page.locator("span.oxd-topbar-body-nav-tab-item:has-text('Qualifications')")
        self.education_menu = page.locator("a.oxd-topbar-body-nav-tab-link:has-text('Education')")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_admin(self):
        self.navigate_to("/web/index.php/admin/viewSystemUsers")

    def enter_search_username(self, username: str):
        self.username_search_input.fill(username)

    def select_role(self, role_name: str):
        self.user_role_dropdown.click()
        self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{role_name}')").first.click()
        self.wait_for_page_ready()

    def select_status(self, status: str):
        self.status_dropdown.click()
        self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{status}')").first.click()
        self.wait_for_page_ready()

    def click_search(self):
        try:
            with self.page.expect_response(lambda r: "admin/users" in r.url, timeout=10000):
                self.search_button.click()
        except Exception:
            self.search_button.click()
        self.wait_for_page_ready()

    def search_user(self, username: str):
        self.enter_search_username(username)
        self.click_search()
        try:
            self.page.wait_for_function(
                """([expected]) => {
                    const cell = document.querySelector(".oxd-table-body .oxd-table-card div[role='cell']:nth-child(2)");
                    return cell && cell.textContent.trim().toLowerCase().includes(expected.toLowerCase());
                }""",
                arg=[username],
                timeout=8000
            )
        except Exception:
            try:
                self.page.locator(f".oxd-table-body .oxd-table-card div[role='cell']:nth-child(2):has-text('{username}')").first.wait_for(state="visible", timeout=3000)
            except Exception:
                pass

    def filter_by_role(self, role_name: str):
        self.select_role(role_name)
        self.click_search()

    def filter_by_status(self, status: str):
        self.select_status(status)
        self.click_search()

    def click_reset(self):
        self.reset_button.click()
        self.wait_for_page_ready()

    def reset_filters(self):
        self.click_reset()

    def click_add_user(self):
        self.add_button.click()
        self.wait_for_page_ready()

    def fill_new_user_form(self, role: str, employee_hint: str, status: str, username: str, password: str):
        self.select_role(role)
        self.select_status(status)
        self.employee_name_input.fill(employee_hint)
        try:
            self.autocomplete_option.first.wait_for(state="visible", timeout=5000)
            self.autocomplete_option.first.click()
        except Exception:
            pass
        self.username_search_input.fill(username)
        self.password_input.fill(password)
        self.confirm_password_input.fill(password)

    def save_new_user(self):
        self.save_user_button.click()
        self.wait_for_page_ready()

    def click_edit_first_user(self):
        self.edit_user_button.click()
        self.wait_for_page_ready()

    def click_delete_first_user(self):
        self.delete_user_button.click()
        self.confirm_delete_button.wait_for(state="visible", timeout=5000)
        self.confirm_delete_button.click()
        self.wait_for_page_ready()

    def get_records_summary_text(self) -> str:
        try:
            return self.records_found_span.first.inner_text().strip()
        except Exception:
            return ""

    def get_records_text(self) -> str:
        return self.get_records_summary_text()

    def get_total_records_count(self) -> int:
        return self.table_rows.count()

    def get_first_row_username(self) -> str:
        try:
            return self.username_cells.first.inner_text().strip()
        except Exception:
            return ""

    def navigate_to_education(self):
        try:
            self.qualifications_nav.click()
            self.education_menu.click()
            self.wait_for_page_ready()
        except Exception:
            self.navigate_to("/web/index.php/admin/viewEducation")

    def delete_first_education_record(self):
        try:
            self.delete_user_button.click()
            self.confirm_delete_button.click()
            self.wait_for_page_ready()
        except Exception:
            pass

    def get_toast_error(self) -> str:
        try:
            self.toast_error.first.wait_for(state="visible", timeout=6000)
            return self.toast_error.first.inner_text().strip()
        except Exception:
            return ""
