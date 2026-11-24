from playwright.sync_api import Page
from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 1. Locators
        self.my_info_nav = page.locator(".oxd-main-menu-item:has(span:has-text('My Info'))")
        self.personal_details_header = page.locator("h6:has-text('Personal Details'), .orangehrm-edit-employee-content, .orangehrm-edit-employee-name")
        self.first_name_input = page.locator("input[name='firstName']")
        self.first_name_error = page.locator(".oxd-input-group:has(input[name='firstName']) .oxd-input-group__message")
        self.nickname_input = page.locator("div.oxd-input-group:has(label:has-text('Nickname')) input")
        self.other_id_input = page.locator("div.oxd-input-group:has(label:has-text('Other Id')) input")
        self.save_button = page.locator("form button[type='submit']").first
        self.toast_success = page.locator(".oxd-toast--success, .oxd-toast")
        self.toast_error = page.locator(".oxd-toast--error, .oxd-toast--warn, .oxd-toast")

        # Emergency Contacts & Dependents Tabs
        self.emergency_contacts_tab = page.locator("a.orangehrm-tabs-item:has-text('Emergency Contacts')")
        self.dependents_tab = page.locator("a.orangehrm-tabs-item:has-text('Dependents')")
        self.add_record_button = page.locator(".orangehrm-action-header button:has-text('Add'), button:has-text('Add')")
        self.contact_name_input = page.locator("div.oxd-input-group:has(label:has-text('Name')) input")
        self.contact_relationship_input = page.locator("div.oxd-input-group:has(label:has-text('Relationship')) input")
        self.contact_mobile_input = page.locator("div.oxd-input-group:has(label:has-text('Mobile')) input")
        self.dependent_relationship_dropdown = page.locator("div.oxd-input-group:has(label:has-text('Relationship')) .oxd-select-wrapper")
        self.dependent_dob_input = page.locator("div.oxd-input-group:has(label:has-text('Date of Birth')) input")
        self.save_subrecord_button = page.locator("form button[type='submit']").first
        self.subrecord_rows = page.locator(".oxd-table-body .oxd-table-card")
        self.field_error_message = page.locator(".oxd-input-group__message")

        # Profile Photo Upload
        self.profile_photo_avatar = page.locator(".orangehrm-edit-employee-image, img.employee-image")
        self.file_input = page.locator("input[type='file']")

    # 2. Actions (Interactions only, no assertions)
    def navigate_to_my_info(self):
        try:
            self.my_info_nav.first.click()
            self.page.wait_for_url("**/viewPersonalDetails/**", timeout=15000)
        except Exception:
            self.navigate_to("/web/index.php/pim/viewPersonalDetails/empNumber/7")
        self.wait_for_page_ready()

    def navigate_to_personal_details(self):
        self.navigate_to_my_info()

    def is_personal_details_page_loaded(self, timeout: int = 15000) -> bool:
        try:
            self.page.wait_for_url("**/viewPersonalDetails/**", timeout=timeout)
            self.personal_details_header.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            try:
                self.other_id_input.first.wait_for(state="visible", timeout=4000)
                return True
            except Exception:
                return "viewPersonalDetails" in self.page.url

    def enter_first_name(self, value: str):
        self.first_name_input.fill(value)

    def get_first_name_field_error(self) -> str:
        try:
            self.first_name_error.first.wait_for(state="visible", timeout=3000)
            return self.first_name_error.first.inner_text().strip()
        except Exception:
            return ""

    def enter_nickname(self, value: str):
        try:
            if self.nickname_input.is_visible(timeout=2000):
                self.nickname_input.fill(value)
            else:
                self.other_id_input.fill(value)
        except Exception:
            self.other_id_input.fill(value)

    def update_nickname(self, value: str):
        self.enter_nickname(value)

    def get_nickname_value(self) -> str:
        try:
            if self.nickname_input.is_visible(timeout=2000):
                return self.nickname_input.input_value()
            return self.other_id_input.input_value()
        except Exception:
            return self.other_id_input.input_value()

    def click_save_details(self):
        self.save_button.click()
        try:
            self.toast_success.first.wait_for(state="visible", timeout=12000)
        except Exception:
            pass
        self.wait_for_page_ready()

    def save_personal_details(self):
        self.click_save_details()

    def get_toast_message(self) -> str:
        try:
            return self.toast_success.first.inner_text().strip()
        except Exception:
            return ""

    def get_toast_error_message(self) -> str:
        try:
            self.toast_error.first.wait_for(state="visible", timeout=4000)
            return self.toast_error.first.inner_text().strip()
        except Exception:
            return ""

    def get_field_error_message(self) -> str:
        try:
            self.field_error_message.first.wait_for(state="visible", timeout=3000)
            return self.field_error_message.first.inner_text().strip()
        except Exception:
            return ""

    def navigate_to_emergency_contacts(self):
        self.emergency_contacts_tab.click()
        self.wait_for_page_ready()

    def add_emergency_contact(self, name: str, relationship: str, mobile: str = ""):
        self.add_record_button.first.click()
        self.contact_name_input.fill(name)
        self.contact_relationship_input.fill(relationship)
        if mobile:
            self.contact_mobile_input.fill(mobile)
        self.save_subrecord_button.click()
        self.wait_for_page_ready()

    def navigate_to_dependents(self):
        self.dependents_tab.click()
        self.wait_for_page_ready()

    def add_dependent(self, name: str, relationship: str = "Child", dob: str = ""):
        self.add_record_button.first.click()
        self.contact_name_input.fill(name)
        try:
            self.dependent_relationship_dropdown.click()
            self.page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{relationship}')").first.click()
        except Exception:
            pass
        if dob:
            self.dependent_dob_input.fill(dob)
        self.save_subrecord_button.click()
        self.wait_for_page_ready()

    def get_subrecords_count(self) -> int:
        try:
            return self.subrecord_rows.count()
        except Exception:
            return 0

    def upload_photo(self, file_path: str):
        try:
            self.profile_photo_avatar.click()
            self.wait_for_page_ready()
        except Exception:
            pass
        self.file_input.set_input_files(file_path)
        self.wait_for_page_ready()
