from playwright.sync_api import Page
from pages.base_page import BasePage


class SidebarComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.search_input = page.locator("input.oxd-input[placeholder='Search']")
        self.menu_item_spans = page.locator(".oxd-main-menu-item span")

    # 2. Actions (Interactions only, no assertions)
    def type_search_query(self, query: str):
        self.search_input.fill(query)

    def search_menu(self, query: str):
        self.type_search_query(query)

    def clear_search_query(self):
        self.search_input.fill("")

    def clear_search(self):
        self.clear_search_query()

    def get_visible_menu_names(self) -> list[str]:
        return [
            self.menu_item_spans.nth(i).inner_text().strip()
            for i in range(self.menu_item_spans.count())
            if self.menu_item_spans.nth(i).is_visible()
        ]

    def get_visible_menu_items(self) -> list[str]:
        return self.get_visible_menu_names()

    def click_menu_item(self, menu_name: str):
        self.page.locator(f".oxd-main-menu-item:has(span:has-text('{menu_name}'))").click()
