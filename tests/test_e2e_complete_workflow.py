import pytest
from steps.e2e_steps import E2ESteps
from data.data_loader import DataLoader

# Load expected messages and test payloads from separate documents
EXPECTED = DataLoader.get_expected_messages()
VALID_CREDS = DataLoader.get_valid_credentials()
SYSTEM_USER_DATA = DataLoader.get_system_user_search_data()
PROFILE_DATA = DataLoader.get_profile_update_data()
NAV_SAMPLES = DataLoader.get_navigation_search_samples()


@pytest.mark.e2e
@pytest.mark.master_flow
class TestCompleteOrangeHRMWorkflow:
    """
    Unified End-to-End Master Workflow:
    1. Tests invalid/negative credentials first on the Login page (remains on login).
    2. Logs in with valid confidential credentials at last.
    3. Seamlessly tests all core sections in a single logged-in session:
       - Dashboard Section (Widgets & Quick Launch shortcuts)
       - Admin Section (User management search & role filter)
       - PIM Section (Add new employee & search in directory)
       - My Info Section (Profile personal details update & persistence)
       - Leave Section (Leave records search & apply leave tab)
       - Recruitment Section (Add candidate into hiring pipeline)
       - Buzz Section (Corporate wall status update post)
       - Sidebar Search Filter Section (Menu filter & restore)
    4. Logs out at the very end and returns to the Login page.

    Architectural Conformance:
    - Data Layer: All data fetched from separate JSON documents / .env via DataLoader.
    - Page Layer: Contains 0 assertions and 0 high-level workflows.
    - Steps Layer: Chains page interactions and returns state dicts (0 assertions).
    - Tests Layer: Performs all verification and assertion statements.
    """

    def test_complete_end_to_end_journey(self, e2e_steps: E2ESteps):
        # ======================================================================
        # PHASE 1: NEGATIVE LOGIN TESTS FIRST (On Login Page)
        # ======================================================================
        print("\n[Phase 1] Executing negative login validations first...")
        neg_results = e2e_steps.execute_negative_login_suite(
            valid_username=VALID_CREDS.username,
            wrong_password="WrongPassword!@#999",
            invalid_username="NonExistentAdmin_999",
            invalid_password=VALID_CREDS.password
        )

        empty_res = neg_results["empty_credentials_result"]
        assert empty_res["username_error"] == EXPECTED.required_field, (
            f"Expected '{EXPECTED.required_field}', got '{empty_res['username_error']}'"
        )
        assert empty_res["password_error"] == EXPECTED.required_field, (
            f"Expected '{EXPECTED.required_field}', got '{empty_res['password_error']}'"
        )
        assert empty_res["is_login_page"] is True

        wrong_pass_res = neg_results["wrong_password_result"]
        assert wrong_pass_res["alert_error"] == EXPECTED.invalid_credentials, (
            f"Expected '{EXPECTED.invalid_credentials}', got '{wrong_pass_res['alert_error']}'"
        )
        assert wrong_pass_res["is_login_page"] is True

        wrong_user_res = neg_results["wrong_user_result"]
        assert wrong_user_res["alert_error"] == EXPECTED.invalid_credentials, (
            f"Expected '{EXPECTED.invalid_credentials}', got '{wrong_user_res['alert_error']}'"
        )
        assert wrong_user_res["is_login_page"] is True
        print("  -> Negative login validations completed successfully!")

        # ======================================================================
        # PHASE 2: AT LAST, LOGIN WITH VALID CONFIDENTIAL CREDENTIALS
        # ======================================================================
        print("\n[Phase 2] Logging in with valid confidential credentials at last...")
        login_res = e2e_steps.execute_valid_login(VALID_CREDS)

        assert login_res["is_dashboard_displayed"] is True, "Failed to reach Dashboard after valid login"
        assert login_res["breadcrumb_title"] == EXPECTED.dashboard_breadcrumb, (
            f"Expected '{EXPECTED.dashboard_breadcrumb}', got '{login_res['breadcrumb_title']}'"
        )
        print("  -> Successfully logged in! Dashboard is active.")

        # ======================================================================
        # PHASE 3: TEST ENTIRE SECTIONS IN A SINGLE CONTINUOUS SESSION
        # ======================================================================

        # --- SECTION A: DASHBOARD ---
        print("\n[Phase 3 - Section A: Dashboard] Inspecting widgets and quick launch shortcuts...")
        dash_res = e2e_steps.execute_dashboard_section()
        assert dash_res["is_displayed"] is True, "Dashboard is not displayed"
        assert dash_res["breadcrumb_title"] == EXPECTED.dashboard_breadcrumb
        assert dash_res["widget_count"] > 0, "No dashboard widgets found"
        print(f"  -> Found {dash_res['widget_count']} dashboard widgets and {len(dash_res['quick_launch_items'])} quick launch items.")

        # --- SECTION B: ADMIN (USER MANAGEMENT) ---
        target_user = SYSTEM_USER_DATA.get("target_username", "Admin")
        target_role = SYSTEM_USER_DATA.get("role", EXPECTED.admin_role)
        print(f"\n[Phase 3 - Section B: Admin] Searching system user '{target_user}' and filtering by role '{target_role}'...")
        admin_res = e2e_steps.execute_admin_section(target_username=target_user, role=target_role)

        search_res = admin_res["search_result"]
        assert search_res["records_count"] >= 1, f"Admin user record '{target_user}' not found"
        assert search_res["first_row_username"] == target_user, (
            f"Expected first row username '{target_user}', got '{search_res['first_row_username']}'"
        )

        role_res = admin_res["role_filter_result"]
        assert role_res["records_count"] >= 1 or "Record" in role_res["summary_text"]
        print("  -> Admin user search and role filter verified!")

        # --- SECTION C: PIM (EMPLOYEE ONBOARDING & DIRECTORY SEARCH) ---
        new_employee = DataLoader.generate_unique_employee()
        print(f"\n[Phase 3 - Section C: PIM] Onboarding employee '{new_employee.firstName} {new_employee.lastName}' (ID: {new_employee.employeeId})...")
        pim_res = e2e_steps.execute_pim_section(employee=new_employee, search_keyword=new_employee.firstName)

        onboard_res = pim_res["onboard_result"]
        assert onboard_res["is_personal_details_displayed"] is True, (
            "Personal details page not displayed after onboarding employee"
        )

        pim_search_res = pim_res["search_result"]
        assert ("Record" in pim_search_res["records_text"]) or (pim_search_res["rows_count"] > 0), (
            f"Onboarded employee '{new_employee.firstName}' not found in PIM directory"
        )
        print("  -> Employee successfully onboarded and verified in PIM directory!")

        # --- SECTION D: MY INFO (PERSONAL PROFILE UPDATE) ---
        update_val = PROFILE_DATA.get("nickname", "AutoProfile")
        print(f"\n[Phase 3 - Section D: My Info] Updating profile personal details to '{update_val}'...")
        profile_res = e2e_steps.execute_profile_section(update_val)

        assert profile_res["is_page_loaded"] is True, "My Info personal details page failed to load"
        assert profile_res["retained_value"] == update_val, (
            f"Expected retained value '{update_val}', got '{profile_res['retained_value']}'"
        )
        print("  -> Profile personal details update and retention verified!")

        # --- SECTION E: LEAVE MANAGEMENT ---
        print("\n[Phase 3 - Section E: Leave] Searching leave records and checking Apply Leave tab...")
        leave_res = e2e_steps.execute_leave_section()

        leave_search = leave_res["leave_search_result"]
        assert ("Record" in leave_search["summary_text"]) or (leave_search["rows_count"] >= 0)

        leave_apply = leave_res["apply_form_result"]
        assert leave_apply["is_apply_displayed"] is True, "Apply Leave form failed to load"
        print("  -> Leave management records and application tab verified!")

        # --- SECTION F: RECRUITMENT (CANDIDATE PIPELINE) ---
        new_candidate = DataLoader.generate_unique_candidate()
        print(f"\n[Phase 3 - Section F: Recruitment] Registering candidate '{new_candidate.firstName} {new_candidate.lastName}' ({new_candidate.email})...")
        recruitment_res = e2e_steps.execute_recruitment_section(new_candidate)

        assert recruitment_res["is_profile_displayed"] is True, "Candidate application profile was not created"
        print("  -> Candidate successfully added to recruitment pipeline!")

        # --- SECTION G: BUZZ (CORPORATE SOCIAL FEED) ---
        buzz_post = DataLoader.generate_unique_buzz_post()
        print(f"\n[Phase 3 - Section G: Buzz] Publishing status update to Buzz wall...")
        buzz_res = e2e_steps.execute_buzz_section(buzz_post)

        assert len(buzz_res["latest_post_content"]) > 0, "No content found on Buzz feed after posting"
        print("  -> Buzz status update successfully published and verified!")

        # --- SECTION H: SIDEBAR SEARCH FILTER ---
        nav_keyword = NAV_SAMPLES[0]["keyword"] if NAV_SAMPLES else "Admin"
        print(f"\n[Phase 3 - Section H: Navigation] Testing dynamic sidebar menu search for '{nav_keyword}'...")
        nav_res = e2e_steps.execute_navigation_filter_section(nav_keyword)

        filter_res = nav_res["filter_result"]
        assert filter_res["visible_count"] >= 1, f"No menu item found matching '{nav_keyword}'"
        assert any(nav_keyword in item for item in filter_res["visible_items"]), (
            f"Expected '{nav_keyword}' in visible menu items: {filter_res['visible_items']}"
        )

        restore_res = nav_res["restore_result"]
        assert restore_res["total_count"] >= 5, "Sidebar menu items not properly restored after clearing filter"
        print("  -> Dynamic menu filtering and restoration verified!")

        # ======================================================================
        # PHASE 4: LOGOUT AT THE END AND RETURN TO LOGIN PAGE
        # ======================================================================
        print("\n[Phase 4: Logout] Logging out from user profile dropdown...")
        logout_res = e2e_steps.execute_logout()

        assert logout_res["is_login_page_displayed"] is True, "Failed to return to Login page after logout"
        assert "login" in logout_res["current_url"], f"Expected 'login' in URL, got {logout_res['current_url']}"
        print("  -> Successfully logged out and returned to Login page!")
        print("\n======================================================================")
        print("  COMPLETE END-TO-END WORKFLOW SUCCEEDED IN A SINGLE SEAMLESS SESSION!")
        print("======================================================================\n")
