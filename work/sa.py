import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':700},device_scale_factor=2)
        await pg.goto('file:///home/claude/thailand-liveaboard-plan.html'); await pg.wait_for_timeout(300)
        el=await pg.query_selector('details.also'); await el.scroll_into_view_if_needed()
        await el.screenshot(path='/tmp/also_closed.png')
        await pg.click('details.also summary'); await pg.wait_for_timeout(300)
        await (await pg.query_selector('details.also summary')).screenshot(path='/tmp/also_open.png')
        await b.close()
asyncio.run(main())
