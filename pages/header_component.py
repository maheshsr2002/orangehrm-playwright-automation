from playwright.sync_api import Page
from pages.base_page import BasePage


class HeaderComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.user_dropdown_tab = page.locator(".oxd-userdropdown-tab")
        self.user_dropdown_name = page.locator(".oxd-userdropdown-name")
        self.user_dropdown_menu = page.locator(".oxd-dropdown-menu, [role='menu']")
        self.logout_link = page.locator("a[role='menuitem']:has-text('Logout'), a.oxd-userdropdown-link:has-text('Logout'), a:has-text('Logout')")

    # 2. Actions (Interactions only, no assertions)
    def open_user_dropdown(self):
        self.user_dropdown_tab.wait_for(state="visible", timeout=10000)
        self.user_dropdown_tab.click()
        self.user_dropdown_menu.wait_for(state="visible", timeout=10000)

    def is_user_dropdown_open(self) -> bool:
        try:
            return self.user_dropdown_menu.is_visible()
        except Exception:
            return False

    def close_user_dropdown(self):
        """
        Closes the user dropdown menu.
        Note: In OrangeHRM, re-clicking the profile icon/tab does not toggle it closed.
        Standard behavior requires pressing 'Escape' or clicking outside on the page.
        """
        self.page.keyboard.press("Escape")
        try:
            self.user_dropdown_menu.wait_for(state="hidden", timeout=3000)
        except Exception:
            # Fallback: click outside on the page canvas
            self.page.locator("body").click(position={"x": 50, "y": 50})
            self.user_dropdown_menu.wait_for(state="hidden", timeout=5000)

    def click_logout_button(self):
        self.logout_link.wait_for(state="visible", timeout=10000)
        self.logout_link.click()

    def click_logout(self):
        self.click_logout_button()

    def logout(self):
        self.open_user_dropdown()
        self.click_logout_button()

    def get_logged_in_username(self) -> str:
        self.user_dropdown_name.wait_for(state="visible", timeout=10000)
        return self.user_dropdown_name.inner_text().strip()
