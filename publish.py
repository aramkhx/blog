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

SITE_NAME     = config.get("title", "My Blog")
SITE_NAME_HY  = config.get("title_hy", "")
SITE_URL      = config.get("domain", "")
TAGLINE       = config.get("tagline", "")
TAGLINE_HY    = config.get("tagline_hy", "")
AUTHOR        = config.get("author", "")
EMAIL         = config.get("email", "")
LINKEDIN      = config.get("linkedin", "")
GITHUB        = config.get("github", "")

# ── Armenian UI translations (edit these freely) ──
I18N = {
    'writing':       ('Writing',        'Հրապարակումներ'),
    'about':         ('About',          'Իմ Մասին'),
    'home':          ('\u2190 Home',     '\u2190 Գլխավոր'),
    'no_posts':      ('No posts yet',   'Դեռ հրապարակումներ չկան'),
    'no_posts_text': (
        'Nothing has been published just yet.<br/>Please check back soon &mdash; new writing is on the way.',
        'Դեռ ոչինչ չի հրապարակվել:<br/>Խնդրում եմ շուտով նորից այցելեք — նոր հրապարակումները ճանապարհին են:'
    ),
}

def i18n(key):
    """Return HTML with both EN and HY spans for a UI string."""
    en, hy = I18N[key]
    return f'<span class="i18n-en">{en}</span><span class="i18n-hy">{hy}</span>'


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
ICON_RSS = _SVG.format(
    '<path d="M4 11a9 9 0 0 1 9 9"/>'
    '<path d="M4 4a16 16 0 0 1 16 16"/>'
    '<circle cx="5" cy="19" r="1"/>'
)

# ── Globe icon for language toggle (Feather Icons) ──
ICON_GLOBE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/>'
    '<line x1="2" y1="12" x2="22" y2="12"/>'
    '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10'
    ' 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
    '</svg>'
)

