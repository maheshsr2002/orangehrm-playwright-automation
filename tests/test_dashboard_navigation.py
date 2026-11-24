import pytest
from steps.dashboard_steps import DashboardSteps
from steps.navigation_steps import NavigationSteps
from data.data_loader import DataLoader

EXPECTED = DataLoader.get_expected_messages()
NAV_SAMPLES = DataLoader.get_navigation_search_samples()


@pytest.mark.smoke
@pytest.mark.dashboard
class TestDashboardNavigation:
    """
    Tests & Assertions Layer: Dashboard and Navigation Menu.
    Responsibility: Validate dashboard landing widgets and sidebar menu search.
    All data fetched from data/payloads/navigation.json and expected_messages.json.
    """

    def test_dashboard_landing_page(self, authenticated_session, dashboard_steps: DashboardSteps):
        """Verifies dashboard breadcrumb, visibility, and widget presence after login."""
        result = dashboard_steps.inspect_dashboard()

        assert result["is_displayed"] is True, "Dashboard was not displayed"
        assert result["breadcrumb_title"] == EXPECTED.dashboard_breadcrumb, (
            f"Expected breadcrumb '{EXPECTED.dashboard_breadcrumb}', got '{result['breadcrumb_title']}'"
        )
        assert result["widget_count"] > 0, "No dashboard widgets found"
        assert len(result["quick_launch_items"]) >= 0

    @pytest.mark.parametrize("sample", NAV_SAMPLES, ids=[s["keyword"] for s in NAV_SAMPLES])
    def test_sidebar_search_filter(self, authenticated_session, navigation_steps: NavigationSteps, sample: dict):
        """Data-driven test: Verifies filtering sidebar menu with keywords from navigation.json."""
        keyword = sample["keyword"]
        filter_result = navigation_steps.filter_menu_by_keyword(keyword)

        assert filter_result["visible_count"] >= 1, f"No menu item found matching '{keyword}'"
        assert any(keyword.lower() in item.lower() for item in filter_result["visible_items"]), (
            f"Expected '{keyword}' in visible menu items: {filter_result['visible_items']}"
        )

        # Clear search and verify menu restoration
        restore_result = navigation_steps.restore_full_menu()
        assert restore_result["total_count"] >= 5, "Sidebar menu items not properly restored after clearing filter"
