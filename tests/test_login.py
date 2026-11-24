import pytest
from steps.auth_steps import AuthSteps
from data.data_loader import DataLoader
from data.models import NegativeLoginCase

# Fetch expected validation messages and negative test cases from separate documents
EXPECTED = DataLoader.get_expected_messages()
NEGATIVE_CASES = DataLoader.get_negative_login_cases()


@pytest.mark.login
class TestLogin:
    """
    Tests & Assertions Layer: Authentication.
    Responsibility: Define test scenarios, orchestrate auth_steps, and execute ALL assertions.
    Data is strictly fetched from separate documents (data/payloads/users.json and expected_messages.json).
    """

    # --------------------------------------------------------------------------
    # Phase 1: Negative Authentication Validations (Tested First)
    # --------------------------------------------------------------------------

    @pytest.mark.negative
    def test_01_both_fields_empty_negative(self, auth_steps: AuthSteps):
        """Negative validation: Submitting empty form displays 'Required' under both fields."""
        result = auth_steps.execute_empty_credentials_attempt()

        assert result["username_error"] == EXPECTED.required_field
        assert result["password_error"] == EXPECTED.required_field
        assert result["is_login_page"] is True

    @pytest.mark.negative
    def test_02_empty_username_negative(self, auth_steps: AuthSteps):
        """Negative validation: Empty username with password shows 'Required' under username."""
        creds = DataLoader.get_valid_credentials()
        result = auth_steps.execute_login(username="", password=creds.password)

        assert result["username_error"] == EXPECTED.required_field
        assert result["is_login_page"] is True

    @pytest.mark.negative
    def test_03_empty_password_negative(self, auth_steps: AuthSteps):
        """Negative validation: Valid username with empty password shows 'Required' under password."""
        creds = DataLoader.get_valid_credentials()
        result = auth_steps.execute_login(username=creds.username, password="")

        assert result["password_error"] == EXPECTED.required_field
        assert result["is_login_page"] is True

    @pytest.mark.negative
    def test_04_invalid_password_negative(self, auth_steps: AuthSteps):
        """Negative validation: Valid username with incorrect password displays alert banner."""
        creds = DataLoader.get_valid_credentials()
        result = auth_steps.execute_login(username=creds.username, password="WrongPassword!@#")

        assert result["alert_error"] == EXPECTED.invalid_credentials
        assert result["is_login_page"] is True

    @pytest.mark.negative
    def test_05_invalid_username_negative(self, auth_steps: AuthSteps):
        """Negative validation: Non-existent username displays alert banner."""
        creds = DataLoader.get_valid_credentials()
        result = auth_steps.execute_login(username="NonExistentAdmin_999", password=creds.password)

        assert result["alert_error"] == EXPECTED.invalid_credentials
        assert result["is_login_page"] is True

    @pytest.mark.negative
    @pytest.mark.parametrize("scenario", NEGATIVE_CASES, ids=[c.case_id for c in NEGATIVE_CASES])
    def test_06_parameterized_negative_scenarios(self, auth_steps: AuthSteps, scenario: NegativeLoginCase):
        """Data-driven negative login testing loaded from data/payloads/users.json document."""
        result = auth_steps.execute_login(username=scenario.username, password=scenario.password)

        if scenario.error_type == "alert":
            assert result["alert_error"] == scenario.expected_error
            assert result["is_login_page"] is True
        elif scenario.error_type == "field":
            if scenario.target_field == "username":
                assert result["username_error"] == scenario.expected_error
            elif scenario.target_field == "password":
                assert result["password_error"] == scenario.expected_error
            elif scenario.target_field == "both":
                assert result["username_error"] == scenario.expected_error
                assert result["password_error"] == scenario.expected_error

    @pytest.mark.positive
    def test_07_forgot_password_navigation(self, auth_steps: AuthSteps):
        """Navigation: Verifies clicking forgot password navigates to reset password page."""
        result = auth_steps.execute_forgot_password_flow()

        assert result["is_reset_page_displayed"] is True
        assert "requestPasswordResetCode" in result["current_url"]

    # --------------------------------------------------------------------------
    # Phase 2: Valid Authentication (Tested At Last)
    # --------------------------------------------------------------------------

    @pytest.mark.positive
    @pytest.mark.smoke
    def test_08_valid_login_positive(self, auth_steps: AuthSteps):
        """
        Positive test: Logs in with valid confidential credentials fetched from document/env.
        Executed at last after all negative validations.
        """
        result = auth_steps.execute_valid_login()

        assert result["is_dashboard_displayed"] is True
        assert result["breadcrumb_title"] == EXPECTED.dashboard_breadcrumb
        assert "dashboard" in result["current_url"]

    # --------------------------------------------------------------------------
    # Phase 3: Logout Flow (Session Termination)
    # --------------------------------------------------------------------------

    @pytest.mark.positive
    @pytest.mark.smoke
    @pytest.mark.logout
    def test_09_logout_flow(self, auth_steps: AuthSteps):
        """
        Logout Flow: Verifies clicking logout terminates the authenticated session
        and redirects safely back to the Login page.
        """
        auth_steps.execute_valid_login()
        logout_result = auth_steps.execute_logout()

        assert logout_result["is_login_page_displayed"] is True, "Login page not displayed after logout"
        assert "login" in logout_result["current_url"], f"Expected 'login' in URL, got {logout_result['current_url']}"
