import os
import time
from pathlib import Path
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from data.config import Config


class Helper:
    """Helper utilities for Playwright automation with visual scrolling and pointer indicators."""

    @staticmethod
    def take_screenshot(page: Page, test_name: str) -> str:
        """Captures a screenshot of the current page and saves it to reports/screenshots."""
        Config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        sanitized_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = Config.SCREENSHOTS_DIR / f"{sanitized_name}_{timestamp}.png"
        page.screenshot(path=str(file_path), full_page=True)
        return str(file_path)

    @staticmethod
    def wait_for_loading_spinner(page: Page, timeout: int = 15000):
        """Waits for OrangeHRM Oxygen UI loader spinner to disappear."""
        try:
            spinner = page.locator(".oxd-loading-spinner")
            if spinner.is_visible(timeout=1500):
                spinner.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass

    @staticmethod
    def wait_for_page_ready(page: Page, timeout: int = 15000):
        """
        Asks the page to wait until it completely responds:
        1. Waits for full DOM load state
        2. Waits for all active asynchronous network traffic to settle (networkidle)
        3. Waits for Oxygen UI loading spinner to vanish
        """
        try:
            page.wait_for_load_state("load", timeout=timeout)
        except Exception:
            pass

        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass

        Helper.wait_for_loading_spinner(page, timeout=timeout)

    @staticmethod
    def scroll_and_highlight(page: Page, locator: Locator):
        """
        1. Scrolls the target element smoothly into view (centered in viewport)
           so actions on lower sections of the page are clearly visible.
        2. Places a bright, glowing pointer cursor directly on the element.
        3. Outlines the element with an animated red/orange highlight ring.
        """
        try:
            # 1. Smoothly scroll into view centered
            locator.evaluate("""(el) => {
                el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
            }""")
            time.sleep(0.3)  # Brief pause so smooth scroll is clearly visible
        except Exception:
            try:
                locator.scroll_into_view_if_needed()
            except Exception:
                pass

        try:
            # 2. Render and position the glowing pointer cursor on target element
            locator.evaluate("""(el) => {
                let pointer = document.getElementById('playwright-visual-pointer');
                if (!pointer) {
                    pointer = document.createElement('div');
                    pointer.id = 'playwright-visual-pointer';
                    pointer.style.position = 'fixed';
                    pointer.style.width = '26px';
                    pointer.style.height = '26px';
                    pointer.style.background = 'radial-gradient(circle, #ff2222 0%, #ff6600 100%)';
                    pointer.style.border = '2.5px solid #ffffff';
                    pointer.style.boxShadow = '0 0 16px 4px rgba(255, 34, 0, 0.9)';
                    pointer.style.borderRadius = '50%';
                    pointer.style.zIndex = '9999999';
                    pointer.style.pointerEvents = 'none';
                    pointer.style.transition = 'all 0.3s cubic-bezier(0.2, 0.9, 0.3, 1.2)';
                    pointer.style.transform = 'translate(-50%, -50%) scale(1)';
                    document.body.appendChild(pointer);
                }

                const rect = el.getBoundingClientRect();
                const targetX = rect.left + rect.width / 2;
                const targetY = rect.top + rect.height / 2;

                pointer.style.left = `${targetX}px`;
                pointer.style.top = `${targetY}px`;
                pointer.style.display = 'block';
                pointer.style.opacity = '1';

                // Highlight target element with glowing outline
                el.dataset.prevOutline = el.style.outline || '';
                el.dataset.prevBoxShadow = el.style.boxShadow || '';
                el.dataset.prevOutlineOffset = el.style.outlineOffset || '';
                el.style.outline = '3px solid #ff3b30';
                el.style.outlineOffset = '2px';
                el.style.boxShadow = '0 0 12px 2px rgba(255, 59, 48, 0.7)';
            }""")
            time.sleep(0.2)  # Pause to let the user see what is being targeted
        except Exception:
            pass

    @staticmethod
    def pulse_and_unhighlight(page: Page, locator: Locator):
        """Pulses the visual pointer on click and removes the outline."""
        try:
            locator.evaluate("""(el) => {
                const pointer = document.getElementById('playwright-visual-pointer');
                if (pointer) {
                    pointer.style.transform = 'translate(-50%, -50%) scale(1.7)';
                    pointer.style.boxShadow = '0 0 24px 6px rgba(255, 255, 255, 1)';
                    setTimeout(() => {
                        if (pointer) {
                            pointer.style.transform = 'translate(-50%, -50%) scale(1)';
                            pointer.style.boxShadow = '0 0 16px 4px rgba(255, 34, 0, 0.9)';
                        }
                    }, 220);
                }
                setTimeout(() => {
                    if (el) {
                        el.style.outline = el.dataset.prevOutline || '';
                        el.style.boxShadow = el.dataset.prevBoxShadow || '';
                        el.style.outlineOffset = el.dataset.prevOutlineOffset || '';
                    }
                }, 350);
            }""")
        except Exception:
            pass

    @staticmethod
    def select_oxd_dropdown(page: Page, dropdown_locator: str, option_text: str, timeout: int = 5000):
        """
        Special helper to interact with OrangeHRM custom Oxygen UI dropdowns (.oxd-select-text).
        Scrolls into view, highlights with pointer, opens dropdown, highlights and selects option.
        """
        container = page.locator(dropdown_locator).first
        container.wait_for(state="visible", timeout=timeout)
        Helper.scroll_and_highlight(page, container)
        container.click()
        Helper.pulse_and_unhighlight(page, container)

        option = page.locator(f".oxd-select-dropdown .oxd-select-option:has-text('{option_text}')").first
        option.wait_for(state="visible", timeout=timeout)
        Helper.scroll_and_highlight(page, option)
        option.click()
        Helper.pulse_and_unhighlight(page, option)

        Helper.wait_for_page_ready(page, timeout=timeout)

    @staticmethod
    def get_toast_message(page: Page, timeout: int = 8000) -> str:
        """Retrieves text from the global toast notification (.oxd-toast)."""
        toast_selector = ".oxd-toast-content .oxd-text--toast-message"
        try:
            toast = page.locator(toast_selector).first
            toast.wait_for(state="visible", timeout=timeout)
            return toast.text_content().strip()
        except PlaywrightTimeoutError:
            return ""
