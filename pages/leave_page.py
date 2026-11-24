from playwright.sync_api import Page
from pages.base_page import BasePage


class LeavePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.apply_tab = page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Apply')")
        self.leave_list_tab = page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Leave List')")
        self.my_leave_tab = page.locator("a.oxd-topbar-body-nav-tab-item:has-text('My Leave')")
        self.search_button = page.locator("button[type='submit']")
        self.reset_button = page.locator("button:has-text('Reset')")
        self.records_found_span = page.locator(".orangehrm-horizontal-padding span")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-card")
        self.apply_leave_title = page.locator("h6:has-text('Apply'), .orangehrm-card-container")

        # Apply Leave Form Locators
        self.leave_type_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Leave Type')) .oxd-select-wrapper")
        self.from_date_input = page.locator("div.oxd-input-group:has(label:has-text('From Date')) input")
        self.to_date_input = page.locator("div.oxd-input-group:has(label:has-text('To Date')) input")
        self.comments_textarea = page.locator("div.oxd-input-group:has(label:has-text('Comments')) textarea")
        self.apply_submit_button = page.locator("button[type='submit']")

        # Action Buttons in Leave List
        self.approve_button = page.locator("button:has-text('Approve')").first
        self.reject_button = page.locator("button:has-text('Reject')").first
        self.cancel_leave_button = page.locator("button:has-text('Cancel')").first
        self.leave_balance_label = page.locator(".orangehrm-leave-balance-text, p:has-text('Day(s)'), span:has-text('Day(s)')")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_leave(self):
        self.navigate_to("/web/index.php/leave/viewLeaveList")

    def click_apply_tab(self):
        self.apply_tab.click()

    def go_to_apply_leave(self):
        self.click_apply_tab()

    def click_leave_list_tab(self):
        self.leave_list_tab.click()

    def click_search(self):
        self.search_button.click()
        self.wait_for_page_ready()

    def search_leave_records(self):
        self.click_search()

    def select_leave_type(self, leave_type: str = None):
        try:
            self.leave_type_dropdown.click()
            if leave_type:
                self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{leave_type}')").first.click()
            else:
                self.page.locator(".oxd-select-dropdown .oxd-select-option").nth(1).click()
        except Exception:
            pass

    def enter_date_range(self, from_date: str, to_date: str):
        try:
            self.from_date_input.fill(from_date)
            self.to_date_input.fill(to_date)
        except Exception:
            pass

    def submit_leave_application(self, leave_type: str = None, from_date: str = "2026-12-01", to_date: str = "2026-12-02"):
        self.select_leave_type(leave_type)
        self.enter_date_range(from_date, to_date)
        self.apply_submit_button.click()
        self.wait_for_page_ready()

    def is_apply_leave_displayed(self) -> bool:
        try:
            return "applyLeave" in self.page.url or self.apply_leave_title.first.is_visible()
        except Exception:
            return False

    def get_records_text(self) -> str:
        try:
            return self.records_found_span.first.inner_text().strip()
        except Exception:
            return ""

    def get_leave_rows_count(self) -> int:
        return self.table_rows.count()

    def is_action_button_available(self) -> bool:
        try:
            return self.approve_button.is_visible(timeout=3000) or self.reject_button.is_visible(timeout=3000)
        except Exception:
            return False

    def get_leave_balance_text(self) -> str:
        try:
            return self.leave_balance_label.first.inner_text().strip()
        except Exception:
            return ""

    def click_cancel_leave(self):
        try:
            if self.cancel_leave_button.is_visible(timeout=3000):
                self.cancel_leave_button.click()
                self.wait_for_page_ready()
        except Exception:
            pass
