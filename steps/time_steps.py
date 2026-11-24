from pages.time_page import TimePage


class TimeSteps:
    """
    Step Definitions / Test Logic Layer: Time & Attendance.
    Chains timesheet inspection, punch in/out, and working hours interactions.
    Contains NO final assertions; returns extracted states.
    """

    def __init__(self, time_page: TimePage):
        self.time_page = time_page

    def inspect_employee_timesheet(self) -> dict:
        """Navigates to timesheet view and returns state."""
        self.time_page.navigate_to_time()
        is_displayed = self.time_page.is_timesheet_displayed()

        return {
            "is_timesheet_displayed": is_displayed,
            "current_url": self.time_page.get_current_url()
        }

    def navigate_and_inspect_punch_page(self) -> dict:
        """Navigates to Attendance Punch In/Out and returns state."""
        self.time_page.navigate_to_punch_in_out()
        is_displayed = self.time_page.is_punch_page_displayed()

        return {
            "is_punch_page_displayed": is_displayed,
            "current_url": self.time_page.get_current_url()
        }

    def submit_timesheet_review(self) -> dict:
        """Attempts to edit and submit timesheet."""
        self.time_page.navigate_to_time()
        self.time_page.click_edit_timesheet()
        self.time_page.click_submit_timesheet()

        return {
            "is_timesheet_displayed": self.time_page.is_timesheet_displayed()
        }
