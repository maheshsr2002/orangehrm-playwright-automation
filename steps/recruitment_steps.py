from pages.recruitment_page import RecruitmentPage
from data.models import CandidatePayload


class RecruitmentSteps:
    """
    Step Definitions / Test Logic Layer: Recruitment Candidate Pipeline.
    Chains candidate registration and search workflows.
    Contains NO final assertions.
    """

    def __init__(self, recruitment_page: RecruitmentPage):
        self.recruitment_page = recruitment_page

    def register_candidate(self, candidate: CandidatePayload) -> dict:
        """Navigates to recruitment, fills candidate form, saves, and returns state."""
        self.recruitment_page.navigate_to_recruitment()
        self.recruitment_page.click_add_button()
        self.recruitment_page.enter_first_name(candidate.firstName)
        if candidate.middleName:
            self.recruitment_page.enter_middle_name(candidate.middleName)
        self.recruitment_page.enter_last_name(candidate.lastName)
        self.recruitment_page.enter_email(candidate.email)
        if candidate.contactNumber:
            self.recruitment_page.enter_contact_number(candidate.contactNumber)

        self.recruitment_page.click_save()

        return {
            "is_profile_displayed": self.recruitment_page.is_candidate_profile_displayed(),
            "candidate_email": candidate.email
        }
