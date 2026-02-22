#!/usr/bin/python3
import os, re
from datetime import datetime

# ── pip install markdown ──
import markdown

SITE_DIR  = "site"
POSTS_DIR = "posts"

# ── Read config ──
config = {}
with open("config.md") as f:
    for line in f:
        m = re.match(r'\[(\w+)\].*\((.*)\)', line.strip())
        if m:
            config[m.group(1)] = m.group(2)

SITE_NAME = config.get("title", "My Blog")
SITE_URL  = config.get("domain", "")
TAGLINE   = config.get("tagline", "")
AUTHOR    = config.get("author", "")
EMAIL     = config.get("email", "")
LINKEDIN  = config.get("linkedin", "")
GITHUB    = config.get("github", "")

# ── Social icon SVGs (Feather Icons, stroke-based) ──
_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{}</svg>'

ICON_EMAIL = _SVG.format(
    '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>'
    '<polyline points="22,6 12,13 2,6"/>'
)
ICON_LINKEDIN = _SVG.format(
    '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>'
    '<rect x="2" y="9" width="4" height="12"/>'
    '<circle cx="4" cy="4" r="2"/>'
)
ICON_GITHUB = _SVG.format(
    '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61'
    'c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1'
    'S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1'
    'A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7'
    'A3.37 3.37 0 0 0 9 18.13V22"/>'
)

# Inline scripts – kept tiny to stay lightweight
ANTI_FOUC = (
    "<script>"
    "(function(){"
    "var t=localStorage.getItem('theme')||"
    "(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');"
    "document.documentElement.setAttribute('data-theme',t);"
    "})();"
    "</script>"
)

THEME_JS = (
    "<script>"
    "(function(){"
    "var b=document.getElementById('theme-btn'),"
    "h=document.documentElement;"
    "b.addEventListener('click',function(){"
    "var n=h.getAttribute('data-theme')==='dark'?'light':'dark';"
    "h.setAttribute('data-theme',n);"
    "localStorage.setItem('theme',n);"
    "});"
    "})();"
    "</script>"
)

PROGRESS_JS = (
    "<script>"
    "(function(){"
    "var p=document.getElementById('reading-progress');"
    "if(!p)return;"
    "window.addEventListener('scroll',function(){"
    "var h=document.documentElement;"
    "var st=h.scrollTop||document.body.scrollTop;"
    "var sh=h.scrollHeight-h.clientHeight;"
    "p.style.width=sh?((st/sh)*100)+'%':'0%';"
    "});"
    "})();"
    "</script>"
)

# Theme toggle SVG icons (Feather Icons)
ICON_MOON = (
    '<svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
)
ICON_SUN = (
    '<svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="5"/>'
    '<line x1="12" y1="1" x2="12" y2="3"/>'
    '<line x1="12" y1="21" x2="12" y2="23"/>'
    '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>'
    '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>'
    '<line x1="1" y1="12" x2="3" y2="12"/>'
    '<line x1="21" y1="12" x2="23" y2="12"/>'
    '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>'
    '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>'
    '</svg>'
)


def fmt_date(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    except Exception:
        return date_str


def header(title, is_post=False, description="", active_page=""):
    prefix     = '../../../' if is_post else ''
    back       = f'<a class="back-link" href="{prefix}index.html">\u2190 Home</a>' if is_post else ""
    page_title = title if title == SITE_NAME else f"{title} \u2014 {SITE_NAME}"
    desc_tag   = f'\n  <meta name="description" content="{description}"/>' if description else ""
    tagline    = f'<p class="tagline">{TAGLINE}</p>\n  ' if TAGLINE else ""
    progress   = '<div class="reading-progress" id="reading-progress"></div>\n' if is_post else ''
    writing_cls = ' class="active"' if active_page == "writing" else ''
    about_cls   = ' class="active"' if active_page == "about" else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  {ANTI_FOUC}
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title}</title>{desc_tag}
  <link rel="stylesheet" href="{prefix}style.css"/>
  <link rel="icon" type="image/png" href="{prefix}images/website-icon.png">
</head>
<body>
{progress}<div class="container">
  <header>
    <p class="site-title"><a href="{prefix}index.html">{SITE_NAME}</a></p>
    {tagline}<div class="header-row">
      <nav>
        <a href="{prefix}index.html"{writing_cls}>Writing</a>
        <a href="{prefix}about.html"{about_cls}>About</a>
      </nav>
      <button class="theme-btn" id="theme-btn" aria-label="Toggle theme">{ICON_MOON}{ICON_SUN}</button>
    </div>
  </header>
  <hr class="header-rule"/>
  {back}
