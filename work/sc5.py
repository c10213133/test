import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':1100},device_scale_factor=1.5)
        await pg.goto('file:///home/claude/thailand-liveaboard-plan.html'); await pg.wait_for_timeout(400)
        await pg.click('.tab[data-t="3"]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='/tmp/j1.png')
        el=await pg.query_selector('#j1'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
        await el.screenshot(path='/tmp/j2.png')
        await b.close()
asyncio.run(main())
