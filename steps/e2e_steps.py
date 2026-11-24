from steps.auth_steps import AuthSteps
from steps.dashboard_steps import DashboardSteps
from steps.admin_steps import AdminSteps
from steps.pim_steps import PIMSteps
from steps.profile_steps import ProfileSteps
from steps.leave_steps import LeaveSteps
from steps.recruitment_steps import RecruitmentSteps
from steps.buzz_steps import BuzzSteps
from steps.navigation_steps import NavigationSteps
from data.models import UserCredentials, EmployeePayload, CandidatePayload


class E2ESteps:
    """
    Step Definitions / Test Logic Layer: End-to-End Master Choreography.
    Chains all application sections into a complete user journey.
    Strict Rule: Contains NO final test assertions; returns step results to tests.
    """

    def __init__(
        self,
        auth_steps: AuthSteps,
        dashboard_steps: DashboardSteps,
        admin_steps: AdminSteps,
        pim_steps: PIMSteps,
        profile_steps: ProfileSteps,
        leave_steps: LeaveSteps,
        recruitment_steps: RecruitmentSteps,
        buzz_steps: BuzzSteps,
        navigation_steps: NavigationSteps,
    ):
        self.auth_steps = auth_steps
        self.dashboard_steps = dashboard_steps
        self.admin_steps = admin_steps
        self.pim_steps = pim_steps
        self.profile_steps = profile_steps
        self.leave_steps = leave_steps
        self.recruitment_steps = recruitment_steps
        self.buzz_steps = buzz_steps
        self.navigation_steps = navigation_steps

    def execute_negative_login_suite(
        self,
        valid_username: str,
        wrong_password: str,
        invalid_username: str,
        invalid_password: str
    ) -> dict:
        """Executes negative login attempts and returns extracted error states."""
        empty_res = self.auth_steps.execute_empty_credentials_attempt()
        wrong_pass_res = self.auth_steps.execute_login(valid_username, wrong_password)
        wrong_user_res = self.auth_steps.execute_login(invalid_username, invalid_password)

        return {
            "empty_credentials_result": empty_res,
            "wrong_password_result": wrong_pass_res,
            "wrong_user_result": wrong_user_res
        }

    def execute_valid_login(self, credentials: UserCredentials) -> dict:
        """Logs into application and returns dashboard landing metrics."""
        return self.auth_steps.execute_valid_login(credentials)

    def execute_dashboard_section(self) -> dict:
        """Inspects dashboard metrics and quick launch icons."""
        return self.dashboard_steps.inspect_dashboard()

    def execute_admin_section(self, target_username: str, role: str) -> dict:
        """Searches system users and filters by role."""
        search_res = self.admin_steps.search_system_user(target_username)
        filter_res = self.admin_steps.filter_by_role(role)
        self.admin_steps.reset_search_filters()
        return {
            "search_result": search_res,
            "role_filter_result": filter_res
        }

    def execute_pim_section(self, employee: EmployeePayload, search_keyword: str) -> dict:
        """Onboards employee and searches employee directory."""
        onboard_res = self.pim_steps.onboard_employee(employee)
        search_res = self.pim_steps.search_employee_directory(search_keyword)
        return {
            "onboard_result": onboard_res,
            "search_result": search_res
        }

    def execute_profile_section(self, new_val: str) -> dict:
        """Updates personal details and checks value retention."""
        return self.profile_steps.update_personal_profile(new_val)

    def execute_leave_section(self) -> dict:
        """Searches leave list and inspects apply leave form."""
        search_res = self.leave_steps.search_leave_records()
        apply_res = self.leave_steps.navigate_to_apply_leave()
        return {
            "leave_search_result": search_res,
            "apply_form_result": apply_res
        }

    def execute_recruitment_section(self, candidate: CandidatePayload) -> dict:
        """Registers a new candidate into hiring pipeline."""
        return self.recruitment_steps.register_candidate(candidate)

    def execute_buzz_section(self, post_content: str) -> dict:
        """Publishes status announcement to Buzz feed."""
        return self.buzz_steps.publish_status_post(post_content)

    def execute_navigation_filter_section(self, keyword: str) -> dict:
        """Filters sidebar menu and restores full menu."""
        filter_res = self.navigation_steps.filter_menu_by_keyword(keyword)
        restore_res = self.navigation_steps.restore_full_menu()
        return {
            "filter_result": filter_res,
            "restore_result": restore_res
        }

    def execute_logout(self) -> dict:
        """Logs out from user dropdown and returns final page state."""
        return self.auth_steps.execute_logout()
