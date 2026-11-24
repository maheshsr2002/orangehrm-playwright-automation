from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.header_component import HeaderComponent
from data.models import UserCredentials
from data.data_loader import DataLoader


class AuthSteps:
    """
    Step Definitions / Test Logic Layer: Authentication.
    Responsibility: Chains multiple page interactions into semantic business flows.
    Strict Rule: Contains NO final test assertions; returns extracted state data to tests.
    """

    def __init__(self, login_page: LoginPage, dashboard_page: DashboardPage, header_component: HeaderComponent):
        self.login_page = login_page
        self.dashboard_page = dashboard_page
        self.header_component = header_component

    def execute_login(self, username: str, password: str) -> dict:
        """Executes a login attempt with arbitrary credentials and returns extracted feedback."""
        self.login_page.navigate_to_login()
        self.login_page.enter_username(username or "")
        self.login_page.enter_password(password or "")
        self.login_page.click_login()

        return {
            "alert_error": self.login_page.get_alert_error_message(),
            "username_error": self.login_page.get_username_field_error(),
            "password_error": self.login_page.get_password_field_error(),
            "is_login_page": self.login_page.is_login_page_displayed(),
            "is_dashboard": self.dashboard_page.is_dashboard_displayed(timeout=3000)
        }

    def execute_valid_login(self, credentials: UserCredentials = None) -> dict:
        """Executes successful login using confidential credentials and returns landing state."""
        creds = credentials or DataLoader.get_valid_credentials()
        self.login_page.navigate_to_login()
        self.login_page.enter_username(creds.username)
        self.login_page.enter_password(creds.password)
        self.login_page.click_login()

        is_dashboard = self.dashboard_page.is_dashboard_displayed(timeout=20000)
        title = self.dashboard_page.get_breadcrumb_title() if is_dashboard else ""

        return {
            "is_dashboard_displayed": is_dashboard,
            "breadcrumb_title": title,
            "current_url": self.dashboard_page.get_current_url()
        }

    def execute_empty_credentials_attempt(self) -> dict:
        """Submits empty credentials and extracts field validations."""
        self.login_page.navigate_to_login()
        self.login_page.enter_username("")
        self.login_page.enter_password("")
        self.login_page.click_login()

        return {
            "username_error": self.login_page.get_username_field_error(),
            "password_error": self.login_page.get_password_field_error(),
            "is_login_page": self.login_page.is_login_page_displayed()
        }

    def execute_forgot_password_flow(self) -> dict:
        """Navigates through forgot password link and extracts destination state."""
        self.login_page.navigate_to_login()
        self.login_page.click_forgot_password()

        return {
            "is_reset_page_displayed": self.login_page.is_reset_password_page_displayed(),
            "current_url": self.login_page.get_current_url()
        }

    def execute_logout(self) -> dict:
        """Chains profile dropdown opening and logout click, returning final page state."""
        self.header_component.open_user_dropdown()
        self.header_component.click_logout_button()

        return {
            "is_login_page_displayed": self.login_page.is_login_page_displayed(),
            "current_url": self.login_page.get_current_url()
        }
