# OrangeHRM End-to-End Automation Testing Framework
### Built with Python, Playwright, and Pytest

A production-grade, modular, and data-driven End-to-End (E2E) test automation framework designed specifically for the [OrangeHRM Open Source Demo](https://opensource-demo.orangehrmlive.com/).

---

## 📋 Table of Contents
- [Overview](#overview)
- [Clean 5-Layer Architectural Standard](#clean-5-layer-architectural-standard)
- [Project Directory Structure](#project-directory-structure)
- [Centralized Test Data Layer](#centralized-test-data-layer)
- [Core Suites & Test Coverage](#core-suites--test-coverage)
- [Prerequisites & Setup](#prerequisites--setup)
- [Executing Tests](#executing-tests)
- [HTML Reports & Failure Screenshots](#html-reports--failure-screenshots)

---

## 🔍 Overview
This testing suite follows strict enterprise test architecture:
- **Playwright for Python**: Fast, reliable browser automation with built-in auto-waiting and web-first interactions.
- **Pytest**: Industry-standard test runner with markers, parameterization, and clean test isolation.
- **Page Object Model (POM)**: Every page object contains ONLY locators and low-level actions (no assertions).
- **Step Definitions Layer (`steps/`)**: Business action choreography without test assertions.
- **Centralized Test Data Layer (`data/`)**: Zero hardcoding, all inputs managed via dedicated JSON documents.

---

## 🏗️ Clean 5-Layer Architectural Standard

```
+-------------------------------------------------------------------------------------------------+
| 1. Test Data Layer (data/ & data/payloads/)                                                     |
|    - Central document: data/payloads/form_inputs.json (All text box inputs)                     |
|    - Payload files: users.json, employees.json, candidates.json, buzz_posts.json, etc.          |
|    - Direct access module: data/test_data.py & data/data_loader.py                              |
|    - Confidential credentials stored strictly in .env (ZERO hardcoding)                         |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| 2. Page Object Model Layer (pages/)                                                             |
|    - Pure Locators (# 1. Locators in __init__) and Actions (# 2. Actions)                       |
|    - Clean interactions (.fill, .click, .inner_text, .is_visible)                               |
|    - ZERO assertions and ZERO test logic inside page classes                                    |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| 3. Step Definitions / Test Logic Layer (steps/)                                                 |
|    - Chains multi-page actions (auth, admin, pim, leave, time, etc.)                            |
|    - ZERO assertions; returns extracted state dictionaries back to tests                        |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| 4. Tests & Assertions Layer (tests/)                                                            |
|    - Concise, readable test methods injecting step definitions & data models                    |
|    - ALL validation assertions reside exclusively here                                          |
|    - Strict test isolation & categorized with Pytest markers (@smoke, @regression, etc.)        |
+-----------------------------------------------+-------------------------------------------------+
                                                |
                                                v
+-------------------------------------------------------------------------------------------------+
| 5. Configuration & Fixtures Layer (conftest.py & pytest.ini)                                    |
|    - Injects all Page and Step fixtures, manages browser lifecycles                             |
|    - Injects smooth scroll behavior and visual glowing red target cursor                        |
|    - Generates HTML reports with auto-embedded failure screenshots and video recordings         |
+-------------------------------------------------------------------------------------------------+
```

---

## 📁 Project Directory Structure

```
├── .env                       <- Confidential credentials & runtime config (GITIGNORED)
├── .env.example               <- Template for team environment variables
├── .gitignore                 <- Protects secrets, cache, and test artifacts
├── pytest.ini                 <- Pytest CLI settings, markers, and HTML report config
├── requirements.txt           <- Python dependencies
├── conftest.py                <- Root fixtures (browser, page, isolated contexts, hooks)
├── package.json               <- Convenience npm run scripts
├── run_tests.py               <- Interactive Python test runner script
│
├── pages/                     <- Page Object Model (POM) layer (Locators + Actions ONLY)
│   ├── base_page.py           <- Common Playwright navigation and spinner wait
│   ├── login_page.py          <- Login selectors, auth actions, alerts, required errors
│   ├── dashboard_page.py      <- Landing page, breadcrumbs, dashboard widgets
│   ├── header_component.py    <- Profile dropdown, logout, user identity
│   ├── sidebar_component.py   <- Left navigation menu and search filter
│   ├── admin_page.py          <- System Users table, role/status filters, user CRUD
│   ├── pim_page.py            <- Employee List, Add Employee, login details toggle
│   ├── profile_page.py        <- My Info, personal details, nickname/other ID update
│   ├── leave_page.py          <- Leave list, apply leave form, date submission
│   ├── time_page.py           <- Timesheet view, hours submission, attendance punch in/out
│   ├── recruitment_page.py    <- Candidate records, vacancy dropdown, pipeline
│   └── buzz_page.py           <- Social feed status posts and timeline
│
├── steps/                     <- Step Definitions / Test Logic Layer (0 assertions)
│   ├── auth_steps.py          <- Login, negative cases, logout
│   ├── dashboard_steps.py     <- Dashboard widgets inspection
│   ├── admin_steps.py         <- User search, role/status filter, CRUD actions
│   ├── pim_steps.py           <- Employee onboarding, directory search, personal details
│   ├── profile_steps.py       <- Profile updates and persistence
│   ├── leave_steps.py         <- Apply leave, search leave list
│   ├── time_steps.py          <- Timesheet review, submit, punch in/out
│   ├── recruitment_steps.py   <- Candidate registration pipeline
│   ├── buzz_steps.py          <- Newsfeed posting
│   ├── navigation_steps.py    <- Sidebar menu filter and clear
│   └── e2e_steps.py           <- Master continuous end-to-end journey
│
├── data/                      <- Test Data Layer
│   ├── config.py              <- Dotenv config loader & secret validator
│   ├── models.py              <- Strongly-typed dataclasses for credentials & payloads
│   ├── data_loader.py         <- Central document loader
│   ├── test_data.py           <- Centralized text box inputs & shortcuts module
│   └── payloads/              <- Isolated JSON documents
│       ├── form_inputs.json   <- All text box inputs (names, IDs, dates, passwords, notes)
│       ├── users.json         <- Negative login cases & system user queries
│       ├── employees.json     <- Mock employee datasets
│       ├── candidates.json    <- Candidate applications
│       ├── buzz_posts.json    <- Buzz newsfeed status updates
│       ├── navigation.json    <- Sidebar navigation samples
│       └── expected_messages.json <- Centralized expected UI validation strings
│
├── tests/                     <- Direct Pytest test suites (All Assertions Reside Here)
│   ├── test_login.py          <- Valid login, invalid login, required fields, logout
│   ├── test_admin.py          <- User search, role/status filter, CRUD operations
│   ├── test_pim.py            <- Add employee, login details, search, update details
│   ├── test_leave.py          <- Apply leave, leave list, approval inspection
│   ├── test_time.py           <- Timesheet review, submit, punch in/out
│   ├── test_dashboard_navigation.py <- Dashboard widgets and sidebar filter
│   ├── test_my_info_profile.py <- Edit personal details & persistence
│   ├── test_recruitment_pipeline.py <- Add candidate into hiring pipeline
│   ├── test_buzz_feed.py      <- Post update to Buzz wall
│   ├── test_known_defects.py  <- Known OrangeHRM defects & edge cases (@pytest.mark.xfail)
│   └── test_e2e_complete_workflow.py <- Master continuous end-to-end user journey
│
├── utils/                     <- Helper utilities
│   └── helper.py              <- Screenshot capture, spinner handling, smooth scrolling
│
└── reports/                   <- Generated test reports
    ├── report.html            <- Self-contained HTML execution report
    ├── screenshots/           <- Captured on test failure automatically
    └── videos/                <- Recorded browser execution videos
```

---

## 🔒 Centralized Test Data Layer

All form text box inputs are maintained in **[data/payloads/form_inputs.json](file:///d:/HRM%20DEMO%20WEBSITE/data/payloads/form_inputs.json)** and imported via **[data/test_data.py](file:///d:/HRM%20DEMO%20WEBSITE/data/test_data.py)**:

```python
from data.test_data import EMPLOYEE_DATA, ADMIN_DATA, LEAVE_DATA, TIME_DATA

# In tests or step definitions:
first_name = EMPLOYEE_DATA["first_name"]
username   = ADMIN_DATA["search_username"]
leave_type = LEAVE_DATA["leave_type"]
hours      = TIME_DATA["hours"]
```

---

## 🧪 Core Suites & Test Coverage

| Test Suite | File | Focus Areas | Markers |
|---|---|---|---|
| **Authentication & Login** | `tests/test_login.py` | Valid login, negative cases (blank fields, invalid password, SQLi, XSS), forgot password, logout | `@smoke`, `@negative`, `@login`, `@logout` |
| **Admin Module** | `tests/test_admin.py` | User search, role filter (`Admin`/`ESS`), status filter (`Enabled`/`Disabled`), CRUD (Create, Read, Update, Delete) | `@smoke`, `@regression`, `@admin` |
| **PIM Module** | `tests/test_pim.py` | Add employee, create login credentials, search by Name & Employee ID, update sensitive personal details | `@smoke`, `@regression`, `@pim` |
| **Leave Module** | `tests/test_leave.py` | Apply for leave, date range selection, leave list queue search, approval/rejection inspection | `@smoke`, `@regression`, `@leave` |
| **Time Module** | `tests/test_time.py` | View timesheets, edit/submit hours, Attendance Punch In / Punch Out | `@smoke`, `@regression`, `@time` |
| **Complete Workflow** | `tests/test_e2e_complete_workflow.py` | Single continuous session journey through all modules, logging out at the end | `@e2e`, `@master_flow` |

---

## ⚙️ Prerequisites & Setup

### 1. Clone the repository & create virtual environment
```bash
# Clone repository
git clone <repository-url>
cd orangehrm-playwright-automation

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate
```

### 2. Install dependencies & Playwright browsers
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
```

### 3. Configure environment variables
Copy the template `.env.example` to `.env` and fill in your confidential credentials:
```bash
# Windows:
copy .env.example .env

# Linux / macOS:
cp .env.example .env
```

Ensure your `.env` contains:
```env
BASE_URL=https://opensource-demo.orangehrmlive.com
ADMIN_USERNAME=your_username_here
ADMIN_PASSWORD=your_password_here
BROWSER=chromium
HEADLESS=true
SLOW_MO=0
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=45000
SCREENSHOT_ON_FAILURE=true
VIDEO_RECORDING=retain-on-failure
```

---

## 🚀 Executing Tests

### Headless Mode (Standard / CI Friendly)
```bash
# 1. Run all tests in headless mode
pytest tests/ --headless -v

# 2. Run with self-contained HTML report
pytest tests/ --headless --html=reports/report.html --self-contained-html -v

# 3. Run by test marker (smoke, regression, negative, defects)
pytest -m smoke --headless -v
pytest -m negative --headless -v
pytest -m defects --headless -v

# 4. Run individual test modules
pytest tests/test_login.py --headless -v
pytest tests/test_admin.py --headless -v
pytest tests/test_pim.py --headless -v
pytest tests/test_leave.py --headless -v
pytest tests/test_time.py --headless -v
```

### Headed Mode (Visual Inspection & Debugging)
```powershell
# Run with visible browser and 1-second delay per interaction
pytest tests/test_e2e_complete_workflow.py --headed --slowmo 1000 -v
pytest tests/test_login.py --headed --slowmo 1000 -v
```

### Quick `npm` Shortcuts
```bash
npm run test:headless          # All tests in headless mode
npm run test:login:headless    # Login suite headless
npm run test:login             # Login suite headed with slowmo
npm run test:workflow          # Master E2E workflow headed
```

---

## 🌐 GitHub Actions CI Integration

This repository is pre-configured for cross-platform execution on GitHub Actions (`ubuntu-latest`):
- All path resolutions use `pathlib.Path` (no hardcoded Windows drive letters).
- `pytest.ini` defaults to headless execution and outputs HTML reports into `reports/`.
- Secrets are supplied via GitHub Repository Secrets (`ADMIN_USERNAME`, `ADMIN_PASSWORD`).

---

## 📊 HTML Reports & Screenshots
- HTML report is generated at `reports/report.html`.
- On any test failure, a full-page screenshot is automatically captured into `reports/screenshots/` and embedded into the HTML report.
