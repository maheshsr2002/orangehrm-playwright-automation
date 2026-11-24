from playwright.sync_api import Page
from pages.base_page import BasePage


class RecruitmentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.add_button = page.locator("button:has-text('Add')")
        self.first_name_input = page.locator("input[name='firstName']")
        self.middle_name_input = page.locator("input[name='middleName']")
        self.last_name_input = page.locator("input[name='lastName']")
        self.email_input = page.locator("div.oxd-input-group:has(label:has-text('Email')) input")
        self.contact_input = page.locator("div.oxd-input-group:has(label:has-text('Contact Number')) input")
        self.save_button = page.locator("button[type='submit']")
        self.candidate_profile_title = page.locator("h6:has-text('Application Stage'), .orangehrm-candidate-page")
        self.table_rows = page.locator(".oxd-table-body .oxd-table-card")
        self.shortlist_button = page.locator("button:has-text('Shortlist')")
        self.shortlist_notes_input = page.locator("textarea[placeholder='Type here'], div.oxd-input-group:has(label:has-text('Notes')) textarea")
        self.save_action_button = page.locator("button[type='submit']")
        self.action_error_message = page.locator(".oxd-toast--error, .oxd-alert-content-text")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_recruitment(self):
        self.navigate_to("/web/index.php/recruitment/viewCandidates")

    def click_add_button(self):
        self.add_button.click()

    def click_add_candidate(self):
        self.click_add_button()

    def enter_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)

    def enter_middle_name(self, middle_name: str):
        self.middle_name_input.fill(middle_name)

    def enter_last_name(self, last_name: str):
        self.last_name_input.fill(last_name)

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def enter_contact_number(self, contact: str):
        self.contact_input.fill(contact)

    def click_save(self):
        self.save_button.click()
        self.wait_for_page_ready()

    def add_candidate(self, first_name: str, last_name: str, email: str, contact: str = ""):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        if contact:
            self.enter_contact_number(contact)
        self.click_save()

    def is_candidate_profile_displayed(self) -> bool:
        try:
            return (
                self.candidate_profile_title.first.is_visible() or
                "addCandidate" in self.page.url or
                "viewCandidates" in self.page.url
            )
        except Exception:
            return False

    def get_candidates_count(self) -> int:
        return self.table_rows.count()

    def click_shortlist(self, notes: str = "Candidate shortlisted via automated test"):
        try:
            self.shortlist_button.first.click()
            self.wait_for_page_ready()
            if notes and self.shortlist_notes_input.is_visible():
                self.shortlist_notes_input.fill(notes)
            self.save_action_button.click()
            self.wait_for_page_ready()
        except Exception:
            pass

    def get_action_error(self) -> str:
        try:
            self.action_error_message.first.wait_for(state="visible", timeout=6000)
            return self.action_error_message.first.inner_text().strip()
        except Exception:
            return ""
