from playwright.sync_api import Page
from pages.base_page import BasePage


class BuzzPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.post_textarea = page.locator("textarea.oxd-buzz-post-input")
        self.post_button = page.locator("button:has-text('Post')").first
        self.feed_posts = page.locator(".orangehrm-buzz-post-body-text")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_buzz(self):
        self.navigate_to("/web/index.php/buzz/viewBuzz")

    def type_post_content(self, content: str):
        self.post_textarea.fill(content)

    def click_post_button(self):
        self.post_button.click()
        self.wait_for_page_ready()

    def create_post(self, content: str):
        self.type_post_content(content)
        self.click_post_button()

    def get_latest_post_content(self) -> str:
        try:
            return self.feed_posts.first.inner_text().strip()
        except Exception:
            return ""
