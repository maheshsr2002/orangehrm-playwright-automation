from pages.profile_page import ProfilePage


class ProfileSteps:
    """
    Step Definitions / Test Logic Layer: My Info Profile.
    Chains profile navigation, field editing, and persistence saving.
    Contains NO final assertions.
    """

    def __init__(self, profile_page: ProfilePage):
        self.profile_page = profile_page

    def update_personal_profile(self, new_value: str) -> dict:
        """Navigates to My Info, enters new personal ID/nickname, and saves."""
        self.profile_page.navigate_to_my_info()
        is_loaded = self.profile_page.is_personal_details_page_loaded()
        self.profile_page.enter_nickname(new_value)
        self.profile_page.click_save_details()
        retained = self.profile_page.get_nickname_value()

        return {
            "is_page_loaded": is_loaded,
            "submitted_value": new_value,
            "retained_value": retained
        }

    def attempt_save_special_characters_name(self, invalid_name: str) -> dict:
        """Attempts to save invalid special characters in first name."""
        self.profile_page.navigate_to_my_info()
        self.profile_page.enter_first_name(invalid_name)
        self.profile_page.click_save_details()

        return {
            "submitted_name": invalid_name,
            "field_error": self.profile_page.get_first_name_field_error(),
            "toast_error": self.profile_page.get_toast_error_message()
        }

    def attempt_save_emoji_nickname(self, emoji_value: str) -> dict:
        """Saves Unicode/emoji in nickname field and checks persistence."""
        self.profile_page.navigate_to_my_info()
        self.profile_page.enter_nickname(emoji_value)
        self.profile_page.click_save_details()
        self.profile_page.page.reload()
        self.profile_page.wait_for_page_ready()

        return {
            "submitted_value": emoji_value,
            "retained_value": self.profile_page.get_nickname_value()
        }

    def attempt_self_emergency_contact(self, name: str, relationship: str, mobile: str) -> dict:
        """Attempts to add employee themselves as an emergency contact."""
        self.profile_page.navigate_to_my_info()
        self.profile_page.navigate_to_emergency_contacts()
        initial_count = self.profile_page.get_subrecords_count()
        self.profile_page.add_emergency_contact(name, relationship, mobile)
        new_count = self.profile_page.get_subrecords_count()

        return {
            "initial_count": initial_count,
            "new_count": new_count,
            "toast_error": self.profile_page.get_toast_error_message(),
            "field_error": self.profile_page.get_field_error_message()
        }

    def attempt_duplicate_dependent(self, name: str, relationship: str, dob: str) -> dict:
        """Attempts to add identical dependent twice."""
        self.profile_page.navigate_to_my_info()
        self.profile_page.navigate_to_dependents()
        count_before = self.profile_page.get_subrecords_count()
        # Add first time
        self.profile_page.add_dependent(name, relationship, dob)
        count_after_first = self.profile_page.get_subrecords_count()
        # Add identical second time
        self.profile_page.add_dependent(name, relationship, dob)
        count_after_second = self.profile_page.get_subrecords_count()

        return {
            "count_before": count_before,
            "count_after_first": count_after_first,
            "count_after_second": count_after_second,
            "toast_error": self.profile_page.get_toast_error_message()
        }
