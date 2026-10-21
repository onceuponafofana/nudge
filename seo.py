"""Search and analytics for nudgeforsleep.com (21 October 2026).

Adds titles, descriptions, social cards, Apple's App Store banner, structured
data (the app, the site, the FAQ), a visible FAQ on the home page and cookieless
PostHog. Safe to run more than once: each block is replaced, never duplicated.

    python3 seo.py
"""
import json, re, datetime

SITE = 'https://nudgeforsleep.com'
APP = 'https://apps.apple.com/app/id6801367643'
POSTHOG_KEY = 'phc_BzNkBLGnKegGDUaazmrknVLHCsNx7eCQDmVS86QN9ruP'   # public project key, same Nudge project as the app

FAQ = [
    ("How does Nudge help with snoring?",
     "Nudge listens for snoring through your iPhone. When it hears it, your Apple Watch (or your phone) gives a light tap, enough to roll you onto your side without waking you. Most people snore far less on their side."),
    ("Do I need an Apple Watch?",
     "No. The watch works best, but without one your iPhone gives the nudge instead. Keep it on the mattress or in a pocket so you can feel it."),
    ("What is Hush?",
     "Hush plays a soft masking sound on your partner's phone that rises when snoring starts and fades when it stops. It is tuned to cover snoring, not generic white noise."),
    ("Does my partner need to pay?",
     "No. One plan covers you both. Your partner joins free with an invite code."),
    ("How much does Nudge cost?",
     "Nudge is free for 7 days, then $29.99 a year or $4.99 a month, for both of you."),
    ("Is my audio uploaded?",
     "No. Recordings stay on your phone. Paired phones only share on and off signals, never audio, and there is no account."),
    ("Is Nudge a medical device?",
     "No. Nudge does not diagnose sleep apnea. If you snore loudly most nights, or someone has noticed pauses in your breathing, talk to a doctor."),
]

PAGES = {
    'index.html': dict(
        title='Nudge: Snoring App for Couples | Snore Tracker for Apple Watch',
        desc='Nudge hears snoring and taps the snorer onto their side with Apple Watch or iPhone, while Hush covers the rest for the person beside them. One plan for two. Free for 7 days.',
        path='/'),
    'support.html': dict(
        title='Nudge Support: Help with the Snoring App',
        desc='Help with Nudge: Apple Watch setup, Hush and your partner, subscriptions and refunds, and privacy. Email support@nudgeforsleep.com.',
        path='/support.html'),
    'privacy.html': dict(
        title='Privacy Policy: Nudge',
        desc='How Nudge handles your data. Recordings stay on your phone, no account, no audio uploaded.',
        path='/privacy.html'),
    'terms.html': dict(
        title='Terms of Use: Nudge',
        desc='Terms of use for Nudge, the snoring app for couples.',
        path='/terms.html'),
}


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'


def faq_schema():
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


APP_SCHEMA = {
    "@context": "https://schema.org", "@type": "MobileApplication",
    "name": "Nudge: Snore Tracker", "operatingSystem": "iOS, watchOS",
    "applicationCategory": "HealthApplication", "url": SITE + "/",
    "downloadUrl": APP, "installUrl": APP,
    "image": SITE + "/assets/icon.png",
    "description": PAGES['index.html']['desc'],
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
               "description": "Free for 7 days, then $29.99 a year or $4.99 a month for two people."},
    "publisher": {"@type": "Organization", "name": "Nudge", "url": SITE + "/",
                  "email": "support@nudgeforsleep.com", "logo": SITE + "/assets/icon.png"},
}
SITE_SCHEMA = {"@context": "https://schema.org", "@type": "WebSite", "name": "Nudge", "url": SITE + "/"}

