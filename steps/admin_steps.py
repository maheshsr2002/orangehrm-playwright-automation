from pages.admin_page import AdminPage


class AdminSteps:
    """
    Step Definitions / Test Logic Layer: Admin User Management.
    Chains filter application, searching, and table inspection.
    Contains NO final assertions.
    """

    def __init__(self, admin_page: AdminPage):
        self.admin_page = admin_page

    def search_system_user(self, username: str) -> dict:
        """Navigates to Admin, filters by username, and returns table state."""
        self.admin_page.navigate_to_admin()
        self.admin_page.search_user(username)

        return {
            "records_count": self.admin_page.get_total_records_count(),
            "first_row_username": self.admin_page.get_first_row_username(),
            "summary_text": self.admin_page.get_records_summary_text()
        }

    def filter_by_role(self, role: str) -> dict:
        """Selects user role filter, searches, and returns results summary."""
        self.admin_page.navigate_to_admin()
        self.admin_page.select_role(role)
        self.admin_page.click_search()

        return {
            "records_count": self.admin_page.get_total_records_count(),
            "summary_text": self.admin_page.get_records_summary_text()
        }

    def filter_by_status(self, status: str) -> dict:
        """Selects user status filter, searches, and returns results summary."""
        self.admin_page.navigate_to_admin()
        self.admin_page.filter_by_status(status)

        return {
            "records_count": self.admin_page.get_total_records_count(),
            "summary_text": self.admin_page.get_records_summary_text()
        }

    def reset_search_filters(self) -> dict:
        """Resets filter criteria on Admin page."""
        self.admin_page.navigate_to_admin()
        self.admin_page.click_reset()
        return {
            "records_count": self.admin_page.get_total_records_count(),
            "summary_text": self.admin_page.get_records_summary_text()
        }

    def create_system_user(self, role: str, employee_hint: str, status: str, username: str, password: str) -> dict:
        """Navigates to Add User, fills details, saves, and returns outcome state."""
        self.admin_page.navigate_to_admin()
        self.admin_page.click_add_user()
        self.admin_page.fill_new_user_form(role, employee_hint, status, username, password)
        self.admin_page.save_new_user()

        return {
            "created_username": username,
            "current_url": self.admin_page.get_current_url()
        }

    def update_first_user(self) -> dict:
        """Clicks edit on the first user in table and saves changes."""
        self.admin_page.click_edit_first_user()

        return {
            "current_url": self.admin_page.get_current_url()
        }

    def delete_first_user(self) -> dict:
        """Clicks delete on the first user in table and confirms deletion."""
        initial_count = self.admin_page.get_total_records_count()
        self.admin_page.click_delete_first_user()

        return {
            "initial_count": initial_count,
            "new_count": self.admin_page.get_total_records_count()
        }
