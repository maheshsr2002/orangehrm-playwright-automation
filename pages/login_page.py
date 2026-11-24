from playwright.sync_api import Page
from pages.base_page import BasePage
from data.config import Config


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("button[type='submit']")
        self.forgot_password_link = page.locator(".orangehrm-login-forgot p, a:has-text('Forgot your password?')")
        self.alert_message = page.locator(".oxd-alert-content-text")
        self.username_error = page.locator(".oxd-input-group:has(input[name='username']) .oxd-input-group__message")
        self.password_error = page.locator(".oxd-input-group:has(input[name='password']) .oxd-input-group__message")
        self.reset_password_header = page.locator(".orangehrm-forgot-password-title")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_login(self, url: str = None):
        target = url or f"{self.base_url}/web/index.php/auth/login"
        self.page.goto(target)

    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str = "", password: str = ""):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def login_with_valid_credentials(self):
        self.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)

    def click_forgot_password(self):
        self.forgot_password_link.click()

    def get_error_text(self) -> str:
        return self.get_alert_error_message()

    def get_alert_error_message(self) -> str:
        try:
            self.alert_message.first.wait_for(state="visible", timeout=8000)
            return self.alert_message.first.inner_text().strip()
        except Exception:
            return ""

    def get_username_field_error(self) -> str:
        try:
            self.username_error.first.wait_for(state="visible", timeout=6000)
            return self.username_error.first.inner_text().strip()
        except Exception:
            return ""

    def get_password_field_error(self) -> str:
        try:
            self.password_error.first.wait_for(state="visible", timeout=6000)
            return self.password_error.first.inner_text().strip()
        except Exception:
            return ""

    def is_login_page_displayed(self, timeout: int = 10000) -> bool:
        try:
            self.login_button.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_reset_password_page_displayed(self) -> bool:
        try:
            self.reset_password_header.wait_for(state="visible", timeout=8000)
            return True
        except Exception:
            return "requestPasswordResetCode" in self.page.url
