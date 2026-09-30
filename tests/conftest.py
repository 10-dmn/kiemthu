
from datetime import datetime
import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:5000"

@pytest.fixture(scope="session")
def driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    
    driver = webdriver.Edge(options=edge_options)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # Create folder if absent
            os.makedirs("tests_reports/screenshots", exist_ok=True)

            # File name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = f"tests_reports/screenshots/{file_name}"

            # Save screenshot
            driver.save_screenshot(file_path)

            # Attach to report
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra.append(
                    extras.image(file_path, mime_type="image/png", label="Failure Screenshot")
                )
