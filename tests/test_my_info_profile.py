import pytest
from steps.profile_steps import ProfileSteps
from data.data_loader import DataLoader

PROFILE_DATA = DataLoader.get_profile_update_data()


@pytest.mark.profile
@pytest.mark.regression
class TestMyInfoProfile:
    """
    Tests & Assertions Layer: My Info Module (Personal Profile).
    Responsibility: Validate viewing and updating personal details fields.
    Data fetched from data/payloads/employees.json via DataLoader.
    """

    def test_view_and_update_personal_profile(self, authenticated_session, profile_steps: ProfileSteps):
        """
        Verifies employee can navigate to My Info, update personal details,
        and confirms that the updated value is persisted.
        """
        update_val = PROFILE_DATA.get("nickname", "AlexAuto")
        result = profile_steps.update_personal_profile(update_val)

        assert result["is_page_loaded"] is True, "My Info personal details page failed to load"
        assert result["retained_value"] == update_val, (
            f"Expected retained value '{update_val}', got '{result['retained_value']}'"
        )
