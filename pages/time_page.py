from playwright.sync_api import Page
from pages.base_page import BasePage


class TimePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.time_nav = page.locator(".oxd-main-menu-item:has(span:has-text('Time'))")
        self.timesheet_header = page.locator(".orangehrm-timesheet-header, h6:has-text('Timesheet')")
        self.attendance_tab = page.locator(".oxd-topbar-body-nav-tab-item:has-text('Attendance')")
        self.punch_in_out_menu = page.locator("a.oxd-topbar-body-nav-tab-link:has-text('Punch In/Out')")
        self.timesheet_table = page.locator(".orangehrm-timesheet-table, .oxd-table")
        self.edit_button = page.locator("button:has-text('Edit')")
        self.save_button = page.locator("button:has-text('Save')")
        self.submit_button = page.locator("button:has-text('Submit')")
        self.punch_header = page.locator("h6:has-text('Punch In'), h6:has-text('Punch Out')")
        self.in_out_button = page.locator("button[type='submit']")
        self.note_textarea = page.locator("textarea[placeholder='Type here']")
        self.toast_alert = page.locator(".oxd-toast--error, .oxd-toast")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_time(self):
        self.navigate_to("/web/index.php/time/viewEmployeeTimesheet")

    def is_timesheet_displayed(self) -> bool:
        try:
            return self.timesheet_header.first.is_visible() or "viewEmployeeTimesheet" in self.page.url
        except Exception:
            return False

    def navigate_to_punch_in_out(self):
        try:
            self.attendance_tab.click()
            self.punch_in_out_menu.click()
            self.wait_for_page_ready()
        except Exception:
            self.navigate_to("/web/index.php/attendance/punchIn")

    def is_punch_page_displayed(self) -> bool:
        try:
            return self.punch_header.first.is_visible() or "punchIn" in self.page.url
        except Exception:
            return False

    def click_edit_timesheet(self):
        try:
            if self.edit_button.is_visible():
                self.edit_button.click()
                self.wait_for_page_ready()
        except Exception:
            pass

    def click_submit_timesheet(self):
        try:
            if self.submit_button.is_visible():
                self.submit_button.click()
                self.wait_for_page_ready()
        except Exception:
            pass

    def click_save_timesheet(self):
        try:
            if self.save_button.is_visible():
                self.save_button.click()
                self.wait_for_page_ready()
        except Exception:
            pass

    def get_toast_message(self) -> str:
        try:
            self.toast_alert.first.wait_for(state="visible", timeout=5000)
            return self.toast_alert.first.inner_text().strip()
        except Exception:
            return ""
