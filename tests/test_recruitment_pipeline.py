import pytest
from steps.recruitment_steps import RecruitmentSteps
from data.data_loader import DataLoader


@pytest.mark.recruitment
@pytest.mark.regression
class TestRecruitmentPipeline:
    """
    Tests & Assertions Layer: Recruitment Module (Candidate Pipeline).
    Responsibility: Validate registering new candidates into hiring pipeline.
    Data generated uniquely or fetched from candidates.json via DataLoader.
    """

    def test_add_candidate_end_to_end(self, authenticated_session, recruitment_steps: RecruitmentSteps):
        """
        E2E Test: Registers a candidate into recruitment pipeline and validates profile creation.
        """
        candidate = DataLoader.generate_unique_candidate()
        result = recruitment_steps.register_candidate(candidate)

        assert result["is_profile_displayed"] is True, "Candidate application profile was not created"
        assert result["candidate_email"] == candidate.email
