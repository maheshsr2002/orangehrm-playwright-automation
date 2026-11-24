import pytest
from steps.auth_steps import AuthSteps
from steps.profile_steps import ProfileSteps
from pages.header_component import HeaderComponent
from pages.admin_page import AdminPage
from pages.recruitment_page import RecruitmentPage
from pages.leave_page import LeavePage
from pages.time_page import TimePage
from data.test_data import KNOWN_DEFECTS_DATA


@pytest.mark.defects
class TestKnownDefectsAndGlitches:
    """
    Tests & Assertions Layer: Known Defects & Edge-Case Vulnerabilities.
    Covers real-world defects documented in OrangeHRM QA defect reports:
    1. Special characters in restricted name fields.
    2. Duplicate dependent records.
    3. Self-assignment as an emergency contact.
    4. Unicode / emoji character encoding corruption.
    5. Profile dropdown toggle failure on second click.

    All tests use @pytest.mark.xfail to document expected failures for known application bugs
    without breaking the primary regression pass rate.
    """

    # --------------------------------------------------------------------------
    # Bug 1: Special Characters in Restricted Fields
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: System accepts invalid special characters in name fields without inline validation",
        strict=False
    )
    def test_bug_special_characters_in_restricted_name_field(
        self,
        authenticated_session,
        profile_steps: ProfileSteps
    ):
        """
        QA Defect: Entering invalid special characters in first name should trigger
        an inline validation error (e.g., 'Allows numbers and alphabets only').
        """
        payload = KNOWN_DEFECTS_DATA.get("special_characters_input", {})
        invalid_name = payload.get("first_name_special_chars", "Alex@#$%^&")

        result = profile_steps.attempt_save_special_characters_name(invalid_name)

        # Expected: Validation warning displayed
        # Actual Bug: Form accepts special characters without error
        assert result["field_error"] != "", (
            f"Bug Reproduced: System permitted saving '{invalid_name}' without inline validation!"
        )

    # --------------------------------------------------------------------------
    # Bug 2: Duplicate Dependent Entries
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Application allows saving duplicate identical dependent entries",
        strict=False
    )
    def test_bug_duplicate_dependent_entries(
        self,
        authenticated_session,
        profile_steps: ProfileSteps
    ):
        """
        QA Defect: Saving identical dependent records multiple times should trigger
        an 'Already exists' validation error.
        """
        payload = KNOWN_DEFECTS_DATA.get("duplicate_dependent", {})
        name = payload.get("name", "Emma Wright")
        relationship = payload.get("relationship", "Child")
        dob = payload.get("date_of_birth", "2018-05-14")

        result = profile_steps.attempt_duplicate_dependent(name, relationship, dob)

        # Expected: Warning appears or second entry is blocked
        # Actual Bug: Second entry saves, incrementing count
        assert "already exists" in result["toast_error"].lower(), (
            f"Bug Reproduced: System allowed duplicate dependent '{name}' without uniqueness warning!"
        )

    # --------------------------------------------------------------------------
    # Bug 3: Self-Assignment as Emergency Contact
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Business logic allows an employee to add themselves as their own emergency contact",
        strict=False
    )
    def test_bug_self_assignment_emergency_contact(
        self,
        authenticated_session,
        profile_steps: ProfileSteps
    ):
        """
        QA Defect: An employee should not be permitted to register themselves as
        their own emergency contact.
        """
        payload = KNOWN_DEFECTS_DATA.get("self_assignment_emergency_contact", {})
        name = payload.get("name", "Alexander Wright")
        relationship = payload.get("relationship", "Self")
        mobile = payload.get("mobile", "+1-555-019-3344")

        result = profile_steps.attempt_self_emergency_contact(name, relationship, mobile)

        # Expected: Business rule validation error
        # Actual Bug: Saves successfully
        assert result["field_error"] != "" or "cannot" in result["toast_error"].lower(), (
            f"Bug Reproduced: Employee was able to add themselves as an emergency contact!"
        )

    # --------------------------------------------------------------------------
    # Bug 4: Character Encoding / Emoji Corruption
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: 4-byte UTF-8 emojis render as '?' due to database collation limit",
        strict=False
    )
    def test_bug_unicode_emoji_encoding(
        self,
        authenticated_session,
        profile_steps: ProfileSteps
    ):
        """
        QA Defect: Entering Unicode 4-byte emojis (e.g., 💅) causes them to render
        as question marks (?) after saving.
        """
        payload = KNOWN_DEFECTS_DATA.get("character_encoding_unicode_emoji", {})
        emoji_val = payload.get("emoji_nickname", "Alex 💅🚀✨")
        raw_emoji = payload.get("raw_emoji", "💅")

        result = profile_steps.attempt_save_emoji_nickname(emoji_val)

        # Expected: Emoji is retained after page reload
        # Actual Bug: Emoji is replaced with '?'
        assert raw_emoji in result["retained_value"], (
            f"Bug Reproduced: Emoji '{raw_emoji}' was corrupted to '{result['retained_value']}'"
        )

    # --------------------------------------------------------------------------
    # Bug 5: Profile Dropdown Toggle Failure
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Clicking profile tab a second time fails to toggle menu closed",
        strict=False
    )
    def test_bug_profile_dropdown_toggle_failure(
        self,
        authenticated_session,
        header_component: HeaderComponent
    ):
        """
        UI Defect: Clicking profile avatar a second time should toggle the menu closed.
        Actual Bug: The dropdown remains visible.
        """
        # First click: opens dropdown
        header_component.open_user_dropdown()
        assert header_component.is_user_dropdown_open() is True, "Dropdown failed to open on first click"

        # Second click on same tab: should close dropdown
        header_component.user_dropdown_tab.click()

        # Expected: Menu closes
        # Actual Bug: Menu remains open
        assert header_component.is_user_dropdown_open() is False, (
            "Bug Reproduced: User dropdown failed to toggle closed on second tab click!"
        )

    # --------------------------------------------------------------------------
    # Bug 6: 404 Error When Deleting Qualifications
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Deleting qualifications results in 404 Records Not Found error",
        strict=False
    )
    def test_bug_qualifications_404_deletion(
        self,
        authenticated_session,
        admin_page: AdminPage
    ):
        """
        Backend Defect: Deleting saved Education entries in Admin -> Qualifications
        should delete smoothly and show 'Successfully Deleted'.
        Actual Bug: Triggers a 404 Records Not Found toast error.
        """
        admin_page.navigate_to_education()
        admin_page.delete_first_education_record()

        toast = admin_page.get_toast_error()
        assert "404" not in toast and "not found" not in toast.lower(), (
            f"Bug Reproduced: Deleting qualification threw 404 error: '{toast}'"
        )

    # --------------------------------------------------------------------------
    # Bug 7: 500 Internal Server Error in Recruitment
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Shortlisting candidate for certain vacancies triggers 500 Internal Server Error",
        strict=False
    )
    def test_bug_recruitment_500_shortlist(
        self,
        authenticated_session,
        recruitment_page: RecruitmentPage
    ):
        """
        Backend Defect: Shortlisting a candidate for vacancy should succeed without 500 error.
        Actual Bug: Backend throws unhandled 500 Internal Server Error.
        """
        recruitment_page.navigate_to_recruitment()
        if recruitment_page.get_candidates_count() > 0:
            recruitment_page.table_rows.first.click()
            recruitment_page.click_shortlist()

        action_error = recruitment_page.get_action_error()
        assert "500" not in action_error and "internal server error" not in action_error.lower(), (
            f"Bug Reproduced: Shortlisting candidate threw 500 error: '{action_error}'"
        )

    # --------------------------------------------------------------------------
    # Bug 8: Leave Module Crashes and Balance Drops
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Leave cancellation fails to restore entitlement balance or crashes on DateTime bounds",
        strict=False
    )
    def test_bug_leave_balance_restoration(
        self,
        authenticated_session,
        leave_page: LeavePage
    ):
        """
        Module Defect: Canceling a submitted leave request must restore the deducted leave balance.
        Actual Bug: Leave balance fails to restore properly.
        """
        leave_page.navigate_to_leave()
        initial_balance = leave_page.get_leave_balance_text()
        leave_page.click_cancel_leave()
        restored_balance = leave_page.get_leave_balance_text()

        # If canceled, balance should not permanently drop
        assert "0.00" not in restored_balance or initial_balance == restored_balance, (
            "Bug Reproduced: Leave balance dropped and failed to restore upon cancellation!"
        )

    # --------------------------------------------------------------------------
    # Bug 9: Timesheet Intermittent Save Failures
    # --------------------------------------------------------------------------
    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="Known Defect: Submitting or updating employee timesheets intermittently fails to save",
        strict=False
    )
    def test_bug_timesheet_intermittent_save_failure(
        self,
        authenticated_session,
        time_page: TimePage
    ):
        """
        Module Defect: Updating timesheet hours and saving should reliably persist.
        Actual Bug: Intermittent save failure without clear error diagnostics.
        """
        time_page.navigate_to_time()
        time_page.click_edit_timesheet()
        time_page.click_save_timesheet()

        toast = time_page.get_toast_message()
        assert "failed" not in toast.lower() and "error" not in toast.lower(), (
            f"Bug Reproduced: Timesheet save operation failed: '{toast}'"
        )
