import asyncio
from playwright.async_api import async_playwright

async def save_auth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://x.com/login")
        print("Login manually in the opened browser...")
        await page.wait_for_timeout(60000)  # 60 seconds to login
        await context.storage_state(path="auth.json")
        await browser.close()

asyncio.run(save_auth())
