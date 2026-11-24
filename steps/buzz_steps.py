from pages.buzz_page import BuzzPage


class BuzzSteps:
    """
    Step Definitions / Test Logic Layer: Buzz Social Wall.
    Chains newsfeed navigation and post publishing workflows.
    Contains NO final assertions.
    """

    def __init__(self, buzz_page: BuzzPage):
        self.buzz_page = buzz_page

    def publish_status_post(self, content: str) -> dict:
        """Navigates to Buzz, inputs post content, clicks post, and returns extracted body."""
        self.buzz_page.navigate_to_buzz()
        self.buzz_page.type_post_content(content)
        self.buzz_page.click_post_button()
        latest = self.buzz_page.get_latest_post_content()

        return {
            "submitted_content": content,
            "latest_post_content": latest
        }
