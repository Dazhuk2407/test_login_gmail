import datetime
import logging

from playwright.sync_api import Playwright


logger = logging.getLogger(__name__)


class App:
    def __init__(self, playwright: Playwright):
        self.browser = playwright.firefox.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://mail.google.com")

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()

    def enter_user_email_or_phone_number(self, identifier):
        self.page.fill("input[type='email']", identifier)
        self.page.click("text=Next")

    def login(self, identifier, password):
        self.enter_user_email_or_phone_number(identifier)
        self.page.fill("input[type='password']", password)
        self.page.click("text=Next")

    def capture_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_path = f"../screenshots/screenshot_{timestamp}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot captured: {screenshot_path}")

    def check_gmail_inbox(self):
        try:
            self.page.wait_for_selector("text=Inbox")
            return self.page.query_selector("text=Inbox") is not None
        except Exception as e:
            self.capture_screenshot()
            logger.error("Error: Gmail login failed", exc_info=True)
            raise e

    def verify_field_not_found_message(self, message):
        try:
            self.page.wait_for_selector(f"text={message}")
            return self.page.query_selector(f"text={message}") is not None
        except Exception as e:
            self.capture_screenshot()
            logger.error(
                f"Error: Message '{message}' not found",
                exc_info=True
            )
            raise e

    def login_with_phone_number_and_password(self, mobile_number, password):
        self.enter_user_email_or_phone_number(mobile_number)
        self.page.wait_for_selector("//button[contains(@class, 'VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf')]")
        self.page.locator("//button[contains(@class, 'VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf')]").click()
        self.page.fill("input[type='password']", password)
        self.page.locator("//button[contains(@class, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf')]").click()
