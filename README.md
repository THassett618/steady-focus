# Steady Focus Co. site (rebuilt 2026-10-21, local only, not pushed)

Static HTML + one `style.css`. No framework. Fonts: Bricolage Grotesque (headings) and
Atkinson Hyperlegible (body), from Google Fonts. Base URL: https://thassett618.github.io/steady-focus/

## Which SOP prompts and template built each page

SOP: `D:\Claude\open-manus-bot\projects\money-engine-cos\skills\digital-product\SKILL.md`, Stage 3.

| Page | Lander template | Prompts run (outputs in `_sop\`) |
|---|---|---|
| `index.html`: ADHD Focus Bundle sales page | `assets\NoPopLander.html` | hook-01, hook-02, hook-03, page-01 → `_sop\adhd-focus-bundle.md` |
| `products\adhd-task-initiation-starter-kit.html` | `assets\NoPopLander.html` | hook-01, hook-02, hook-03, page-01 → `_sop\adhd-task-initiation-kit.md` |
| `products\adhd-time-blindness-toolkit.html` | `assets\NoPopLander.html` | hook-01, hook-02, hook-03, page-01 → `_sop\adhd-time-blindness-kit.md` |
| `guides\adhd-planner-and-focus-tools-compared.html` | none (an article, traffic-04) | copy kept from the first build (it was fair and sourced); restyled, real page pictures added |
| `about.html` | none | copy kept, restyled |
| `products\adhd-focus-bundle.html` | — | redirect to `index.html` (the bundle's page is now the home page) |

What was kept from the templates: NoPopLander's order (pre-headline pill, headline with a highlighted
phrase, sub-headline, media block, CTA with a security note, green-tick bullet box, footer with
copyright and privacy line). From page-01: logo + badge header, the "stack" box, a side panel on
desktop, and a sticky "Get it" bar on mobile.

What was changed, and why:
- The email form became a Whop buy button. Kit does not exist yet, and SKILL.md says the first sale
  goes straight to the Whop payment link.
- The pop-up modal (PopUpLander / page-01) was not built. With no form it would only add a step.
- The video block became a fan of the real product pages.

Not run: **hook-04** (needs live Instagram research, which the prompt says never to fake; the brand's
Instagram account does not exist yet, T-024). **page-02** is the post-sign-up email, so it does not
apply until Kit exists (`runs\<slug>\emails.json` already holds the drafts).

## Honesty rules used
- Every quote on a sales page is a row in the Money Engine `evidence` table (OPP-0043/44/45), quoted
  word for word with a link. They are labelled as reviews of *other* products, not ours.
- No reviews or testimonials of our own (none exist), no invented numbers, no money-back promise
  (neither Whop nor our own policy offers one), no health claims.
- The two worked examples (kitchen micro-steps, shower +50%) are labelled "Example filled in by us".

## Files
- `img\`: every product page rendered from the real PDFs (webp, 960px + 420px), OG images, icon.
- `_src\assets.py` makes the images. `_src\build.py` (+ `read_pages.py`) writes the pages.
  `_src\shots.py` takes the review screenshots into `_review\` (not committed).
- Folders starting with `_` are skipped by GitHub Pages (Jekyll), so they never go live.

## Rebuild
```powershell
cd D:\Claude\steady-focus-site; python _src\assets.py; python _src\build.py; python _src\shots.py
```

## Publishing (needs Thomas's yes)
The repo already exists (`origin` = github.com/THassett618/steady-focus). Publishing = `git push`.
Products 2 and 3 still have `listing_url: null` (Telegram question #9). Pushing makes their Whop
links public, the same as the first build did.
