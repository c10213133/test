import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':390,'height':1000},device_scale_factor=1.5)
        await pg.goto('file:///home/claude/thailand-liveaboard-plan.html'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='/tmp/t1.png')
        await pg.click('.tab[data-t="2"]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path='/tmp/t2.png',full_page=True)
        await b.close()
asyncio.run(main())
