import pymupdf, glob, os
from PIL import Image, ImageFilter, ImageDraw
R='D:/Claude/open-manus-bot/projects/money-engine-cos/skills/digital-product/runs/'
sets={'focus':sorted(glob.glob('D:/MoneyEngine/bundle_adhd_planner/*.pdf')),
 'task':sorted(glob.glob(R+'adhd-task-initiation-kit/product/*.pdf')),
 'time':sorted(glob.glob(R+'adhd-time-blindness-kit/product/*.pdf'))}
out='img'
for k,fs in sets.items():
  for f in fs:
    name=k+'-'+os.path.basename(f)[3:-4].replace('_','-')
    pix=pymupdf.open(f)[0].get_pixmap(dpi=150)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    for w,suf in ((960,''),(420,'-sm')):
      h=round(im.height*w/im.width)
      im.resize((w,h),Image.LANCZOS).save(f'{out}/{name}{suf}.webp','WEBP',quality=82,method=6)
    print(name)
# OG images: teal field with fanned real pages
def og(slug,pages):
  W,H=1200,630
  bg=Image.new('RGB',(W,H),(31,111,107))
  angles=[-9,0,8]; xs=[300,600,900]
  for i,(p,a,x) in enumerate(zip(pages,angles,xs)):
    pg=Image.open(f'{out}/{p}.webp').convert('RGBA'); pg=pg.resize((380,round(pg.height*380/pg.width)),Image.LANCZOS)
    sh=Image.new('RGBA',(pg.width+80,pg.height+80),(0,0,0,0)); d=ImageDraw.Draw(sh); d.rectangle((40,52,pg.width+40,pg.height+52),fill=(10,40,38,120)); sh=sh.filter(ImageFilter.GaussianBlur(18))
    sh=sh.rotate(a,expand=True,resample=Image.BICUBIC); pr=pg.rotate(a,expand=True,resample=Image.BICUBIC)
    y=110+ (0 if i==1 else 40)
    bg.paste(sh,(x-sh.width//2,y-20),sh); bg.paste(pr,(x-pr.width//2,y),pr)
  bg.save(f'{out}/og-{slug}.jpg','JPEG',quality=84)
og('focus-bundle',['focus-daily-focus-planner','focus-dopamine-menu','focus-weekly-habit-tracker'])
og('task-kit',['task-micro-step-breakdown','task-five-minute-start-timer','task-one-task-at-a-time'])
og('time-kit',['time-time-block-card','time-stop-alarm-checklist','time-time-cost-estimator'])
# favicon from brand profile
Image.open('D:/Claude/open-manus-bot/projects/digital-products/brand/profile-800.png').convert('RGB').resize((180,180),Image.LANCZOS).save(f'{out}/apple-touch-icon.png')