"""


def page_footer(is_post=False):
    domain_display = SITE_URL.replace("https://", "").replace("http://", "")
    domain_link = f'<a href="{SITE_URL}">{domain_display}</a>' if SITE_URL else ""
    sep = " · " if domain_link else ""

    social = ""
    if EMAIL:
        social += f'<a href="mailto:{EMAIL}" class="social-link" title="Email">{ICON_EMAIL}</a>'
    if LINKEDIN:
        social += f'<a href="{LINKEDIN}" class="social-link" title="LinkedIn" rel="noopener noreferrer" target="_blank">{ICON_LINKEDIN}</a>'
    if GITHUB:
        social += f'<a href="{GITHUB}" class="social-link" title="GitHub" rel="noopener noreferrer" target="_blank">{ICON_GITHUB}</a>'

    social_html = f'<div class="footer-social">{social}</div>' if social else ""
    progress_script = PROGRESS_JS if is_post else ""

    return f"""  <footer>
    {social_html}
  </footer>
{THEME_JS}
{progress_script}
</div>
</body>
</html>
"""


def extract_metadata(content):
    """Extract [key]: <> (value) metadata from top of .md file"""
    meta = {}
    lines = content.split('\n')
    body_start = 0
    for i, line in enumerate(lines):
        m = re.match(r'\[(\w+)\].*\((.*)\)', line.strip())
        if m:
            meta[m.group(1)] = m.group(2)
            body_start = i + 1
        elif line.strip() == '':
            if meta:
                body_start = i + 1
                break
    body = '\n'.join(lines[body_start:])
    return meta, body


def strip_leading_h1(body, title):
    """Remove first # heading from markdown body if it duplicates the post title."""
    lines = body.lstrip('\n').split('\n')
    if lines and re.match(r'^#\s+', lines[0]):
        heading_text = re.sub(r'^#+\s+', '', lines[0]).strip()
        if heading_text.lower() == title.lower():
            return '\n'.join(lines[1:]).lstrip('\n')
    return body


def build_posts():
    posts = []
    for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath) as f:
            raw = f.read()
        meta, body = extract_metadata(raw)
        if not meta.get('title') or not meta.get('date') or not meta.get('category'):
            print(f"  Skipping {filename} — missing title/date/category")
            continue

        body     = strip_leading_h1(body, meta['title'])
        html_body = markdown.markdown(body, extensions=['fenced_code', 'tables'])

        slug     = filename[:-3]
        category = meta['category'].lower()
        date     = meta['date']
        out_dir  = os.path.join(SITE_DIR, category, date)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, slug + '.html')
        rel_path = f"{category}/{date}/{slug}.html"

        page  = header(meta['title'], is_post=True, description=meta.get('excerpt', ''), active_page="writing")
        page += f"""  <article>
    <div class="post-header">
      <h1>{meta['title']}</h1>
      <div class="post-meta">{fmt_date(date)}</div>
    </div>
    <div class="post-content">
{html_body}
    </div>
  </article>
"""
        page += page_footer(is_post=True)

        with open(out_path, 'w') as f:
            f.write(page)
        print(f"  \u2705 Built: {out_path}")

        posts.append({
            'title': meta['title'],
            'date':  date,
            'path':  rel_path,
            'excerpt': meta.get('excerpt', ''),
        })

    return posts


def build_homepage(posts):
    page  = header(SITE_NAME, active_page="writing")

    if posts:
        items = ""
        for p in posts:
            excerpt_html = f'\n      <p class="post-excerpt">{p["excerpt"]}</p>' if p.get("excerpt") else ""
            items += f"""    <li>
      <time class="post-date">{fmt_date(p['date'])}</time>
      <a class="post-title-link" href="{p['path']}">{p['title']}</a>{excerpt_html}
    </li>
"""
        page += f'<ul class="post-list">\n{items}</ul>\n'
    else:
        page += """  <div class="empty-state">
    <svg class="empty-icon" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10 9 9 9 8 9"/>
    </svg>
    <h2 class="empty-title">No posts yet</h2>
    <p class="empty-text">Nothing has been published just yet.<br/>Please check back soon &mdash; new writing is on the way.</p>
  </div>
"""

    page += page_footer()

    os.makedirs(SITE_DIR, exist_ok=True)
    with open(os.path.join(SITE_DIR, 'index.html'), 'w') as f:
        f.write(page)
    print("  ✅ Built: site/index.html")


def copy_assets():
    import shutil
    for asset in ['style.css', 'about.html']:
        if os.path.exists(asset):
            shutil.copy(asset, os.path.join(SITE_DIR, asset))
    if os.path.exists('images'):
        dest = os.path.join(SITE_DIR, 'images')
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree('images', dest)
    print("  ✅ Copied assets")


print("Building site...")
posts = build_posts()
build_homepage(posts)
copy_assets()
print(f"\nDone — {len(posts)} post(s) built. Upload the site/ folder to Pinata.")
