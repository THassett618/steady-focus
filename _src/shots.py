import sys
from playwright.sync_api import sync_playwright
pages=[('index','index.html'),('task','products/adhd-task-initiation-starter-kit.html'),('time','products/adhd-time-blindness-toolkit.html'),('guide','guides/adhd-planner-and-focus-tools-compared.html'),('about','about.html')]
with sync_playwright() as pw:
  b=pw.chromium.launch()
  for w,h,tag,dsf in ((390,844,'390',2),(1440,900,'1440',1)):
    ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=dsf)
    for n,f in pages:
      p=ctx.new_page(); p.goto('file:///D:/Claude/steady-focus-site/'+f,wait_until='networkidle'); p.wait_for_timeout(1600)
      p.screenshot(path=f'D:/Claude/steady-focus-site/_review/{n}-{tag}-fold.png')
      p.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0);document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');await new Promise(r=>setTimeout(r,700))}"); p.wait_for_timeout(5200)
      p.screenshot(path=f'D:/Claude/steady-focus-site/_review/{n}-{tag}-full.png',full_page=True)
      info=p.evaluate("""()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.top),Math.round(b.bottom)]};return {ovx:document.documentElement.scrollWidth-innerWidth,h1:r('h1'),fan:r('.fan'),price:r('.buy .price'),btn:r('.buy .btn'),font:document.fonts.check('800 20px "Bricolage Grotesque"')}}""")
      print(n,tag,info)
      if n in ('index','task','time'):
        for sel,lab in (('.vs','vs'),('#value','value'),('#get','get')):
          p.locator(sel).scroll_into_view_if_needed(); p.wait_for_timeout(4800 if lab=='vs' else 1800)
          p.locator(sel).screenshot(path=f'D:/Claude/steady-focus-site/_review/{n}-{tag}-{lab}.png')
      if n in ('index','task'):
        p.locator('#inside').scroll_into_view_if_needed(); p.wait_for_timeout(400); p.click('#next'); p.wait_for_timeout(180)
        p.locator('#inside').screenshot(path=f'D:/Claude/steady-focus-site/_review/{n}-{tag}-flip-mid.png')
        p.wait_for_timeout(900); p.click('#next'); p.wait_for_timeout(900)
        p.locator('#inside').screenshot(path=f'D:/Claude/steady-focus-site/_review/{n}-{tag}-flip-p3.png')
      p.close()
    ctx.close()
  b.close()
