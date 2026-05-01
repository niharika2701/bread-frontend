import pytest
import time
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def unique(base: str) -> str:
    return f"{base}{int(time.time() * 1000) % 100000}"


def register_and_login(page: Page, username: str, password: str = "password123"):
    """Helper: register a user and login, ending on the calculations page."""
    page.goto(f"{BASE_URL}/register")
    page.fill("#username", username)
    page.fill("#email", f"{username}@example.com")
    page.fill("#password", password)
    page.fill("#confirm", password)
    page.click("button")
    page.wait_for_timeout(600)

    page.goto(f"{BASE_URL}/login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button")
    page.wait_for_timeout(1200)
    page.goto(f"{BASE_URL}/calculations")
    page.wait_for_timeout(500)


class TestAddCalculation:

    def test_add_calculation_success(self, page: Page):
        register_and_login(page, unique("adduser"))
        page.fill("#add-a", "10")
        page.fill("#add-b", "5")
        page.select_option("#add-type", "Add")
        page.click("button.btn-add")
        page.wait_for_timeout(800)
        expect(page.locator("#add-message")).to_contain_text("15")

    def test_add_multiply(self, page: Page):
        register_and_login(page, unique("muluser"))
        page.fill("#add-a", "6")
        page.fill("#add-b", "7")
        page.select_option("#add-type", "Multiply")
        page.click("button.btn-add")
        page.wait_for_timeout(800)
        expect(page.locator("#add-message")).to_contain_text("42")

    def test_add_divide(self, page: Page):
        register_and_login(page, unique("divuser"))
        page.fill("#add-a", "100")
        page.fill("#add-b", "4")
        page.select_option("#add-type", "Divide")
        page.click("button.btn-add")
        page.wait_for_timeout(800)
        expect(page.locator("#add-message")).to_contain_text("25")

    def test_add_divide_by_zero_rejected(self, page: Page):
        register_and_login(page, unique("divzero"))
        page.fill("#add-a", "10")
        page.fill("#add-b", "0")
        page.select_option("#add-type", "Divide")
        page.click("button.btn-add")
        expect(page.locator("#add-message")).to_contain_text("zero")

    def test_add_missing_inputs_rejected(self, page: Page):
        register_and_login(page, unique("emptyuser"))
        page.click("button.btn-add")
        expect(page.locator("#add-message")).to_contain_text("numbers")


class TestBrowseCalculations:

    def test_browse_shows_added_calculations(self, page: Page):
        register_and_login(page, unique("browseuser"))
        page.fill("#add-a", "3")
        page.fill("#add-b", "4")
        page.select_option("#add-type", "Add")
        page.click("button.btn-add")
        page.wait_for_timeout(800)
        expect(page.locator("#calc-body")).to_contain_text("7")

    def test_browse_empty_state(self, page: Page):
        register_and_login(page, unique("emptystate"))
        expect(page.locator("#calc-body")).to_contain_text("No calculations yet")


class TestEditCalculation:

    def test_edit_calculation(self, page: Page):
        register_and_login(page, unique("edituser"))
        page.fill("#add-a", "5")
        page.fill("#add-b", "5")
        page.select_option("#add-type", "Add")
        page.click("button.btn-add")
        page.wait_for_timeout(800)

        page.click("button.btn-edit")
        page.wait_for_timeout(300)

        first_edit_a = page.locator("input[id^='edit-a-']").first
        first_edit_b = page.locator("input[id^='edit-b-']").first
        first_edit_type = page.locator("select[id^='edit-type-']").first

        first_edit_a.fill("10")
        first_edit_b.fill("3")
        first_edit_type.select_option("Multiply")

        page.click("button.btn-save")
        page.wait_for_timeout(800)
        expect(page.locator("#calc-body")).to_contain_text("30")


class TestDeleteCalculation:

    def test_delete_calculation(self, page: Page):
        register_and_login(page, unique("deluser"))
        page.fill("#add-a", "9")
        page.fill("#add-b", "3")
        page.select_option("#add-type", "Divide")
        page.click("button.btn-add")
        page.wait_for_timeout(800)

        expect(page.locator("#calc-body")).to_contain_text("3")
        page.click("button.btn-delete")
        page.wait_for_timeout(800)
        expect(page.locator("#calc-body")).to_contain_text("No calculations yet")


class TestUnauthenticated:

    def test_redirect_to_login_if_not_authenticated(self, page: Page):
        """Visiting /calculations without a token redirects to login."""
        page.goto(f"{BASE_URL}/calculations")
        page.wait_for_timeout(800)
        expect(page).to_have_url(f"{BASE_URL}/login")
