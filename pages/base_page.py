from playwright.sync_api import Page
from data.config import Config


class BasePage:
    """
    Base Page Model.
    Responsibility: Common page navigation and basic wait actions.
    Rule: Interactions only, NO assertions.
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_url = Config.BASE_URL

    # Common Actions (Interactions only, no assertions)
    def navigate_to(self, route: str = ""):
        self.page.goto(f"{self.base_url}{route}")

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_spinner(self, timeout: int = 15000):
        try:
            spinner = self.page.locator(".oxd-loading-spinner")
            if spinner.is_visible(timeout=1500):
                spinner.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass

    def wait_for_page_ready(self, timeout: int = 15000):
        try:
            self.page.wait_for_load_state("load", timeout=timeout)
        except Exception:
            pass
        self.wait_for_spinner(timeout=timeout)
