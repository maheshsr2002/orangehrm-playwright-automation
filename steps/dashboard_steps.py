from pages.dashboard_page import DashboardPage


class DashboardSteps:
    """
    Step Definitions / Test Logic Layer: Dashboard.
    Chains dashboard inspection interactions and returns extracted statistics.
    Contains NO final assertions.
    """

    def __init__(self, dashboard_page: DashboardPage):
        self.dashboard_page = dashboard_page

    def inspect_dashboard(self) -> dict:
        """Inspects and returns dashboard state metrics."""
        is_displayed = self.dashboard_page.is_dashboard_displayed(timeout=10000)
        title = self.dashboard_page.get_breadcrumb_title() if is_displayed else ""
        widgets_count = self.dashboard_page.get_dashboard_widgets_count()
        quick_launch_items = self.dashboard_page.get_quick_launch_card_names()

        return {
            "is_displayed": is_displayed,
            "breadcrumb_title": title,
            "widget_count": widgets_count,
            "quick_launch_items": quick_launch_items
        }
