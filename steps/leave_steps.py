from pages.leave_page import LeavePage


class LeaveSteps:
    """
    Step Definitions / Test Logic Layer: Leave Management.
    Chains leave list search and apply tab navigation.
    Contains NO final assertions.
    """

    def __init__(self, leave_page: LeavePage):
        self.leave_page = leave_page

    def search_leave_records(self) -> dict:
        """Navigates to Leave, triggers search, and returns records count."""
        self.leave_page.navigate_to_leave()
        self.leave_page.click_search()

        return {
            "summary_text": self.leave_page.get_records_text(),
            "rows_count": self.leave_page.get_leave_rows_count()
        }

    def navigate_to_apply_leave(self) -> dict:
        """Clicks Apply tab and returns form visibility state."""
        self.leave_page.navigate_to_leave()
        self.leave_page.click_apply_tab()

        return {
            "is_apply_displayed": self.leave_page.is_apply_leave_displayed()
        }

    def apply_for_leave(self, leave_type: str = None, from_date: str = "2026-12-01", to_date: str = "2026-12-02") -> dict:
        """Navigates to Apply tab and submits leave request."""
        self.leave_page.navigate_to_leave()
        self.leave_page.click_apply_tab()
        self.leave_page.submit_leave_application(leave_type=leave_type, from_date=from_date, to_date=to_date)

        return {
            "is_submitted": True,
            "current_url": self.leave_page.get_current_url()
        }

    def inspect_approval_workflow(self) -> dict:
        """Inspects leave queue for pending leave action buttons (Approve/Reject)."""
        self.leave_page.navigate_to_leave()
        self.leave_page.click_search()

        return {
            "has_action_buttons": self.leave_page.is_action_button_available(),
            "total_records": self.leave_page.get_leave_rows_count()
        }
