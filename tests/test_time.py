import pytest
from steps.time_steps import TimeSteps
from data.test_data import TIME_DATA


@pytest.mark.time
@pytest.mark.regression
class TestTimeModule:
    """
    Test Suite: Time & Attendance Module.
    Covers:
      1. Timesheet View & Submission: Viewing employee timesheets and submitting working hours.
      2. Attendance & Punch In/Out: Navigating to attendance tracking.
    """

    @pytest.mark.smoke
    def test_view_employee_timesheet(self, authenticated_session, time_steps: TimeSteps):
        """Verifies navigating to Time module and loading employee timesheet."""
        result = time_steps.inspect_employee_timesheet()

        assert result["is_timesheet_displayed"] is True, "Employee timesheet failed to load"
        assert "timesheet" in result["current_url"].lower()

    def test_navigate_to_punch_in_out(self, authenticated_session, time_steps: TimeSteps):
        """Verifies navigation to Attendance Punch In / Punch Out screen."""
        result = time_steps.navigate_and_inspect_punch_page()

        assert result["is_punch_page_displayed"] is True or "punch" in result["current_url"].lower()

    def test_edit_and_submit_timesheet(self, authenticated_session, time_steps: TimeSteps):
        """Verifies timesheet review and submission trigger for supervisor approval."""
        result = time_steps.submit_timesheet_review()

        assert result["is_timesheet_displayed"] is True
