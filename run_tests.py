#!/usr/bin/env python3
"""
Test Runner Script for OrangeHRM Automation Framework.
Executes the unified end-to-end master workflow in headed browser mode with slow_mo=1000ms delay:
1. Tests invalid credentials first (stays on login page).
2. Logs in with valid confidential credentials at last.
3. Continuously tests entire application sections in a single session:
   - Dashboard
   - Admin (User Search & Role Filtering)
   - PIM (Employee Onboarding & Directory Search)
   - My Info (Personal Details Update & Persistence)
   - Leave (Leave Records & Apply Form)
   - Recruitment (Candidate Pipeline)
   - Buzz (Corporate Wall Status Post)
   - Sidebar Navigation & Filter
4. Logs out at the end and returns to the login page.
"""
import sys
import subprocess
from pathlib import Path


def run_complete_workflow():
    project_root = Path(__file__).resolve().parent

    print("=" * 80)
    print("  ORANGEHRM UNIFIED MASTER END-TO-END WORKFLOW")
    print("  Phase 1: Invalid Logins Tested First (Negative Validations)")
    print("  Phase 2: Valid Confidential Login at Last (Valid Credentials from .env)")
    print("  Phase 3: Continuous Section Testing in a Single Session")
    print("  Phase 4: Final Logout and Return to Login Page")
    print("  Mode: Headed Browser | SlowMo: 1000ms | Dynamic Response Waiting")
    print("=" * 80)

    # Command line arguments for pytest
    target = sys.argv[1] if len(sys.argv) > 1 else "tests/test_e2e_complete_workflow.py"

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        target,
        "--headed",
        "--slowmo",
        "1000",
        "-v",
        "-s",
        "--html=reports/report.html",
        "--self-contained-html"
    ]

    print(f"\nExecuting: {' '.join(cmd)}\n")
    sys.stdout.flush()

    try:
        process = subprocess.run(cmd, cwd=str(project_root))
        sys.exit(process.returncode)
    except KeyboardInterrupt:
        print("\nTest run cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    run_complete_workflow()