# Inline scripts – kept tiny to stay lightweight
ANTI_FOUC = (
    "<script>"
    "(function(){"
    "var t=localStorage.getItem('theme')||"
    "(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');"
    "var l=localStorage.getItem('lang')||'en';"
    "var h=document.documentElement;"
    "h.setAttribute('data-theme',t);"
    "h.setAttribute('data-lang',l);"
    "var tl=h.getAttribute('data-title-'+l);"
    "if(tl)document.title=tl;"
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

LANG_JS = (
    "<script>"
    "(function(){"
    "var b=document.getElementById('lang-btn'),"
    "h=document.documentElement,"
    "label=document.getElementById('lang-label');"
    "if(label)label.textContent=h.getAttribute('data-lang')==='hy'?'HY':'EN';"
    "b.addEventListener('click',function(){"
    "var n=h.getAttribute('data-lang')==='en'?'hy':'en';"
    "h.setAttribute('data-lang',n);"
    "localStorage.setItem('lang',n);"
    "if(label)label.textContent=n==='en'?'EN':'HY';"
    "var tl=h.getAttribute('data-title-'+n);"
    "if(tl)document.title=tl;"
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


_HY_MONTHS = {
    1: '\u0540\u0578\u0582\u0576\u057e\u0561\u0580',
    2: '\u0553\u0565\u057f\u0580\u057e\u0561\u0580',
    3: '\u0544\u0561\u0580\u057f',
    4: '\u0531\u057a\u0580\u056b\u056c',
    5: '\u0544\u0561\u0575\u056b\u057d',
    6: '\u0540\u0578\u0582\u0576\u056b\u057d',
    7: '\u0540\u0578\u0582\u056c\u056b\u057d',
    8: '\u0555\u0563\u0578\u057d\u057f\u0578\u057d',
    9: '\u054d\u0565\u057a\u057f\u0565\u0574\u0562\u0565\u0580',
    10: '\u0540\u0578\u056f\u057f\u0565\u0574\u0562\u0565\u0580',
    11: '\u0546\u0578\u0575\u0565\u0574\u0562\u0565\u0580',
    12: '\u0534\u0565\u056f\u057f\u0565\u0574\u0562\u0565\u0580',
}


def fmt_date_hy(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{_HY_MONTHS[dt.month]} {dt.day}, {dt.year}"
    except Exception:
        return date_str


def i18n_date(date_str):
    return (
        f'<span class="i18n-en">{fmt_date(date_str)}</span>'
        f'<span class="i18n-hy">{fmt_date_hy(date_str)}</span>'
    )


def header(title, title_hy="", is_post=False, description="", active_page=""):
    prefix     = '../../../' if is_post else ''
    back       = f'<a class="back-link" href="{prefix}index.html">{i18n("home")}</a>' if is_post else ""
    page_title = title if title == SITE_NAME else f"{title} \u2014 {SITE_NAME}"
    # Armenian page title for browser tab
    if title == SITE_NAME:
        page_title_hy = SITE_NAME_HY or SITE_NAME
    elif title_hy and SITE_NAME_HY:
        page_title_hy = f"{title_hy} \u2014 {SITE_NAME_HY}"
    elif SITE_NAME_HY:
        page_title_hy = f"{title} \u2014 {SITE_NAME_HY}"
    else:
        page_title_hy = page_title
    desc_tag   = f'\n  <meta name="description" content="{description}"/>' if description else ""
    progress   = '<div class="reading-progress" id="reading-progress"></div>\n' if is_post else ''
    writing_cls = ' class="active"' if active_page == "writing" else ''
    about_cls   = ' class="active"' if active_page == "about" else ''

    # Tagline with i18n
    if TAGLINE:
        tagline_en = f'<span class="i18n-en">{TAGLINE}</span>'
        tagline_hy = f'<span class="i18n-hy">{TAGLINE_HY}</span>' if TAGLINE_HY else ''
        tagline = f'<p class="tagline">{tagline_en}{tagline_hy}</p>\n  '
    else:
        tagline = ""

    # Site title with i18n
    if SITE_NAME_HY:
        site_title_inner = f'<span class="i18n-en">{SITE_NAME}</span><span class="i18n-hy">{SITE_NAME_HY}</span>'
    else:
        site_title_inner = SITE_NAME

    return f"""<!DOCTYPE html>
<html lang="en" data-title-en="{page_title}" data-title-hy="{page_title_hy}">
<head>
  <meta charset="UTF-8"/>
  {ANTI_FOUC}
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{page_title}</title>{desc_tag}
  <link rel="stylesheet" href="{prefix}style.css"/>
  <link rel="icon" type="image/png" href="{prefix}images/website-icon.png">
  <link rel="alternate" type="application/rss+xml" title="{SITE_NAME} RSS Feed" href="{prefix}rss.xml"/>
</head>
<body>
{progress}<div class="container">
  <header>
    <p class="site-title"><a href="{prefix}index.html">{site_title_inner}</a></p>
    {tagline}<div class="header-row">
      <nav>
        <a href="{prefix}index.html"{writing_cls}>{i18n('writing')}</a>
        <a href="{prefix}about.html"{about_cls}>{i18n('about')}</a>
      </nav>
      <div class="header-buttons">
        <button class="lang-btn" id="lang-btn" aria-label="Toggle language">{ICON_GLOBE}<span class="lang-label" id="lang-label">EN</span></button>
        <button class="theme-btn" id="theme-btn" aria-label="Toggle theme">{ICON_MOON}{ICON_SUN}</button>
      </div>
    </div>
  </header>
  <hr class="header-rule"/>
  {back}
"""


def page_footer(is_post=False):
    social = ""
    if EMAIL:
        social += f'<a href="mailto:{EMAIL}" class="social-link" title="Email">{ICON_EMAIL}</a>'
    if LINKEDIN:
        social += f'<a href="{LINKEDIN}" class="social-link" title="LinkedIn" rel="noopener noreferrer" target="_blank">{ICON_LINKEDIN}</a>'
    if GITHUB:
        social += f'<a href="{GITHUB}" class="social-link" title="GitHub" rel="noopener noreferrer" target="_blank">{ICON_GITHUB}</a>'
    social += f'<a href="{SITE_URL}/rss.xml" class="social-link" title="RSS Feed" rel="noopener noreferrer" target="_blank">{ICON_RSS}</a>'

    social_html = f'<div class="footer-social">{social}</div>' if social else ""
    progress_script = PROGRESS_JS if is_post else ""

    return f"""  <footer>
    {social_html}
  </footer>
{THEME_JS}
{LANG_JS}
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
    """Remove first # heading from markdown body since the title is already shown in the post header."""
    lines = body.lstrip('\n').split('\n')
    if lines and re.match(r'^#\s+', lines[0]):
        return '\n'.join(lines[1:]).lstrip('\n')
    return body


def load_armenian_post(slug):
    """Try to load the Armenian (.hy.md) version of a post. Returns (meta, html_body) or None."""
    hy_path = os.path.join(POSTS_DIR, slug + '.hy.md')
    if not os.path.exists(hy_path):
        return None
    with open(hy_path) as f:
        raw = f.read()
    meta, body = extract_metadata(raw)
    if meta.get('title'):
        body = strip_leading_h1(body, meta['title'])
    html_body = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    return meta, html_body


def build_posts():
    posts = []
    for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
        if not filename.endswith('.md'):
            continue
        # Skip Armenian translation files — they're loaded by their English counterpart
        if filename.endswith('.hy.md'):
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

        # Check for Armenian translation
        hy = load_armenian_post(slug)

        # Build post title with i18n if Armenian exists
        if hy:
            hy_meta, hy_html_body = hy
            title_html = (
                f'<span class="i18n-en">{meta["title"]}</span>'
                f'<span class="i18n-hy">{hy_meta.get("title", meta["title"])}</span>'
            )
        else:
            title_html = meta['title']

        page  = header(meta['title'], title_hy=hy_meta.get('title', '') if hy else '', is_post=True, description=meta.get('excerpt', ''), active_page="writing")
        page += f"""  <article>
    <div class="post-header">
      <h1>{title_html}</h1>
      <div class="post-meta">{i18n_date(date)}</div>
    </div>
"""
        if hy:
            page += f"""    <div class="post-content i18n-en">
{html_body}
    </div>
    <div class="post-content i18n-hy">
{hy_html_body}
    </div>
"""
        else:
            page += f"""    <div class="post-content">
{html_body}
    </div>
"""
        page += "  </article>\n"
        page += page_footer(is_post=True)

        with open(out_path, 'w') as f:
            f.write(page)
        print(f"  \u2705 Built: {out_path}")

        posts.append({
            'title': meta['title'],
            'title_hy': hy[0].get('title', '') if hy else '',
            'date':  date,
            'category': category,
            'path':  rel_path,
            'excerpt': meta.get('excerpt', ''),
            'excerpt_hy': hy[0].get('excerpt', '') if hy else '',
            'html_body': html_body,
        })

    return posts


def build_homepage(posts):
    page  = header(SITE_NAME, active_page="writing")

    if posts:
        items = ""
        for p in posts:
            # Post title with i18n
            if p.get('title_hy'):
                title_link = (
                    f'<span class="i18n-en">{p["title"]}</span>'
                    f'<span class="i18n-hy">{p["title_hy"]}</span>'
                )
            else:
                title_link = p['title']

            # Excerpt with i18n
            if p.get('excerpt') and p.get('excerpt_hy'):
                excerpt_html = (
                    f'\n      <p class="post-excerpt i18n-en">{p["excerpt"]}</p>'
                    f'\n      <p class="post-excerpt i18n-hy">{p["excerpt_hy"]}</p>'
                )
            elif p.get('excerpt'):
                excerpt_html = f'\n      <p class="post-excerpt">{p["excerpt"]}</p>'
            else:
                excerpt_html = ""

            items += f"""    <li>
      <time class="post-date">{i18n_date(p['date'])}</time>
      <a class="post-title-link" href="{p['path']}">{title_link}</a>{excerpt_html}
    </li>
"""
        page += f'<ul class="post-list">\n{items}</ul>\n'
    else:
        page += f"""  <div class="empty-state">
    <svg class="empty-icon" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10 9 9 9 8 9"/>
    </svg>
    <h2 class="empty-title">{i18n('no_posts')}</h2>
    <p class="empty-text"><span class="i18n-en">{I18N['no_posts_text'][0]}</span><span class="i18n-hy">{I18N['no_posts_text'][1]}</span></p>
  </div>
"""

    page += page_footer()

    os.makedirs(SITE_DIR, exist_ok=True)
    with open(os.path.join(SITE_DIR, 'index.html'), 'w') as f:
        f.write(page)
    print("  \u2705 Built: site/index.html")


def build_rss(posts):
    from xml.sax.saxutils import escape
    from email.utils import formatdate
    from calendar import timegm
    from time import strptime

    def to_rfc822(date_str):
        t = strptime(date_str, '%Y-%m-%d')
        return formatdate(timegm(t), usegmt=True)

    items = ""
    for p in posts:
        link = f"{SITE_URL}/{p['path']}"
        pub_date = to_rfc822(p['date'])
        description = escape(p['html_body'])
        items += f"""    <item>
      <title>{escape(p['title'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub_date}</pubDate>
      <category>{escape(p['category'])}</category>
      <description>{description}</description>
    </item>
"""

    now = formatdate(usegmt=True)
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(SITE_NAME)}</title>
    <link>{SITE_URL}</link>
    <description>{escape(TAGLINE)}</description>
    <language>en</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{items}  </channel>
</rss>
"""

    with open(os.path.join(SITE_DIR, 'rss.xml'), 'w') as f:
        f.write(rss)
    print("  \u2705 Built: site/rss.xml")


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
    print("  \u2705 Copied assets")


print("Building site...")
posts = build_posts()
build_homepage(posts)
build_rss(posts)
copy_assets()
print(f"\nDone \u2014 {len(posts)} post(s) built. Upload the site/ folder to Pinata.")
