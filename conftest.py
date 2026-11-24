import os
import pytest
from pathlib import Path
from playwright.sync_api import Page, BrowserContext, Browser

from data.config import Config
from data.data_loader import DataLoader
from utils.helper import Helper

# Page Object Layer
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.header_component import HeaderComponent
from pages.sidebar_component import SidebarComponent
from pages.admin_page import AdminPage
from pages.pim_page import PIMPage
from pages.profile_page import ProfilePage
from pages.leave_page import LeavePage
from pages.recruitment_page import RecruitmentPage
from pages.buzz_page import BuzzPage
from pages.time_page import TimePage

# Step Definitions / Test Logic Layer
from steps.auth_steps import AuthSteps
from steps.dashboard_steps import DashboardSteps
from steps.admin_steps import AdminSteps
from steps.pim_steps import PIMSteps
from steps.profile_steps import ProfileSteps
from steps.leave_steps import LeaveSteps
from steps.recruitment_steps import RecruitmentSteps
from steps.buzz_steps import BuzzSteps
from steps.navigation_steps import NavigationSteps
from steps.time_steps import TimeSteps
from steps.e2e_steps import E2ESteps


# ==============================================================================
# Configuration & Browser Lifecycle (conftest.py)
# ==============================================================================

def pytest_addoption(parser):
    """Adds custom command line flags."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode (overriding .env HEADLESS=false setting)"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Configures browser launch parameters, respecting CLI flags and .env."""
    is_headed = pytestconfig.getoption("--headed", default=False)
    is_headless_cli = pytestconfig.getoption("--headless", default=False)

    if is_headless_cli:
        headless_mode = True
    elif is_headed:
        headless_mode = False
    else:
        headless_mode = Config.HEADLESS

    cli_slowmo = pytestconfig.getoption("--slowmo", default=None)
    # In headless mode, default slow_mo to 0 for maximum execution speed
    if cli_slowmo is not None:
        slow_mo_val = cli_slowmo
    else:
        slow_mo_val = 0 if headless_mode else Config.SLOW_MO

    return {
        **browser_type_launch_args,
        "headless": headless_mode,
        "slow_mo": slow_mo_val,
        "args": ["--no-sandbox", "--disable-dev-shm-usage"]
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Sets standard viewport sizing, base URL, and video recordings."""
    args = {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
        "base_url": Config.BASE_URL,
    }
    if Config.VIDEO_RECORDING in ("on", "retain-on-failure"):
        Config.VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        args["record_video_dir"] = str(Config.VIDEOS_DIR)
    return args


@pytest.fixture(autouse=True)
def configure_page_timeouts(page: Page):
    """Configures timeouts, smooth scrolling, and visual mouse pointer indicators."""
    page.set_default_timeout(Config.DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(Config.NAVIGATION_TIMEOUT)

    try:
        page.add_init_script("""
            window.addEventListener('DOMContentLoaded', () => {
                const style = document.createElement('style');
                style.innerHTML = `
                    html { scroll-behavior: smooth !important; }
                    #playwright-visual-pointer {
                        position: fixed;
                        width: 26px;
                        height: 26px;
                        background: radial-gradient(circle, #ff2222 0%, #ff6600 100%);
                        border: 2.5px solid #ffffff;
                        box-shadow: 0 0 16px 4px rgba(255, 34, 0, 0.9);
                        border-radius: 50%;
                        z-index: 9999999;
                        pointer-events: none;
                        transition: all 0.3s cubic-bezier(0.2, 0.9, 0.3, 1.2);
                        transform: translate(-50%, -50%) scale(1);
                        display: none;
                    }
                `;
                document.head.appendChild(style);
            });
        """)
    except Exception:
        pass

    yield


# ==============================================================================
# Page Object Fixtures (pages/)
# ==============================================================================

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page: Page) -> DashboardPage:
    return DashboardPage(page)


@pytest.fixture
def header_component(page: Page) -> HeaderComponent:
    return HeaderComponent(page)


@pytest.fixture
def sidebar_component(page: Page) -> SidebarComponent:
    return SidebarComponent(page)


@pytest.fixture
def admin_page(page: Page) -> AdminPage:
    return AdminPage(page)


@pytest.fixture
def pim_page(page: Page) -> PIMPage:
    return PIMPage(page)


@pytest.fixture
def profile_page(page: Page) -> ProfilePage:
    return ProfilePage(page)


@pytest.fixture
def leave_page(page: Page) -> LeavePage:
    return LeavePage(page)


@pytest.fixture
def recruitment_page(page: Page) -> RecruitmentPage:
    return RecruitmentPage(page)


@pytest.fixture
def buzz_page(page: Page) -> BuzzPage:
    return BuzzPage(page)


@pytest.fixture
def time_page(page: Page) -> TimePage:
    return TimePage(page)


# ==============================================================================
# Step Definitions Layer Fixtures (steps/)
# ==============================================================================

@pytest.fixture
def auth_steps(login_page: LoginPage, dashboard_page: DashboardPage, header_component: HeaderComponent) -> AuthSteps:
    return AuthSteps(login_page, dashboard_page, header_component)


@pytest.fixture
def dashboard_steps(dashboard_page: DashboardPage) -> DashboardSteps:
    return DashboardSteps(dashboard_page)


@pytest.fixture
def admin_steps(admin_page: AdminPage) -> AdminSteps:
    return AdminSteps(admin_page)


@pytest.fixture
def pim_steps(pim_page: PIMPage) -> PIMSteps:
    return PIMSteps(pim_page)


@pytest.fixture
def profile_steps(profile_page: ProfilePage) -> ProfileSteps:
    return ProfileSteps(profile_page)


@pytest.fixture
def leave_steps(leave_page: LeavePage) -> LeaveSteps:
    return LeaveSteps(leave_page)


@pytest.fixture
def recruitment_steps(recruitment_page: RecruitmentPage) -> RecruitmentSteps:
    return RecruitmentSteps(recruitment_page)


@pytest.fixture
def buzz_steps(buzz_page: BuzzPage) -> BuzzSteps:
    return BuzzSteps(buzz_page)


@pytest.fixture
def navigation_steps(sidebar_component: SidebarComponent) -> NavigationSteps:
    return NavigationSteps(sidebar_component)


@pytest.fixture
def time_steps(time_page: TimePage) -> TimeSteps:
    return TimeSteps(time_page)


@pytest.fixture
def e2e_steps(
    auth_steps: AuthSteps,
    dashboard_steps: DashboardSteps,
    admin_steps: AdminSteps,
    pim_steps: PIMSteps,
    profile_steps: ProfileSteps,
    leave_steps: LeaveSteps,
    recruitment_steps: RecruitmentSteps,
    buzz_steps: BuzzSteps,
    navigation_steps: NavigationSteps,
) -> E2ESteps:
    return E2ESteps(
        auth_steps,
        dashboard_steps,
        admin_steps,
        pim_steps,
        profile_steps,
        leave_steps,
        recruitment_steps,
        buzz_steps,
        navigation_steps,
    )


# ==============================================================================
# Pre-Authenticated Session Fixture (storage_state support)
# ==============================================================================

@pytest.fixture
def authenticated_session(page: Page, auth_steps: AuthSteps, dashboard_steps: DashboardSteps):
    """
    Convenience fixture for tests requiring logged-in state.
    Uses AuthSteps to log in and returns page once Dashboard is verified.
    """
    res = auth_steps.execute_valid_login()
    assert res["is_dashboard_displayed"], "Failed to reach Dashboard during session authentication"
    return page


# ==============================================================================
# Failure Hook: Screenshots and Reporting
# ==============================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshot automatically upon test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture and Config.SCREENSHOT_ON_FAILURE:
            try:
                screenshot_path = Helper.take_screenshot(page_fixture, item.name)
                if hasattr(report, "extra"):
                    import pytest_html
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra = extra
            except Exception as e:
                print(f"Warning: Failed to capture failure screenshot: {e}")