POSTHOG = """<script>
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
if (!location.hostname.endsWith("github.io")) {
  posthog.init('KEY', {api_host:'https://us.i.posthog.com', persistence:'memory', person_profiles:'identified_only', autocapture:false, capture_pageview:true, capture_pageleave:true, disable_session_recording:true, disable_surveys:true, capture_dead_clicks:false, enable_heatmaps:false});
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="apps.apple.com"]');
    if (a) posthog.capture('app_store_click', {label: a.textContent.trim(), page: location.pathname});
  });
}
</script>""".replace('KEY', POSTHOG_KEY)


def head_block(name, meta):
    url = SITE + meta['path']
    tags = [
        f'<title>{meta["title"]}</title>',
        f'<meta name="description" content="{meta["desc"]}" />',
        f'<link rel="canonical" href="{url}" />',
        '<meta name="robots" content="index, follow" />',
        '<meta name="apple-itunes-app" content="app-id=6801367643" />',
        '<link rel="icon" href="assets/icon.png" />',
        '<link rel="apple-touch-icon" href="assets/icon.png" />',
        '<meta property="og:site_name" content="Nudge" />',
        f'<meta property="og:title" content="{meta["title"]}" />',
        f'<meta property="og:description" content="{meta["desc"]}" />',
        '<meta property="og:type" content="website" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:image" content="{SITE}/assets/story-result.png" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{meta["title"]}" />',
        f'<meta name="twitter:description" content="{meta["desc"]}" />',
        f'<meta name="twitter:image" content="{SITE}/assets/story-result.png" />',
    ]
    if name == 'index.html':
        tags += [jsonld(APP_SCHEMA), jsonld(SITE_SCHEMA), jsonld(faq_schema())]
    if name == 'support.html':
        tags += [jsonld(faq_schema())]
    tags.append(POSTHOG)
    return '<!-- seo:start -->\n' + '\n'.join(tags) + '\n<!-- seo:end -->'


FAQ_CSS = """      .faq { padding:40px 0 110px; }
      .faq h2 { font-size:clamp(42px,5vw,70px); margin-bottom:28px; }
      .faq details { border-top:1px solid var(--line); padding:18px 0; }
      .faq summary { cursor:pointer; font-size:19px; font-weight:750; list-style:none; }
      .faq summary::-webkit-details-marker { display:none; }
      .faq summary::after { content:"+"; float:right; color:var(--blue); font-weight:800; }
      .faq details[open] summary::after { content:"\\2212"; }
      .faq p { margin:10px 0 0; max-width:760px; color:#5f5f5f; font-size:17px; line-height:1.5; }
"""


def faq_section():
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'<!-- faq:start --><section id="faq" class="shell faq"><h2>Questions</h2>{items}</section><!-- faq:end -->'


for name, meta in PAGES.items():
    s = open(name).read()
    s = re.sub(r'\s*<!-- seo:start -->.*?<!-- seo:end -->', '', s, flags=re.S)
    # drop the old single tags this block now owns
    for pat in [r'\s*<title>.*?</title>', r'\s*<meta name="description"[^>]*>', r'\s*<link rel="canonical"[^>]*>',
                r'\s*<meta property="og:[^"]*"[^>]*>', r'\s*<link rel="icon"[^>]*>', r'\s*<meta name="theme-color"[^>]*>']:
        s = re.sub(pat, '', s)
    s = s.replace('</head>', head_block(name, meta) + '\n<meta name="theme-color" content="#FAFAF8" />\n</head>', 1)
    if name == 'index.html':
        s = re.sub(r'<!-- faq:start -->.*?<!-- faq:end -->', '', s, flags=re.S)
        s = s.replace('<section id="try"', faq_section() + '\n      <section id="try"', 1)
        if '.faq {' not in s:
            s = s.replace('      @media (max-width:800px)', FAQ_CSS + '      @media (max-width:800px)', 1)
    open(name, 'w').write(s)

today = datetime.date.today().isoformat()
urls = [('/', '1.0'), ('/support.html', '0.6'), ('/privacy.html', '0.3'), ('/terms.html', '0.3')]
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n' for p, pr in urls) + '</urlset>\n')
open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('done')
