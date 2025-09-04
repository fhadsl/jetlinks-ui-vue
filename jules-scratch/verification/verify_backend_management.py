from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Navigate to the application and log in
        page.goto("http://localhost:9101", timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)

        page.get_by_placeholder("请输入用户名").fill("admin")
        page.get_by_placeholder("请输入密码").fill("admin@123")
        page.get_by_role("button", name="登录").click()

        # Wait for navigation to the home page
        expect(page).to_have_url("http://localhost:9101/#/", timeout=60000)

        # 2. Go to the "服务管理" (Service Management) page
        page.locator(".user-info").click()
        page.get_by_role("menuitem", name="切换服务").click()
        page.get_by_role("menuitem", name="服务管理").click()
        expect(page).to_have_url("http://localhost:9101/#/backend-manager")

        # 3. Add a new backend service
        page.get_by_role("button", name="新增").click()
        page.get_by_label("名称").fill("Test Backend")
        page.get_by_label("地址").fill("http://test.backend.com/api")
        page.get_by_role("button", name="OK").click()

        # 4. Verify the new backend is in the table
        expect(page.get_by_role("cell", name="Test Backend")).to_be_visible()

        # 5. Switch to the new service
        page.locator(".user-info").click()
        page.get_by_role("menuitem", name="切换服务").click()
        # Find the menu item by the text content of its children
        page.locator('div.backend-sub-menu-item-title:has-text("Test Backend")').click()


        # 6. Verify that the page reloads and the new service is active
        expect(page).to_have_url("http://localhost:9101/#/", timeout=60000) # Should reload to home
        page.wait_for_load_state('networkidle')
        page.locator(".user-info").click()
        page.get_by_role("menuitem", name="切换服务").click()
        expect(page.locator('//div[contains(@class, "backend-sub-menu-item-title") and contains(., "Test Backend")]/div/span[contains(@class, "ant-tag-success")]')).to_be_visible()
        page.get_by_role("menuitem", name="服务管理").click() # Close the menu

        # 7. Go back to the "服务管理" page and delete the service
        page.get_by_role("button", name="删除").click()
        page.get_by_role("button", name="确定").click()


        # 8. Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as p:
    run(p)
