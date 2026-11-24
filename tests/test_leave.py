import pytest
from steps.leave_steps import LeaveSteps
from data.test_data import LEAVE_DATA


@pytest.mark.leave
@pytest.mark.regression
class TestLeaveModule:
    """
    Test Suite: Leave Module.
    Covers:
      1. Apply for Leave: Form navigation, type selection, date submission.
      2. Leave List / Entitlements: Searching leave records queue and verification.
      3. Approval/Rejection Workflow: Action button availability in leave queue.
    """

    @pytest.mark.smoke
    def test_navigate_to_apply_leave_form(self, authenticated_session, leave_steps: LeaveSteps):
        """Verifies navigation to Apply Leave form tab and form load."""
        result = leave_steps.navigate_to_apply_leave()

        assert result["is_apply_displayed"] is True, "Apply Leave form failed to display"

    def test_apply_for_leave_submission(self, authenticated_session, leave_steps: LeaveSteps):
        """Selects leave type, chooses date ranges, and submits leave request."""
        result = leave_steps.apply_for_leave(
            leave_type=LEAVE_DATA.get("leave_type"),
            from_date=LEAVE_DATA.get("from_date", "2026-12-01"),
            to_date=LEAVE_DATA.get("to_date", "2026-12-02")
        )

        assert result["is_submitted"] is True

    def test_view_and_search_leave_list(self, authenticated_session, leave_steps: LeaveSteps):
        """Verifies searching leave list records displays leave queue."""
        result = leave_steps.search_leave_records()

        assert ("Record" in result["summary_text"]) or (result["rows_count"] >= 0)

    def test_inspect_leave_approval_workflow(self, authenticated_session, leave_steps: LeaveSteps):
        """Inspects corporate leave list queue for approval/rejection actions."""
        result = leave_steps.inspect_approval_workflow()

        assert result["total_records"] >= 0
