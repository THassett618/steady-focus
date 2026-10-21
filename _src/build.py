"""Build the Steady Focus Co. sales pages from one lander structure.

Structure = SOP assets/NoPopLander.html (pre-headline pill, headline with highlighted span,
sub-headline, media block, CTA area with security note, green-check bullet box, footer)
+ page-01 Gemini prompt requirements (logo + badge header, the "stack" box, desktop side
panel, mobile sticky Get-it bar). Copy comes from _sop/<slug>.md (hook-01..03 outputs).

Run:  python _src/build.py   (from D:\\Claude\\steady-focus-site)
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://thassett618.github.io/steady-focus/"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap" rel="stylesheet">')

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#fbf8f3"/>'
        '<path d="M7 20h18" stroke="#1f6f6b" stroke-width="2.4" stroke-linecap="round"/><circle cx="16" cy="20" r="4.2" fill="#d5794a"/>'
        '<path d="M10 12.5h12" stroke="#1f6f6b" stroke-width="2.4" stroke-linecap="round"/></svg>')
CHECK = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="currentColor" opacity=".12"/><path d="M7 12.5l3.2 3.2L17 9" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="currentColor" opacity=".12"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOCK = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 11V8a4 4 0 018 0v3" stroke="currentColor" stroke-width="2"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CYCLE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 12a8 8 0 11-2.3-5.6M20 4v4.5h-4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
QUOTE = '<svg viewBox="0 0 30 24" aria-hidden="true"><path fill="currentColor" d="M0 24V14C0 6 4.6 1.4 12 0l1.4 3.6C9 5 7 8 7 12h5v12H0zm17 0V14c0-8 4.6-12.6 12-14l1 3.6C26 5 24 8 24 12h5v12H17z"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'

e = html.escape

PRODUCTS = {}

PRODUCTS["focus"] = dict(
    file="index.html", path="", name="ADHD Focus Bundle", short="Focus Bundle", count="11",
    whop="https://whop.com/checkout/plan_5PKOyKxXjyidI", og="og-focus-bundle.jpg",
    title="ADHD Focus Bundle: 11 One-Job Printable Planner Pages, $7",
    desc="Your planner isn't the problem. Its size is. 11 printable ADHD planner pages that each do one job. Miss a day and nothing piles up. $7, instant PDF.",
    pre="Printable ADHD planner pages · instant PDF",
    h1='Your planner isn\'t the problem. <span class="mark">Its size is.</span>',
    sub="The ADHD Focus Bundle is 11 small printable pages. Each one does one job and stands on its own, so a missed day leaves nothing to catch up on.",
    btn="Get the 11 pages",
    fan=["focus-daily-focus-planner", "focus-dopamine-menu", "focus-weekly-habit-tracker"],
    problem_h="Why planners end up in a drawer",
    problem_lede="We read what people wrote about planners they had paid for. The same complaint kept coming up, and it was never about willpower. It was upkeep.",
    quotes=[
        ("If you have more than 3 things to do in one day you will easily spend about an hour making sure everything is updated in the right place.",
         "A 1-out-of-5 Trustpilot rating of a digital planner", "https://www.trustpilot.com/review/productivitymethod.com", True),
        ("If your planner is a lot of work to keep up with, you're probably not going to stick with it.",
         "Neurodivergent Notes, \u201cWhy ADHDers fail at planning\u201d", "https://neurodivergentnotes.substack.com/p/why-adhders-fail-at-planning", False),
        ("It actually caused me more chaos than making my life easier.",
         "A 1-out-of-5 Trustpilot rating of the same digital planner", "https://www.trustpilot.com/review/productivitymethod.com", False),
        ("We forget what information lives where, and we update them sporadically because there's so much to keep up with.",
         "Neurodivergent Notes, on spreading plans across many apps and trackers", "https://neurodivergentnotes.substack.com/p/why-adhders-fail-at-planning", True),
    ],
    vs_h="One big planner, or eleven loose pages",
    vs_old=("One big planner", "Every page leans on the one before it. Miss Tuesday and Wednesday already starts behind. The thicker it gets, the louder the guilt.",
            '<div class="book" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><b>Week 3, Tuesday<em>3 days to catch up</em></b></div>'),
    vs_new=("Eleven loose pages", "Nothing is linked to anything else. Skip a day and nothing waits for you. Print the page you need today and ignore the rest.",
            '<div class="loose" aria-hidden="true"><img src="img/focus-meal-planner-sm.webp" alt="" width="420" height="543" loading="lazy"><img src="img/focus-daily-focus-planner-sm.webp" alt="" width="420" height="543" loading="lazy"><img src="img/focus-grocery-list-sm.webp" alt="" width="420" height="543" loading="lazy"></div>'),
    pages=[
        ("focus-daily-focus-planner", "Daily Focus Planner", "Three priorities (only three), time blocks from 07:00 to 18:00 and a brain-dump box."),
        ("focus-dopamine-menu", "Dopamine Menu", "When you're stuck, pick ONE thing off the list: a 2-minute tidy, a glass of water, one song."),
        ("focus-weekly-habit-tracker", "Weekly Habit Tracker", "A tick grid for the week. No streak to break, just a record of what got done."),
        ("focus-morning-routine-checklist", "Morning Routine", "The same order every morning, so there are fewer choices before you're awake."),
        ("focus-evening-wind-down", "Evening Wind-Down", "Clothes out, bag packed, tomorrow's top three written, lights out."),
        ("focus-meal-planner", "Simple Meal Planner", "A meal for each day, plus a backup for when there's no effort left."),
        ("focus-grocery-list", "Grocery List", "Sorted by aisle: produce, protein, dairy, pantry, frozen, household."),
        ("focus-medication-task-tracker", "Medication & Task Tracker", "Tick it when it's done, so you stop wondering whether you did."),
        ("focus-micro-chore-checklist", "Micro-Chore Checklist", "Chores cut small: clear ONE surface, start one load of laundry."),
        ("focus-monthly-reset", "Monthly Reset", "One thing that went well, one thing to adjust. Not a report card."),
        ("focus-how-to-print", "How to Print & Use", "Print sizes, paper, and how to reuse a page in a plastic sleeve."),
    ],
    stack_extra=["One combined PDF of all 11 pages, plus each page as its own file",
                 "US Letter size, prints fine on A4. Black and white is enough",
                 "Reuse any page: slip it in a plastic sleeve and use a dry-erase pen"],
    stack_preview=["focus-morning-routine-checklist", "focus-monthly-reset", "focus-micro-chore-checklist"],
    yes=["You've bought planners before and stopped using them within a week or two",
         "You like paper and want something you can pin to the fridge",
         "You want a few small pages, not a whole system to learn",
         "You'd rather skip a day than feel behind"],
    no=["You keep a big detailed planner happily. Keep it",
        "You want reminders, alarms or syncing. That's an app's job",
        "You have no printer and no tablet to write on"],
    faq=[
        ("What exactly do I get?", "11 printable pages: a quick-start sheet and 10 one-job pages. You get them as one combined PDF and as separate files, so you can print the whole set or just one page."),
        ("How do I get the files?", "Checkout is on Whop. As soon as you've paid, you're taken to your download folder. Nothing is posted to you."),
        ("Is it a subscription?", "No. It's $7 once. There's no app and no account to set up with us."),
        ("What size are the pages?", "US Letter (8.5 \u00d7 11 in). They print fine on A4 at 100% / actual size. Every page works in black and white."),
        ("Can I use it on a tablet?", "Yes, if you have a PDF app that lets you write on files. Most people print the page they need."),
        ("Is this medical advice?", "No. These are planning pages. They don't replace support from a doctor or clinician."),
    ],
    others=["task", "time"],
)

PRODUCTS["task"] = dict(
    file="products/adhd-task-initiation-starter-kit.html", path="products/adhd-task-initiation-starter-kit.html",
    name="ADHD Task-Initiation Starter Kit", short="Task-Initiation Kit", count="4",
    whop="https://whop.com/checkout/plan_PmRQsptBQyqsA", og="og-task-kit.jpg",
    title="ADHD Task-Initiation Starter Kit: Write the First Move, $7",
    desc="Your to-do list isn't missing tasks. It's missing the first move. 4 printable pages built around the first physical action and a 5-minute start. $7 PDF.",
    pre="Printable task-starting pages · instant PDF",
    h1='Your to-do list isn\'t missing tasks. <span class="mark">It\'s missing the first move.</span>',
    sub="Four printable pages that only ask two things: what is the first thing your hands do, and can you give it five minutes?",
    btn="Get the 4 pages",
    fan=["task-micro-step-breakdown", "task-five-minute-start-timer", "task-one-task-at-a-time"],
    problem_h="The task is on the list. You still haven't started.",
    problem_lede="People who use to-do apps describe the same wall. The list holds the goal. Nothing on it tells you how to begin.",
    quotes=[
        ("Standard to-do lists typically fail people with ADHD because they list what needs to be done without addressing how to start.",
         "Hello Klarity, \u201cBreaking the first step barrier\u201d", "https://www.helloklarity.com/post/breaking-the-first-step-barrier-how-micro-steps-can-help-adhd-brains-overcome-task-initiation-problems/", True),
        ("If I dont do them strictly in the same exact order daily...then they all get completely out of order!!! And then itll be super confusing.",
         "An App Store rating (2 of 5) of a to-do app, Finch", "https://apps.apple.com/us/app/finch-self-care-pet/id1528595748", False),
        ("I very much appreciate the breakdown tasks function.",
         "An App Store rating of Tiimo, on the one feature that helped", "https://apps.apple.com/us/app/tiimo-the-adhd-autism-app/id1480220328", False),
    ],
    vs_h="A goal, or a first move",
    vs_old=("Your to-do list says", "A goal. Your brain looks at it, finds nothing to grab, and the task waits another hour.",
            '<ul class="listcard" aria-hidden="true"><li><span class="box"></span><span class="stuck">Clean the kitchen</span></li><li><span class="box"></span>Start the report</li><li><span class="box"></span>Sort the post</li></ul>'),
    vs_new=("The Micro-Step page says", "The first three things your hands do, and five minutes on the clock. When the timer ends you're allowed to stop.",
            '<ul class="listcard" aria-hidden="true"><li><span class="box"></span><span><span class="stuck">Pick up the first cup</span></span></li><li><span class="box"></span>Run the hot tap</li><li><span class="box"></span>Wipe one counter <span class="hint">· 5 min, then stop if you want</span></li></ul><p class="example">Example filled in by us.</p>'),
    pages=[
        ("task-micro-step-breakdown", "Micro-Step Breakdown", "The task you're avoiding, then its first 3 physical actions. Actions, not goals."),
        ("task-five-minute-start-timer", "5-Minute Start Timer", "One small action for five minutes. When it ends: stop, or go again. Both count."),
        ("task-one-task-at-a-time", "One Task at a Time", "What you're doing right now, and a parking lot for everything that tries to interrupt."),
        ("task-how-to-use", "How to Use This Kit", "The whole method on one page, in five steps."),
    ],
    stack_extra=["One combined PDF, plus each page as its own file",
                 "US Letter size, prints fine on A4. Black and white is enough",
                 "Print a fresh Micro-Step page for every task you're stuck on"],
    stack_preview=["task-micro-step-breakdown", "task-five-minute-start-timer", "task-one-task-at-a-time"],
    yes=["You know exactly what needs doing and still can't start",
         "Big tasks feel like a wall, so you do everything else instead",
         "You want something on paper, away from your phone",
         "Five minutes sounds possible when an hour doesn't"],
    no=["You start easily and struggle to finish. This kit is only about starting",
        "You want reminders that nag you. Use an app or a phone alarm",
        "You have no printer and no tablet to write on"],
    faq=[
        ("What exactly do I get?", "4 printable pages: Micro-Step Breakdown, 5-Minute Start Timer, One Task at a Time, and a how-to-use page. One combined PDF plus separate files."),
        ("How do I get the files?", "Checkout is on Whop. As soon as you've paid, you're taken to your download folder. Nothing is posted to you."),
        ("Is it a subscription?", "No. It's $7 once. There's no app and no account to set up with us."),
        ("What size are the pages?", "US Letter (8.5 \u00d7 11 in). They print fine on A4 at 100% / actual size, in black and white."),
        ("Why only four pages?", "Because the kit only does one job: getting you started. More pages would be more to keep up with."),
        ("Is this medical advice?", "No. These are planning pages. They don't replace support from a doctor or clinician."),
    ],
    others=["focus", "time"],
)

PRODUCTS["time"] = dict(
    file="products/adhd-time-blindness-toolkit.html", path="products/adhd-time-blindness-toolkit.html",
    name="ADHD Time-Blindness Toolkit", short="Time-Blindness Toolkit", count="4",
    whop="https://whop.com/checkout/plan_emZpimXKpOva9", og="og-time-kit.jpg",
    title="ADHD Time-Blindness Toolkit: Plans With the Buffer Built In, $7",
    desc="Your planner assumes you can feel time passing. This one doesn't. 4 printable pages with a 50% buffer already added and a stop-alarm plan. $7 PDF.",
    pre="Printable time-planning pages · instant PDF",
    h1='Your planner assumes you can feel time passing. <span class="mark">This one doesn\'t.</span>',
    sub="Four printable pages where every time block already has 50% added, and the alarm is set for when to stop, not just when to start.",
    btn="Get the 4 pages",
    fan=["time-time-block-card", "time-stop-alarm-checklist", "time-time-cost-estimator"],
    problem_h="\u201cTen minutes,\u201d and then it's forty",
    problem_lede="People who use planning apps say the same thing. The schedule looks right. The times in it are wrong.",
    quotes=[
        ("They always get the time wrong like go to bed and make dinner 5 min and take a shower one hour.",
         "An App Store rating of the planning app Tiimo", "https://apps.apple.com/us/app/tiimo-the-adhd-autism-app/id1480220328", True),
        ("You sit down to answer one email, and an hour disappears. You meant to leave the house at 8:00, and somehow it is 8:40.",
         "Talkiatry, \u201cADHD time blindness\u201d", "https://www.talkiatry.com/blog/adhd-time-blindness", False),
        ("I had trouble with timing on my chores.",
         "An App Store rating of Tiimo", "https://apps.apple.com/us/app/tiimo-the-adhd-autism-app/id1480220328", False),
    ],
    vs_h="A blank grid, or a padded plan",
    vs_old=("A blank schedule grid", "It writes down your guess and calls it a plan. If the guess is short, the whole day runs late.",
            '<table class="minitable" aria-hidden="true"><tr><th>Time</th><th>Task</th></tr><tr><td>8:00</td><td>Shower</td></tr><tr><td>8:10</td><td>Breakfast</td></tr><tr><td>8:20</td><td>Leave</td></tr></table>'),
    vs_new=("The Time-Block Day Card", "Your guess, then the block you actually give it with 50% added, then what it really took. Next time, your guess is closer.",
            '<table class="minitable" aria-hidden="true"><tr><th>Task</th><th>I think</th><th>+50% block</th><th>Took</th></tr><tr><td>Shower</td><td>10 min</td><td class="plus">15 min</td><td>__</td></tr><tr><td>Breakfast</td><td>10 min</td><td class="plus">15 min</td><td>__</td></tr></table><p class="example">Example filled in by us.</p>'),
    pages=[
        ("time-time-block-card", "Time-Block Day Card", "Task, your guess, the block with 50% added, and what it actually took."),
        ("time-stop-alarm-checklist", "Stop-Alarm Checklist", "The 3 things you do the moment the alarm rings, plus a backup alarm time."),
        ("time-time-cost-estimator", "Time-Cost Estimator", "Your guess next to what the timer showed, for tasks you do every week."),
        ("time-how-to-use", "How to Use This Toolkit", "How the three pages work together, on one page."),
    ],
    stack_extra=["One combined PDF, plus each page as its own file",
                 "US Letter size, prints fine on A4. Black and white is enough",
                 "Print a new Day Card each morning, or reuse one in a plastic sleeve"],
    stack_preview=["time-time-block-card", "time-stop-alarm-checklist", "time-time-cost-estimator"],
    yes=["\u201cI'll be ready in ten minutes\u201d is almost never true",
         "You get lost in a task and look up an hour later",
         "You want a plan on paper that already allows for running over",
         "You'd like your time guesses to get more honest over time"],
    no=["You already plan time well and arrive early",
        "You want a phone to buzz you. Use your phone's alarm alongside this",
        "You have no printer and no tablet to write on"],
    faq=[
        ("What exactly do I get?", "4 printable pages: Time-Block Day Card, Stop-Alarm Checklist, Time-Cost Estimator and a how-to-use page. One combined PDF plus separate files."),
        ("How do I get the files?", "Checkout is on Whop. As soon as you've paid, you're taken to your download folder. Nothing is posted to you."),
        ("Is it a subscription?", "No. It's $7 once. There's no app and no account to set up with us."),
        ("Why 50%?", "It's a common rule of thumb: plan for half as long again as you think. If you think 20 minutes, block 30. The card does the sum for you."),
        ("What size are the pages?", "US Letter (8.5 \u00d7 11 in). They print fine on A4 at 100% / actual size, in black and white."),
        ("Is this medical advice?", "No. These are planning pages. They don't replace support from a doctor or clinician."),
    ],
    others=["focus", "task"],
)

KIT_BLURB = {
    "focus": ("ADHD Focus Bundle", "11 one-job pages instead of one big planner. For when planners get dropped.", "focus-daily-focus-planner"),
    "task": ("Task-Initiation Starter Kit", "For when the task is on the list and you still can't start.", "task-micro-step-breakdown"),
    "time": ("Time-Blindness Toolkit", "For when \u201cten minutes\u201d keeps turning into forty.", "time-time-block-card"),
}


def rel(depth):
    return "../" * depth


def head(title, desc, url, og, depth, extra_ld, og_type="product"):
    r = rel(depth)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#1f6f6b">
<meta property="og:site_name" content="Steady Focus Co.">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}img/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{r}style.css">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
</head>'''


def topbar(depth, current=None, badge=None):
    r = rel(depth)
    nav = [("Focus Bundle", f"{r}index.html", "focus"), ("Task Kit", f"{r}products/adhd-task-initiation-starter-kit.html", "task"),
           ("Time Kit", f"{r}products/adhd-time-blindness-toolkit.html", "time"), ("Guide", f"{r}guides/adhd-planner-and-focus-tools-compared.html", "guide")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a>' for t, h, k in nav)
    b = f'<span class="badge">{badge}</span>' if badge else ""
    return f'''<header class="top"><div class="wrap"><a class="logo" href="{r}index.html">{LOGO}Steady Focus Co.</a><nav aria-label="Main">{links}</nav>{b}</div></header>'''


def footer(depth):
    r = rel(depth)
    return f'''<footer><div class="wrap">
<a class="logo" href="{r}index.html">{LOGO}Steady Focus Co.</a>
<p>Printable planning pages. Not medical advice, and no replacement for support from a doctor or clinician.</p>
<p>Checkout and file delivery by Whop. We respect your privacy: this site has no tracking and no sign-up form.</p>
<p><a href="{r}about.html">About us</a> · <a href="{r}guides/adhd-planner-and-focus-tools-compared.html">ADHD planners and focus tools compared</a></p>
<p>&copy; 2026 Steady Focus Co.</p>
</div></footer>'''


def secure(dark=True):
    return (f'<p class="secure"><span>{LOCK}Secure checkout on Whop</span><span>{DOWN}Download right after paying</span>'
            f'<span>{CYCLE}$7 once, no subscription</span></p>')


def buy_button(p, label=None, cls="btn"):
    return f'<a class="{cls}" href="{p["whop"]}" rel="noopener">{e(label or p["btn"])} · $7 {ARROW}</a>'


def product_page(key):
    p = PRODUCTS[key]
    depth = p["file"].count("/")
    r = rel(depth)
    url = BASE + p["path"]
    ld = [
        {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["desc"],
         "image": BASE + "img/" + p["og"], "brand": {"@type": "Brand", "name": "Steady Focus Co."},
         "offers": {"@type": "Offer", "price": "7.00", "priceCurrency": "USD", "url": p["whop"], "availability": "https://schema.org/InStock"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    if key == "focus":
        ld.insert(0, {"@context": "https://schema.org", "@type": "Organization", "name": "Steady Focus Co.", "url": BASE, "logo": BASE + "img/apple-touch-icon.png"})
    f1, f2, f3 = p["fan"]
    fan = (f'<div class="fan" id="fan">'
           f'<img class="p1" src="{r}img/{f2}.webp" alt="" width="960" height="1242" fetchpriority="high">'
           f'<img class="p3" src="{r}img/{f3}.webp" alt="" width="960" height="1242" fetchpriority="high">'
           f'<img class="p2" src="{r}img/{f1}.webp" alt="The {e(p["pages"][0][1])} page from the {e(p["name"])}" width="960" height="1242" fetchpriority="high">'
           f'<div class="sticker" aria-hidden="true"><b>{p["count"]}</b><span>pages · PDF</span></div></div>')

    quotes = "".join(
        f'<figure class="q{" wide" if wide else ""}">{QUOTE}<blockquote>{e(t)}</blockquote>'
        f'<figcaption>{e(src)} · <a href="{u}" rel="noopener nofollow">source</a></figcaption></figure>'
        for t, src, u, wide in p["quotes"])

    tabs = "".join(
        f'<button class="tab" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="stage" data-src="{r}img/{img}.webp" data-alt="{e(t)} page" data-cap="{e(c)}">'
        f'<img src="{r}img/{img}-sm.webp" alt="" width="420" height="543" loading="lazy"><span class="tt"><strong>{e(t)}</strong><span>{e(c)}</span></span></button>'
        for i, (img, t, c) in enumerate(p["pages"]))
    first = p["pages"][0]

    stack_items = "".join(f"<li>{CHECK}<span><strong>{e(t)}</strong></span></li>" for _, t, _ in p["pages"]) + \
        "".join(f"<li>{CHECK}<span>{e(x)}</span></li>" for x in p["stack_extra"])
    prev = "".join(f'<img src="{r}img/{x}-sm.webp" alt="{e(dict((a, b) for a, b, _ in p["pages"])[x])} page" width="420" height="543" loading="lazy">' for x in p["stack_preview"])

    yes = "".join(f"<li>{CHECK}<span>{e(x)}</span></li>" for x in p["yes"])
    no = "".join(f"<li>{CROSS}<span>{e(x)}</span></li>" for x in p["no"])
    faq = "".join(f"<details><summary>{e(q)}{PLUS}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])

    def kit(k):
        n, b, img = KIT_BLURB[k]
        href = r + PRODUCTS[k]["file"]
        return (f'<a class="kit" href="{href}"><img src="{r}img/{img}-sm.webp" alt="" width="420" height="543" loading="lazy">'
                f'<div><h3>{e(n)}</h3><p>{e(b)}</p><span class="more">See the pages · $7</span></div></a>')
    kits = "".join(kit(k) for k in p["others"])

    o_t, o_p, o_demo = p["vs_old"]
    n_t, n_p, n_demo = p["vs_new"]

    body = f'''<body>
<!-- Built from the Digital Product SOP: lander template assets/NoPopLander.html (structure) + prompts/page-01 (stack box, desktop side panel, mobile sticky bar). Copy: _sop/*.md (hook-01, hook-02, hook-03). -->
{topbar(depth, key, "Instant PDF")}
<main>
<section class="hero" style="padding:0"><div class="wrap">
  <div class="hero-copy">
    <p class="pre">{e(p["pre"])}</p>
    <h1>{p["h1"]}</h1>
  </div>
  {fan}
  <div class="buy" id="buy">
    <div class="price" aria-label="Price: 7 US dollars"><small>$</small>7<span class="sr"> US dollars</span></div>
    {buy_button(p)}
    {secure()}
  </div>
  <p class="hero-sub">{e(p["sub"])}</p>
</div></section>

<section><div class="wrap">
  <h2>{e(p["problem_h"])}</h2>
  <p class="lede">{e(p["problem_lede"])}</p>
  <div class="quotes">{quotes}</div>
  <p class="fine">These are public reviews and articles about other products, quoted word for word and linked so you can check them. We have no customer reviews of our own to show yet.</p>
</div></section>

<section class="sand"><div class="wrap">
  <h2>{e(p["vs_h"])}</h2>
  <div class="vs">
    <div class="side old"><span class="tag">Before</span><h3>{e(o_t)}</h3><p>{e(o_p)}</p><div class="demo">{o_demo}</div></div>
    <div class="side new"><span class="tag">With the {e(p["short"])}</span><h3>{e(n_t)}</h3><p>{e(n_p)}</p><div class="demo">{n_demo}</div></div>
  </div>
</div></section>

<section id="inside"><div class="wrap">
  <h2>Every page, up close</h2>
  <p class="lede">These are the real pages you download. Tap one to see it full size.</p>
  <div class="viewer">
    <div class="tabs" role="tablist" aria-label="Pages in the {e(p["name"])}">{tabs}</div>
    <figure class="stage" id="stage" role="tabpanel" aria-live="polite">
      <img id="stage-img" src="{r}img/{first[0]}.webp" alt="{e(first[1])} page" width="960" height="1242" loading="lazy">
      <figcaption id="stage-cap">{e(first[2])}</figcaption>
    </figure>
  </div>
</div></section>

<section class="sand"><div class="wrap stack-wrap">
  <div class="stack">
    <h3>Everything in the {e(p["name"])}</h3>
    <ul class="checks">{stack_items}</ul>
    <div class="total">
      <div class="price"><small>$</small>7<span class="price-note">one time · instant download</span></div>
      {buy_button(p)}
    </div>
    {secure()}
  </div>
  <div class="preview-grid" aria-label="Page previews">{prev}</div>
</div></section>

<section><div class="wrap">
  <h2>Is this for you?</h2>
  <div class="fit">
    <div><h3>Yes, if</h3><ul class="checks">{yes}</ul></div>
    <div class="no"><h3>Probably not, if</h3><ul class="checks">{no}</ul></div>
  </div>
</div></section>

<section class="sand"><div class="wrap faq">
  <h2>Questions</h2>
  {faq}
</div></section>

<section><div class="wrap">
  <h2>Stuck somewhere else?</h2>
  <p class="lede">Two more small kits from Steady Focus Co. Same idea: a few pages, one job each, $7.</p>
  <div class="kits">{kits}</div>
</div></section>

<section class="close"><div class="wrap">
  <h2>{p["h1"].replace('<span class="mark">', '').replace('</span>', '')}</h2>
  <p>{e(p["sub"])}</p>
  {buy_button(p)}
  {secure()}
</div></section>
</main>

<div class="bar" id="bar" aria-hidden="true"><div class="t"><b>{e(p["short"])}</b>$7 · instant PDF</div>{buy_button(p, "Get it")}</div>
{footer(depth)}
<script>
(function(){{
  var fan=document.getElementById('fan'); if(fan) fan.classList.add('ready');
  var img=document.getElementById('stage-img'), cap=document.getElementById('stage-cap');
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  function pick(t){{
    tabs.forEach(function(x){{x.setAttribute('aria-selected', x===t?'true':'false');}});
    img.classList.add('swap');
    var n=new Image(); n.onload=function(){{img.src=t.dataset.src; img.alt=t.dataset.alt; cap.textContent=t.dataset.cap; requestAnimationFrame(function(){{img.classList.remove('swap');}});}}; n.src=t.dataset.src;
  }}
  tabs.forEach(function(t,i){{
    t.addEventListener('click',function(){{pick(t);}});
    t.addEventListener('keydown',function(ev){{var k=ev.key, j=-1; if(k==='ArrowDown'||k==='ArrowRight') j=(i+1)%tabs.length; if(k==='ArrowUp'||k==='ArrowLeft') j=(i-1+tabs.length)%tabs.length; if(j>-1){{ev.preventDefault(); tabs[j].focus(); pick(tabs[j]);}}}});
  }});
  var bar=document.getElementById('bar'), buy=document.getElementById('buy');
  if(bar && buy && 'IntersectionObserver' in window){{
    var seen=false;
    new IntersectionObserver(function(es){{es.forEach(function(en){{ if(en.isIntersecting) seen=true; var on=seen && !en.isIntersecting && en.boundingClientRect.top<0; bar.classList.toggle('show',on); bar.setAttribute('aria-hidden',on?'false':'true');}});}}).observe(buy);
  }}
}})();
</script>
</body>
</html>
'''
    out = ROOT / p["file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(p["title"], p["desc"], url, p["og"], depth, ld) + "\n" + body, encoding="utf-8")
    print("wrote", out)


def read_page(file, title, desc, current, main_html, ld, og="og-focus-bundle.jpg", og_type="article"):
    depth = file.count("/")
    url = BASE + file
    body = f'''<body>
{topbar(depth, current)}
<main class="read"><div class="wrap narrow">
{main_html}
</div></main>
{footer(depth)}
</body>
</html>
'''
    (ROOT / file).write_text(head(title, desc, url, og, depth, ld, og_type) + "\n" + body, encoding="utf-8")
    print("wrote", ROOT / file)


def redirect_bundle():
    # The old bundle URL now lives at the site root (index.html is the bundle's sales page).
    (ROOT / "products/adhd-focus-bundle.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>ADHD Focus Bundle | Steady Focus Co.</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{BASE}">
<meta http-equiv="refresh" content="0; url=../index.html"></head>
<body><p>The ADHD Focus Bundle page has moved: <a href="../index.html">see it here</a>.</p></body></html>
''', encoding="utf-8")


if __name__ == "__main__":
    for k in PRODUCTS:
        product_page(k)
    redirect_bundle()
    import read_pages
    read_pages.build(read_page, PRODUCTS, KIT_BLURB, BASE)
