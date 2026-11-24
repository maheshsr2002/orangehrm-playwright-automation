from pages.sidebar_component import SidebarComponent


class NavigationSteps:
    """
    Step Definitions / Test Logic Layer: Sidebar Menu Navigation.
    Chains menu filtering and clearing sequences.
    Contains NO final assertions.
    """

    def __init__(self, sidebar_component: SidebarComponent):
        self.sidebar_component = sidebar_component

    def filter_menu_by_keyword(self, keyword: str) -> dict:
        """Types keyword into sidebar search and returns visible items list."""
        self.sidebar_component.type_search_query(keyword)
        visible = self.sidebar_component.get_visible_menu_names()

        return {
            "keyword": keyword,
            "visible_items": visible,
            "visible_count": len(visible)
        }

    def restore_full_menu(self) -> dict:
        """Clears search filter and returns restored menu items."""
        self.sidebar_component.clear_search_query()
        visible = self.sidebar_component.get_visible_menu_names()

        return {
            "restored_items": visible,
            "total_count": len(visible)
        }
