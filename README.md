# Steady Focus Co. static site (local only, not published)

Plain HTML and CSS. No build step. Not pushed anywhere yet.

Pages: `index.html`, `about.html`, three product pages in `products/`, one honest comparison article in `guides/` (traffic-04 style, but fair: it says we sell one item on it), `sitemap.xml`, `robots.txt`, `style.css`.

## Placeholder base URL
Every canonical link, the sitemap and robots.txt use the placeholder `https://thassett618.github.io/steady-focus/`. If the real address differs, search and replace that string across the folder before publishing.

## Publish on GitHub Pages (needs Thomas's yes)
Run from PowerShell. It creates a public repo, so only run it once approved:

```powershell
cd D:\Claude\steady-focus-site; git init -b main; git add .; git commit -m "Steady Focus Co. site"; gh repo create THassett618/steady-focus --public --source . --push; gh api -X POST repos/THassett618/steady-focus/pages -f "source[branch]=main" -f "source[path]=/"
```

Then submit `https://thassett618.github.io/steady-focus/sitemap.xml` in Search Console and Bing Webmaster Tools.

## Add a page
1. Copy an existing page (a product page for a product, the guide for an article) and edit the `<title>`, meta description, canonical, the one `<h1>`, and the body.
2. Link to it from `index.html` or another page.
3. Add a `<url>` entry to `sitemap.xml`.
4. Only add a product page once its Whop checkout link returns 200 (`curl -s -o NUL -L -w "%{http_code}" <link>`).

## Honesty rules used
No reviews or testimonials (none exist yet), no invented numbers, no health claims, competitors named only where our research files hold a source, and every quote links to where it came from. Quotes come from the Money Engine `evidence` table (OPP-0043/44/45).

## Notes for Thomas
- Title tags run 55 to 69 characters, so Google may shorten a few.
- Products 2 and 3 have no `listing_url` yet (an open question to Thomas since 2026-10-09). Their pages link to the live Whop checkout, so publishing the site would make those links public.
