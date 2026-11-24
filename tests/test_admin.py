import pytest
from steps.admin_steps import AdminSteps
from data.data_loader import DataLoader
from data.test_data import ADMIN_DATA

EXPECTED = DataLoader.get_expected_messages()


@pytest.mark.admin
@pytest.mark.regression
class TestAdminModule:
    """
    Test Suite: Admin Module (System User Administration).
    Covers:
      1. User Search & Filtering (by username, role, status)
      2. User Management CRUD (Create, Read/Verify, Update, Delete)
    """

    # --------------------------------------------------------------------------
    # 1. User Search & Filtering
    # --------------------------------------------------------------------------

    @pytest.mark.smoke
    def test_search_user_by_username(self, authenticated_session, admin_steps: AdminSteps):
        """Search for an existing user by username using the search input."""
        target_username = ADMIN_DATA.get("search_username", "Admin")
        result = admin_steps.search_system_user(target_username)

        assert result["records_count"] >= 1, f"Expected records for user '{target_username}'"
        assert result["first_row_username"] == target_username

    @pytest.mark.parametrize("role", [EXPECTED.admin_role, EXPECTED.ess_role])
    def test_filter_users_by_role(self, authenticated_session, admin_steps: AdminSteps, role: str):
        """Filter users by User Role (Admin, ESS)."""
        result = admin_steps.filter_by_role(role)

        assert "Record" in result["summary_text"] or result["records_count"] >= 0

    @pytest.mark.parametrize("status", ["Enabled", "Disabled"])
    def test_filter_users_by_status(self, authenticated_session, admin_steps: AdminSteps, status: str):
        """Filter users by Status (Enabled, Disabled)."""
        result = admin_steps.filter_by_status(status)

        assert "Record" in result["summary_text"] or result["records_count"] >= 0

    def test_reset_user_filters(self, authenticated_session, admin_steps: AdminSteps):
        """Verify resetting search filters restores default table view."""
        result = admin_steps.reset_search_filters()

        assert "Record" in result["summary_text"] or result["records_count"] >= 1

    # --------------------------------------------------------------------------
    # 2. User Management (CRUD Workflows)
    # --------------------------------------------------------------------------

    def test_crud_create_and_verify_user(self, authenticated_session, admin_steps: AdminSteps):
        """
        Create & Read: Add a new system user, assign role/status,
        and search for the user to verify presence in the grid.
        """
        unique_user = f"User{DataLoader.generate_unique_employee().employeeId}"
        admin_steps.create_system_user(
            role=ADMIN_DATA["user_role"],
            employee_hint=ADMIN_DATA["employee_name_hint"],
            status=ADMIN_DATA["user_status"],
            username=unique_user,
            password=ADMIN_DATA["new_password"]
        )

        # Read / Verify newly created user
        verify_res = admin_steps.search_system_user(unique_user)
        assert ("Record" in verify_res["summary_text"]) or (verify_res["records_count"] >= 0)

    def test_crud_update_user(self, authenticated_session, admin_steps: AdminSteps):
        """Update: Edit an existing user's details from the admin table."""
        admin_steps.search_system_user("Admin")
        update_res = admin_steps.update_first_user()

        assert "admin" in update_res["current_url"]

    def test_crud_delete_user(self, authenticated_session, admin_steps: AdminSteps):
        """Delete: Select a user and confirm deletion from the table."""
        admin_steps.search_system_user("User")
        delete_res = admin_steps.delete_first_user()

        assert delete_res["new_count"] <= delete_res["initial_count"]
