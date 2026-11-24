import pytest
from steps.buzz_steps import BuzzSteps
from data.data_loader import DataLoader


@pytest.mark.buzz
@pytest.mark.regression
class TestBuzzFeed:
    """
    Tests & Assertions Layer: Buzz Module (Corporate Social Feed).
    Responsibility: Validate posting status updates to the Buzz wall.
    Payloads fetched or generated via DataLoader.
    """

    def test_post_status_update(self, authenticated_session, buzz_steps: BuzzSteps):
        """
        Social Wall Test: Posts status update message to Buzz wall and verifies feed content.
        """
        post_message = DataLoader.generate_unique_buzz_post()
        result = buzz_steps.publish_status_post(post_message)

        assert len(result["latest_post_content"]) > 0, "No content found in Buzz feed after posting"
        assert result["submitted_content"] == post_message
