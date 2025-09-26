from playwright.sync_api import Page, expect

def test_task_lookup(page: Page):
    # 1. Arrange: Go to the application's homepage.
    page.goto("http://localhost:8000")

    # 2. Act: Enter a username and click the "Get Tasks" button.
    page.get_by_placeholder("Enter RuneScape Username").fill("TestUser")
    page.get_by_role("button", name="Get Tasks").click()

    # 3. Assert: Wait for the task list to be populated.
    # We expect the "completed-tasks" element to be visible, which indicates the data has been loaded.
    expect(page.locator("#completed-tasks")).to_be_visible()

    # 4. Screenshot: Capture the final result for visual verification.
    page.screenshot(path="jules-scratch/verification/verification.png")