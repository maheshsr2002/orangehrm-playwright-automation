from playwright.sync_api import Page
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.breadcrumb_header = page.locator(".oxd-topbar-header-breadcrumb-module, .oxd-topbar-header-breadcrumb h6, h6:has-text('Dashboard')")
        self.dashboard_widgets = page.locator(".oxd-sheet.orangehrm-dashboard-widget")
        self.quick_launch_cards = page.locator(".orangehrm-quick-launch-card p")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_dashboard(self):
        self.navigate_to("/web/index.php/dashboard/index")

    def get_breadcrumb_title(self) -> str:
        try:
            self.breadcrumb_header.first.wait_for(state="visible", timeout=10000)
            return self.breadcrumb_header.first.inner_text().strip()
        except Exception:
            return ""

    def is_dashboard_displayed(self, timeout: int = 15000) -> bool:
        try:
            self.page.wait_for_url("**/dashboard/**", timeout=timeout)
            self.breadcrumb_header.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_dashboard_widgets_count(self) -> int:
        return self.dashboard_widgets.count()

    def get_quick_launch_card_names(self) -> list[str]:
        return [
            self.quick_launch_cards.nth(i).inner_text().strip()
            for i in range(self.quick_launch_cards.count())
        ]
