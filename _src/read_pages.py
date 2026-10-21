"""Guide + about pages: keep the existing honest copy (git HEAD), restyle into the new world."""
import re, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def old_main(path):
    src = subprocess.run(["git", "-C", str(ROOT), "show", f"d4218e8:{path}"], capture_output=True, text=True, encoding="utf-8").stdout
    m = re.search(r'<main class="wrap">(.*?)</main>', src, re.S)
    return m.group(1)


def fix_links(h, depth):
    r = "../" * depth
    h = h.replace(f'{r}products/adhd-focus-bundle.html', f'{r}index.html').replace('products/adhd-focus-bundle.html', 'index.html')
    h = re.sub(r'<table>', '<div class="tablewrap"><table>', h)
    h = h.replace('</table>', '</table></div>')
    return h


def build(read_page, P, KITS, BASE):
    # ---- guide ----
    g = old_main("guides/adhd-planner-and-focus-tools-compared.html")
    g = g.replace('<p class="crumbs"><a href="../index.html">Home</a> / Guide</p>',
                  '<p class="crumbs"><a href="../index.html">Home</a> / Guide</p>')
    g = g.replace("Updated 2026-10-16.", "Updated 2026-10-21.")
    cards = "".join(
        f'<a href="../{P[k]["file"]}"><img src="../img/{img}-sm.webp" alt="" width="420" height="543" loading="lazy">{n}<span>{b}</span></a>'
        for k, (n, b, img) in KITS.items())
    # replace the plain list of our three sets with picture cards of the real pages
    g = re.sub(r'(There are three sets, \$7 each:</p>)\s*<ul>.*?</ul>', r'\1<div class="inline-kit">' + cards + '</div>', g, flags=re.S)
    g = g.replace('href="https://whop.com/checkout/plan_5PKOyKxXjyidI" rel="noopener" target="_blank">See the ADHD Focus Bundle ($7)</a>',
                  'href="../index.html">See the ADHD Focus Bundle ($7)</a>')
    g = fix_links(g, 1)
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": "ADHD Planners and Focus Tools Compared: Which Type Fits How You Get Stuck",
           "datePublished": "2026-10-16", "dateModified": "2026-10-21", "image": BASE + "img/og-focus-bundle.jpg",
           "author": {"@type": "Organization", "name": "Steady Focus Co.", "url": BASE}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
              {"@type": "ListItem", "position": 2, "name": "Guide", "item": BASE + "guides/adhd-planner-and-focus-tools-compared.html"}]}]
    read_page("guides/adhd-planner-and-focus-tools-compared.html",
              "ADHD Planners and Focus Tools Compared: Which Type Fits You (2026)",
              "A fair comparison of paper planners, apps, sticky notes and small printables for ADHD planning trouble. We sell one item on it and say so.",
              "guide", g, ld)
    # ---- about ----
    a = old_main("about.html")
    a = fix_links(a, 0)
    a = a.replace('<p class="crumbs"><a href="index.html">Home</a> / About</p>', '<p class="crumbs"><a href="index.html">Home</a> / About</p>')
    read_page("about.html", "About Steady Focus Co.: Small Printable Planning Tools",
              "Steady Focus Co. makes small printable pages for planning, starting tasks and keeping track of time. What we make, how we chose it, and what we don't do.",
              "about", a, [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About Steady Focus Co.", "url": BASE + "about.html"}], og="og-about.jpg", og_type="website")
