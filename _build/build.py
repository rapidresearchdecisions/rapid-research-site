"""Builds the Rapid Research site pages.

Run from the repo root:  python3 _build/build.py
Edit copy in this file, then rebuild. Shared styles live in styles.css.
"""
import html, json, os, re
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, "_build", "fragments")
SITE = "https://rapid-research.com"

FORM_ID = "1FAIpQLSci1r40mZ8e9HO_UGi31vYxu5qBLl9QBHffaYD_DEqWpdEnog"
ENTRY_PKG = "1463049893"      # "Which package are you interested in?"
ENTRY_FOLLOW = "426517647"    # "How should I follow up?"
FOLLOW = {"call": "15-min audio call", "quote": "Email recommendation"}
NOT_SURE = "Not sure yet / free consultation"
CHECK_PKG = "Rapid UX Check, DIY tool ($49)"
EVALS_PKG = "AI evals (scoped on a call)"
CHECK_PRICE = "$49"
# Paste the Gumroad / Lemon Squeezy product link here once it exists; until then
# the buy button opens the request form with the check preselected.
CHECK_BUY_URL = None

STRIPE = {
    "teardown": "https://buy.stripe.com/8x29AU5mG03E4dzepo2sM00",
    "firstuse": "https://buy.stripe.com/7sY28s3ey5nY9xTfts2sM01",
    "diagnosis": "https://buy.stripe.com/00w8wQg1k9Ee7pL4OO2sM02",
    "sprint": "https://buy.stripe.com/6oU3cw8ySg2CfWhchg2sM05",
    "launch": "https://buy.stripe.com/00wcN6eXg5nY9xT1CC2sM04",
    "coaching": "https://buy.stripe.com/dRm6oIdTcbMmcK5fts2sM03",
}
PKG = {  # must match the Google Form options exactly
    "teardown": "Signup Teardown ($500)",
    "firstuse": "First-Use Test ($1,000)",
    "diagnosis": "Drop-off Diagnosis ($3,000)",
    "sprint": "Growth Research Sprint ($8,500)",
    "launch": "Launch & Fundraise Review ($12,000)",
    "coaching": "Customer Interview Coaching ($750)",
}


def frag(name):
    return open(os.path.join(FRAG, name)).read()


def form_link(prefix, pkg=NOT_SURE, follow=None):
    """Link to the homepage form with the package (and follow-up) preselected."""
    q = "pkg=" + quote_plus(pkg)
    if follow:
        q += "&follow=" + follow
    return f"{prefix}?{q}#consult"


import hashlib
CSS_VERSION = hashlib.md5(open(os.path.join(ROOT, "styles.css"), "rb").read()).hexdigest()[:8]


def head(title, desc, path, prefix, extra=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Rapid Research">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/img/og-image.png">
<link rel="icon" href="{prefix}img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}img/apple-touch-icon.png">
<meta name="theme-color" content="#072D59">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}styles.css?v={CSS_VERSION}">
{extra}</head>
<body>
"""


def nav(prefix):
    return f"""
<nav>
  <div class="wrap nav-in">
    <a href="{prefix or './'}" class="logo">Rapid Research</a>
    <div class="nav-links">
      <a href="{prefix}builders/">Solo builders</a>
      <a href="{prefix}startups/">Startups</a>
      <a href="{prefix}teams/">Teams &amp; investors</a>
      <a href="{prefix}ai-evals/">AI evals</a>
      <a href="{prefix}learn/">Learn</a>
      <a href="{form_link(prefix, follow='call')}" class="btn btn-mint">Free 15-min call</a>
    </div>
  </div>
</nav>
"""


def footer(prefix):
    f = frag("footer.html")
    f = f.replace('<div class="logo" style="margin-bottom:10px">Rapid Research</div>',
                  f'<a href="{prefix or "./"}" class="logo" style="margin-bottom:10px">Rapid Research</a>')
    links = (f'<nav class="foot-links" aria-label="Footer">'
             f'<a href="{prefix}builders/">Solo builders</a><a href="{prefix}startups/">Startups</a>'
             f'<a href="{prefix}teams/">Teams &amp; investors</a><a href="{prefix}ai-evals/">AI evals</a><a href="{prefix}learn/">Learn</a>'
             f'<a href="{prefix}check/">UX Check ({CHECK_PRICE})</a><a href="{prefix}sample-report.pdf">Sample report</a></nav>')
    f = f.replace('<p class="disc">', links + '\n    <p class="disc">')
    return "\n" + f + "\n</body>\n</html>\n"


def tier(key, speed, name, tagline, price, bullets, best, label, featured=False, badge=None):
    cls = "tier featured" if featured else "tier"
    btn = "btn-mint" if featured else "btn-ghost"
    b = f'\n        <span class="badge mono">{badge}</span>' if badge else ""
    lis = "\n".join(f"          <li>{x}</li>" for x in bullets)
    return f"""      <div class="{cls}">{b}
        <span class="speed mono">{speed}</span>
        <h3>{name}</h3>
        <p class="tagline">{tagline}</p>
        <div class="price">{price}</div>
        <ul>
{lis}
        </ul>
        <p class="best"><b>Best for:</b> {best}</p>
        <a href="{STRIPE[key]}" class="btn {btn}" target="_blank" rel="noopener">{label} →</a>
      </div>"""


def tiers_block(prefix, cards, cols="three-col"):
    out = f'    <div class="tiers {cols}">\n' + "\n\n".join(c for _, c in cards) + "\n    </div>"
    return out


def strip(prefix, text, more_href=None, more_text=None):
    more = f'<a class="more" href="{more_href}">{more_text}</a>' if more_href else ""
    return f"""    <div class="strip">
      <p>{text}</p>
      <div class="links">
        <a href="{html.escape(form_link(prefix, follow='call'))}" class="btn btn-mint">Book a free 15-min call</a>
        <a class="more" href="{prefix}sample-report.pdf" target="_blank" rel="noopener">See a sample report</a>
        {more}
      </div>
    </div>"""


TRUST_LINE = "PhD in human-AI interaction · Research experience at Meta and Microsoft · NDA on request"


def check_strip(prefix, text="Not ready to hire anyone? Check your product yourself."):
    return f"""    <a class="diy" href="{prefix}check/">
      <span class="diy-tag">DIY · {CHECK_PRICE}</span>
      <span class="diy-txt"><b>{text}</b> The Rapid UX Check is an AI tool that reviews your site or code and gives you the top 3 fixes, with the research behind each one.</span>
      <span class="diy-go">See the UX Check →</span>
    </a>"""


def page_hero(prefix, eyebrow, h1, lead, cta=None):
    btn = f'\n    <div class="hero-ctas" style="margin-top:26px">{cta}</div>' if cta else ""
    return f"""
<header class="page-hero">
  <div class="wrap">
    <a href="{prefix}" class="crumb">← All options</a><br>
    <span class="eyebrow mono">● {eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>{btn}
    <p class="hero-meta">{TRUST_LINE}</p>
  </div>
</header>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)


# ---------------------------------------------------------------- shared cards
C = {
 "teardown": lambda: tier("teardown", "⚡ 24 hours", "Signup Teardown",
    "My expert take on your product, as a brand-new user.", "$500",
    ["I go through one flow, like signup to first use",
     "Answers to up to 3 of your questions",
     "Every place people will get stuck, with screenshots and fixes"],
    "a quick gut check before you launch or share it.", "Book Teardown"),
 "firstuse": lambda featured=False, badge=None: tier("firstuse", "⚡ 24 hours", "First-Use Test",
    "Watch three real people try your product.", "$1,000",
    ["3 screen-and-voice recordings on tasks you choose",
     "Works with your live site, app, or prototype link",
     "Where they got stuck, with the clips to prove it"],
    "checking a flow before you build more.", "Book First-Use Test", featured, badge),
 "diagnosis": lambda featured=False, badge=None: tier("diagnosis", "5 business days", "Drop-off Diagnosis",
    "Five customer interviews on one problem.", "$3,000",
    ["Five 30-minute interviews with people like your users",
     "One problem, like signups, activation, or churn",
     "What's costing you users, and what to fix first"],
    "one metric that isn't moving.", "Book Diagnosis", featured, badge),
}

TL_SCRIPT = r"""<script>
(function(){
  var tl=document.querySelector(".tl"); if(!tl) return;
  function set(mode){
    tl.setAttribute("data-mode",mode);
    tl.querySelectorAll(".tl-toggle button").forEach(function(b){b.setAttribute("aria-pressed",b.getAttribute("data-set")===mode);});
    tl.querySelectorAll(".tl-bar").forEach(function(i){
      var v=i.getAttribute(mode==="rapid"?"data-r":"data-t").split(",");
      i.style.left=v[0]+"%"; i.style.width=v[1]+"%";
    });
  }
  tl.querySelectorAll(".tl-toggle button").forEach(function(b){b.addEventListener("click",function(){set(b.getAttribute("data-set"));});});
  // Play the comparison once when it scrolls into view
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(e){ if(e[0].isIntersecting){ setTimeout(function(){set("rapid");},700); io.disconnect(); } },{threshold:.5});
    io.observe(tl);
  }
})();
</script>"""

# ================================================================== HOME
def home():
    p = ""
    hero_report = frag("hero_report.html")
    st = frag("stats_trust.html")
    trust = st[st.index('<div class="trust">'):]
    ld = frag("ld.html")
    # keep the FAQ structured data in sync with the visible FAQ
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', ld, re.S)
    data = json.loads(m.group(1))
    faqs = re.findall(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', frag("faq.html"), re.S)
    clean = lambda x: html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
    data[1]["mainEntity"] = [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in faqs]
    ld = '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>'
    extra = ld + "\n"
    out = head("User Research in 24 Hours | Find Out Why Users Drop Off | Rapid Research",
               "Answers from real users in 24 hours, customer interviews in 5 days. Find out why users drop off, churn, or don't pay, without waiting weeks for an agency. From $500.",
               "/", p, extra)
    out += nav(p)
    out += f"""
<header class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow mono">● Customer research for startups</span>
        <h1>Know why users drop off <em>by tomorrow</em>, not next quarter.</h1>
        <p class="lead">Real users try your product in 24 hours. Customer interviews take 5 days. You get a clear list of what to fix first.</p>
        <div class="hero-ctas">
          <a href="#paths" class="btn btn-mint">Find your fit ↓</a>
          <a href="#consult" class="btn btn-ghost" data-pkg="{NOT_SURE}" data-follow="call">Book a free 15-min call</a>
        </div>
        <p class="hero-meta">From $500 · Fixed prices · NDA on request</p>
      </div>

      {hero_report}
    {trust}
  </div>
</header>

<section id="paths">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">Find your fit</span>
      <h2>Where are you right now?</h2>
      <p>Pick the one that sounds most like you.</p>
    </div>
    <div class="paths six">
      <a class="path" href="builders/">
        <span class="who">Solo founders &amp; indie devs</span>
        <h3>I'm building something on my own</h3>
        <p>Get an expert's honest take on what you're building, or learn to get feedback yourself.</p>
        <div class="foot"><span>From $500 · 24 hours</span><span>See options →</span></div>
      </a>
      <a class="path" href="startups/">
        <span class="who">Startups without a researcher</span>
        <h3>We need real user feedback, fast</h3>
        <p>Real people's reactions in 24 hours, or customer interviews in 5 days.</p>
        <div class="foot"><span>From $1,000 · 24 hours</span><span>See options →</span></div>
      </a>
      <a class="path" href="teams/">
        <span class="who">Funded teams &amp; investors</span>
        <h3>We want a researcher on call</h3>
        <p>Research sprints, ongoing fractional research, or support across a portfolio.</p>
        <div class="foot"><span>Sprints in 2–3 weeks</span><span>See options →</span></div>
      </a>
      <a class="path" href="ai-evals/">
        <span class="who">Teams building with AI</span>
        <h3>Is our AI actually any good?</h3>
        <p>Real people test your AI's answers, so you know if the new version is better before you ship.</p>
        <div class="foot"><span>From $3,000 · 5 days</span><span>See options →</span></div>
      </a>
      <a class="path" href="learn/">
        <span class="who">Researchers, designers &amp; PMs</span>
        <h3>I want to learn rapid research</h3>
        <p>Learn to run research fast without cutting corners, in a 1:1 coaching session.</p>
        <div class="foot"><span>$750 · within a week</span><span>See options →</span></div>
      </a>
      <a class="path diy-path" href="check/">
        <span class="who">Not ready to hire anyone?</span>
        <h3>I'll check it myself</h3>
        <p>An AI tool that reviews your site or code and gives you the top 3 fixes, with the research behind each one.</p>
        <div class="foot"><span>{CHECK_PRICE} · instant</span><span>See the UX Check →</span></div>
      </a>
    </div>
  </div>
</section>

<section id="speed" style="padding:72px 0 24px">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">Why speed matters</span>
      <h2>Answers while the decision is still open.</h2>
      <p>By the time a typical study reports back, you've already shipped.</p>
    </div>
    <div class="tl" data-mode="trad">
      <div class="tl-head">
        <div><h3>Getting answers about your users</h3><p>The same study, start to finish.</p></div>
        <div class="tl-toggle" role="group" aria-label="Compare timelines">
          <button type="button" data-set="trad" aria-pressed="true">Traditional research</button>
          <button type="button" data-set="rapid" aria-pressed="false">Rapid Research</button>
        </div>
      </div>
      <div class="tl-grid">
        <div class="tl-row tl-axis"><div class="tl-lab"></div><div class="tl-weeks"><span>Week 1</span><span>Week 2</span><span>Week 3</span><span>Week 4</span><span>Week 5</span><span>Week 6</span><em class="tl-marker" aria-hidden="true">Report · day 5</em></div></div>
        <div class="tl-row">
          <div class="tl-lab"><b>Scope the study</b><span>Kickoff calls and a research plan</span></div>
          <div class="tl-track" aria-hidden="true">
            <i class="tl-ghost" style="left:0.0%;width:21.67%"></i>
            <i class="tl-bar" data-t="0.0,21.67" data-r="0.0,2.0" style="left:0.0%;width:21.67%"></i>
          </div>
        </div>
        <div class="tl-row">
          <div class="tl-lab"><b>Recruit participants</b><span>Screener, scheduling, no-shows</span></div>
          <div class="tl-track" aria-hidden="true">
            <i class="tl-ghost" style="left:16.67%;width:36.67%"></i>
            <i class="tl-bar" data-t="16.67,36.67" data-r="1.67,5.83" style="left:16.67%;width:36.67%"></i>
          </div>
        </div>
        <div class="tl-row">
          <div class="tl-lab"><b>Run the sessions</b><span>Interviews or real-user tests</span></div>
          <div class="tl-track" aria-hidden="true">
            <i class="tl-ghost" style="left:43.33%;width:26.67%"></i>
            <i class="tl-bar" data-t="43.33,26.67" data-r="5.83,5.83" style="left:43.33%;width:26.67%"></i>
          </div>
        </div>
        <div class="tl-row">
          <div class="tl-lab"><b>Make sense of it</b><span>Notes, patterns, what matters most</span></div>
          <div class="tl-track" aria-hidden="true">
            <i class="tl-ghost" style="left:63.33%;width:25.0%"></i>
            <i class="tl-bar" data-t="63.33,25.0" data-r="10.0,4.67" style="left:63.33%;width:25.0%"></i>
          </div>
        </div>
        <div class="tl-row">
          <div class="tl-lab"><b>Report back</b><span>Deck, readout meetings</span></div>
          <div class="tl-track" aria-hidden="true">
            <i class="tl-ghost" style="left:83.33%;width:16.67%"></i>
            <i class="tl-bar" data-t="83.33,16.67" data-r="14.17,2.5" style="left:83.33%;width:16.67%"></i>
          </div>
        </div>
      </div>
      <div class="tl-foot">
        <div class="tl-sum trad"><b>4–8 weeks</b><span>is common for an agency or in-house study, with several meetings before you hear a single answer.</span></div>
        <div class="tl-sum rapid"><b>24 hours–5 days</b><span>from booking to report. Real-user tests in 24 hours, customer interviews in 5 days. No meetings required.</span></div>
      </div>
    </div>
  </div>
</section>
{TL_SCRIPT}

{frag("sample.html")}

{frag("why.html")}

<section id="consult">
  <div class="wrap consult-grid">
    <div class="sec-head" style="margin-bottom:0">
      <span class="mono">Start free</span>
      <h2>Check me out first. It's free.</h2>
      <p>No commitment and no sales pitch. Pick one, fill in the form, and I'll reply within 1 business day.</p>
      <div class="free-opts">
        <button type="button" class="free-opt" data-pkg="{NOT_SURE}" data-follow="call"><b>A free 15-min call</b><span>Tell me what's worrying you. I'll tell you what I'd look at first.</span></button>
        <button type="button" class="free-opt" data-pkg="{NOT_SURE}" data-follow="quote"><b>A free plan and quote</b><span>Send your question and a link. Get a plan and a fixed price by email.</span></button>
      </div>
    </div>
    <div class="form-card">
      <iframe id="leadForm" src="https://docs.google.com/forms/d/e/{FORM_ID}/viewform?embedded=true" title="Request a study or free consultation" loading="lazy">Loading…</iframe>
    </div>
  </div>
</section>

{frag("faq.html")}


"""
    out += f"""
<script>
// Preselect the package and follow-up method in the lead form.
(function(){{
  var base="https://docs.google.com/forms/d/e/{FORM_ID}/viewform?embedded=true&usp=pp_url";
  var follow={json.dumps(FOLLOW)};
  var f=document.getElementById("leadForm");
  function setForm(pkg,fol){{
    if(!f) return;
    var u=base;
    if(pkg) u+="&entry.{ENTRY_PKG}="+encodeURIComponent(pkg);
    if(fol&&follow[fol]) u+="&entry.{ENTRY_FOLLOW}="+encodeURIComponent(follow[fol]);
    f.src=u;
  }}
  document.querySelectorAll("[data-pkg]").forEach(function(b){{
    b.addEventListener("click",function(){{ setForm(b.getAttribute("data-pkg"),b.getAttribute("data-follow"));
      document.querySelectorAll(".free-opt").forEach(function(o){{ o.classList.toggle("on", o===b); }}); }});
  }});
  var q=new URLSearchParams(location.search);
  if(q.get("pkg")||q.get("follow")) setForm(q.get("pkg"),q.get("follow"));
}})();
</script>"""
    out += footer(p)
    write("index.html", out)


# ================================================================== BUILDERS
def builders():
    p = "../"
    out = head("Product Feedback in 24 Hours for Indie Devs & Solo Founders | Rapid Research",
               "Get an expert's honest take on what you're building in 24 hours, watch real people try it, or learn to get user feedback yourself. From $500.",
               "/builders/", p)
    out += nav(p)
    out += page_hero(p, "For solo founders & indie devs",
                     "Feedback on what you're building, by tomorrow.",
                     "Vibe coding a side project or about to launch? Get a senior researcher's honest take in 24 hours, or learn to get feedback yourself.")
    coaching = tier("coaching", "Within 1 week", "Customer Interview Coaching",
                    "Learn to get feedback on your product yourself.", "$750",
                    ["A 90-minute call focused on your product",
                     "Find the right people and ask questions that get honest answers",
                     "Run quick tests without a research budget",
                     "Templates to keep, plus 2 weeks of email follow-up"],
                    "builders who want to keep testing on their own.", "Book Coaching")
    out += f"""
<section id="packages">
  <div class="wrap">
{tiers_block(p, [("teardown", C["teardown"]()), ("firstuse", C["firstuse"](True, "Most useful")), ("coaching", coaching)])}
    <div class="mini-steps">
      <div><b>1. Book</b><span>Pay by card. Takes a minute.</span></div>
      <div><b>2. Send a link</b><span>Your product and up to 3 questions.</span></div>
      <div><b>3. Get answers</b><span>A clear report in your inbox, in 24 hours.</span></div>
    </div>
{check_strip(p, "On a tight budget? Run the check yourself.")}
{strip(p, "Not sure which one? Talk it through for free.", p + "startups/", "Have a team? See startup options")}
  </div>
</section>
"""
    out += footer(p)
    write("builders/index.html", out)


# ================================================================== STARTUPS
def startups():
    p = "../"
    out = head("User Testing in 24 Hours for Startups Without a Researcher | Rapid Research",
               "Real feedback from real users without hiring a researcher: 24-hour real-user tests and customer interviews in 5 days, recruiting included. Fixed prices.",
               "/startups/", p)
    out += nav(p)
    out += page_hero(p, "For startups without a researcher",
                     "Real user feedback in 24 hours. Customer interviews in 5 days.",
                     "No researcher on the team? No problem. I find the people, run the sessions, and send a clear report you can act on this sprint.")
    process = frag("process.html").replace('<section id="process" class="light">', '<section id="process" class="light">')
    out += f"""
<section id="packages">
  <div class="wrap">
{tiers_block(p, [("firstuse", C["firstuse"]()), ("diagnosis", C["diagnosis"](True, "Recommended")), ("teardown", C["teardown"]())])}
    <div class="addons">
      <div class="addon">
        <h4>Specialist or B2B participants</h4>
        <p>Need people in a specific job or industry? <span class="mint">+$500</span> on a Drop-off Diagnosis.</p>
      </div>
      <div class="addon">
        <h4>Use your own customers</h4>
        <p>You make the intros, I handle the rest. <span class="mint">−$250</span> on a Drop-off Diagnosis.</p>
      </div>
    </div>
{check_strip(p, "Want a quick self-check first?")}
{strip(p, "Want to check me out first? The first call is free.", p + "teams/", "Need ongoing research? See team options")}
  </div>
</section>

{process}
"""
    out += footer(p)
    write("startups/index.html", out)


# ================================================================== TEAMS
def teams():
    p = "../"
    out = head("Fast Fractional User Research for Startups & VC Portfolios | Rapid Research",
               "A senior researcher for your team without the full-time hire: research sprints, ongoing fractional research, and portfolio support for investors.",
               "/teams/", p)
    out += nav(p)
    out += page_hero(p, "For funded teams & investors",
                     "Research at startup speed: answers in days, not quarters.",
                     "A senior researcher for your team or your portfolio, without the full-time hire or the agency timeline. Every engagement starts with a short call.",
                     f'<a href="{html.escape(form_link(p, follow="call"))}" class="btn btn-mint">Book a call</a><a href="#compare" class="btn btn-ghost">How it compares</a>')
    cmp = frag("compare.html").replace("Real users, senior expertise, startup budget.", "Senior expertise, without agency cost or timelines.")
    call = html.escape(form_link(p, follow="call"))
    out += f"""
<section id="offers">
  <div class="wrap">
    <div class="offers">
      <div class="offer">
        <div class="row"><h3>Growth Research Sprint</h3><span class="from"><small>from</small> $8,500</span></div>
        <p>Fifteen customer interviews across up to three problems, in 2 weeks.</p>
        <ul><li>Activation, retention, pricing, or a new market</li><li>Ranked findings and a highlight reel of quotes</li><li>Readout for your team</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Launch &amp; Fundraise Review</h3><span class="from"><small>from</small> $12,000</span></div>
        <p>Your whole product, end to end, in 3 weeks.</p>
        <ul><li>Expert review plus twenty customer interviews</li><li>Fix roadmap: quick wins vs. bigger bets</li><li>One-page summary for your team and board</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Research on retainer</h3><span class="from">Monthly</span></div>
        <p>A senior researcher on call while you're between hires, or before your first one.</p>
        <ul><li>A steady rhythm of interviews and tests each month</li><li>Async access for quick research questions</li><li>Help hiring your first researcher when you're ready</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Portfolio program</h3><span class="from">For funds</span></div>
        <p>Fast customer insight for your portfolio companies before a launch or a raise.</p>
        <ul><li>Studies your founders can request when they need them</li><li>One contract and one invoice for the fund</li><li>Optional workshops for founders</li></ul>
      </div>
    </div>
    <div class="strip">
      <p>Every engagement is scoped on a short call. NDA and invoicing available.</p>
      <div class="links">
        <a href="{call}" class="btn btn-mint">Book a call</a>
        <a class="more" href="mailto:hello@rapid-research.com">or email hello@rapid-research.com</a>
      </div>
    </div>
  </div>
</section>

{cmp}
<section style="padding-top:0">
  <div class="wrap">
    <a class="diy" href="{p}ai-evals/">
      <span class="diy-tag">AI teams</span>
      <span class="diy-txt"><b>Shipping an AI product?</b> Find out if its answers are actually good, tested by real people, before your users find the problems.</span>
      <span class="diy-go">See AI evals →</span>
    </a>
  </div>
</section>
"""
    out += footer(p)
    write("teams/index.html", out)


# ================================================================== LEARN
def learn():
    p = "../"
    out = head("Rapid Research Coaching for UX Researchers | Rapid Research",
               "Learn to run user research fast without cutting corners: a 1:1 coaching session for researchers, designers, and PMs, with templates included.",
               "/learn/", p)
    out += nav(p)
    out += page_hero(p, "For researchers, designers & PMs",
                     "Learn to get answers in days, not weeks.",
                     "A 1:1 session on scoping, recruiting, running sessions, and synthesis, built around a study you're planning right now.")
    coaching = tier("coaching", "Within 1 week", "Rapid Research Coaching",
                    "A 1:1 session on running research fast.", "$750",
                    ["90 minutes, built around a study you're planning",
                     "Scope a study around one decision",
                     "Recruit and screen in days, not weeks",
                     "Synthesize in hours, with templates you keep",
                     "2 weeks of email follow-up"],
                    "researchers who are asked for answers by Friday.", "Book Coaching", True)
    out += f"""
<section id="packages">
  <div class="wrap">
    <div class="tiers wide-one" style="display:grid;grid-template-columns:minmax(0,520px);justify-content:center">
{coaching.replace("{FORM_coaching}", html.escape(form_link(p, PKG["coaching"], "call")))}
    </div>
{check_strip(p, "See how I review products, then use it yourself.")}
    <div class="strip">
      <p>A full cohort course is coming. Subscribe to The Chaos Debrief to hear first.</p>
      <div class="links">
        <a href="https://rapidresearcher.substack.com" target="_blank" rel="noopener" class="btn btn-ghost">Subscribe on Substack</a>
      </div>
    </div>
  </div>
</section>
"""
    out += footer(p)
    write("learn/index.html", out)


# ================================================================== CHECK (DIY product)
def check():
    p = "../"
    buy = CHECK_BUY_URL or form_link(p, CHECK_PKG, "quote")
    buy_attrs = ' target="_blank" rel="noopener"' if CHECK_BUY_URL else ""
    buy_btn = f'<a href="{html.escape(buy)}" class="btn btn-mint"{buy_attrs}>Get the UX Check · {CHECK_PRICE}</a>'
    out = head("Rapid UX Check: An AI Usability Review for Your Site or App | Rapid Research",
               "An AI skill for Claude Code that checks your site, app, or code for common usability problems and gives you the top 3 fixes, with the research behind each one. " + CHECK_PRICE + ".",
               "/check/", p)
    out += nav(p)
    out += page_hero(p, "DIY tool for builders",
                     "A usability review of your product, in minutes.",
                     "Point it at your site, your code, or a few screenshots. You get the 3 fixes that matter most, exactly where to make them, and the research that explains why.",
                     buy_btn + '<a href="sample-report.html" class="btn btn-ghost" target="_blank" rel="noopener">See a sample report</a>')
    checks = [
        ("Too many choices", "Competing buttons and long menus slow people down.", "Hick's law"),
        ("Tap targets", "Buttons and links too small to hit on a phone.", "Fitts's law, WCAG 2.2"),
        ("Hard-to-read text", "Contrast below the readability standard, with a fixed color.", "WCAG 2.2"),
        ("Form friction", "Missing labels, wrong phone keyboards, long forms, iPhone zoom.", "NN/g, Baymard"),
        ("Speed", "How long the main content takes to appear, and things that jump.", "Core Web Vitals"),
        ("First impression", "Can a visitor tell what it is and what to do in 5 seconds?", "NN/g"),
        ("Dead ends", "Empty screens and vague errors with no way forward.", "Nielsen's heuristics"),
        ("Accessibility basics", "Alt text, unlabeled icons, missing headlines.", "WCAG 2.2"),
    ]
    cards = "\n".join(f'      <div class="ck"><b>{t}</b><span>{d}</span><em>{src}</em></div>' for t, d, src in checks)
    out += f"""
<section id="what">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">What it checks</span>
      <h2>The problems that cost you users, caught automatically.</h2>
      <p>It measures your pages on desktop and phone, reads your code if you share it, and only reports what it can point to.</p>
    </div>
    <div class="cks">
{cards}
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">What you get</span>
      <h2>Three fixes, not thirty.</h2>
      <p>A one-page report you'll actually read.</p>
    </div>
    <div class="mini-steps">
      <div><b>Your top 3 fixes</b><span>What's wrong, why it matters, and exactly where to change it.</span></div>
      <div><b>The research, as a chart</b><span>Hick's law, Fitts's law, contrast, and more, with your numbers on it.</span></div>
      <div><b>What's already working</b><span>Plus a tucked-away list of smaller things for later.</span></div>
    </div>
    <div class="strip">
      <p>Includes a {CHECK_PRICE} credit toward any Rapid Research study within 30 days.</p>
      <div class="links">
        {buy_btn}
        <a class="more" href="sample-report.html" target="_blank" rel="noopener">See a sample report</a>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="faq">
      <details><summary>What do I need to run it?</summary><p>Claude Code, plus Node and Python on your computer. It asks before installing anything else (it uses Playwright to load your pages).</p></details>
      <details><summary>Does it work on my local dev server?</summary><p>Yes. Give it a localhost address, your repo, or screenshots. Live URLs give the most complete check.</p></details>
      <details><summary>Is this the same as real user research?</summary><p>No. It catches common, well-understood problems fast. It can't tell you whether people want your product. For that, a First-Use Test shows real people using it.</p></details>
      <details><summary>Can I use it more than once?</summary><p>Yes. Run it as often as you like, on any project.</p></details>
    </div>
  </div>
</section>
"""
    out += footer(p)
    write("check/index.html", out)


# ================================================================== AI EVALS
def evals():
    p = "../"
    call = html.escape(form_link(p, EVALS_PKG, "call"))
    out = head("AI Evals with Real Users: Test Your Chatbot, Copilot, or Agent | Rapid Research",
               "Find out if your AI is actually good. Real people test your chatbot, copilot, or agent on real tasks, so you know if the new version beats the old one before you ship.",
               "/ai-evals/", p)
    out += nav(p)
    out += page_hero(p, "For teams building with AI",
                     "Is your AI actually getting better? Find out before your users do.",
                     "Stop vibe-checking. Real people test your AI on real tasks, and you get a clear answer: what's working, what's broken, and whether the new version beats the old one.",
                     f'<a href="{call}" class="btn btn-mint">Book a call</a><a href="#offers" class="btn btn-ghost">See options</a>')
    out += f"""
<section id="why-evals" style="padding-bottom:40px">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">Why it works</span>
      <h2>Vibe checks don't scale.</h2>
      <p>Your team knows the product too well to test it like a customer would. Real users ask things you'd never think of, and don't forgive mistakes.</p>
    </div>
    <div class="mini-steps">
      <div><b>Tested by real users</b><span>People who match your customers ask your AI what they'd actually ask it.</span></div>
      <div><b>Grades you can trust</b><span>Every answer is graded by more than one person, so the scores aren't one person's opinion.</span></div>
      <div><b>Auto-evals that match people</b><span>Your automated grader tuned to agree with real people, so you can run it on every release.</span></div>
    </div>
  </div>
</section>

<section id="offers" style="padding-top:40px">
  <div class="wrap">
    <div class="offers">
      <div class="offer">
        <div class="row"><h3>AI Answer Audit</h3><span class="from">$3,000 <small>· 5 days</small></span></div>
        <p>Find out where your AI lets people down. I go through 100–200 of your real conversations and show you what goes wrong, and how often.</p>
        <ul><li>The top problems, ranked by how often they happen and how much they hurt</li><li>A clear checklist of what a good answer looks like</li><li>50 graded examples to start your test set</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Real-User AI Test</h3><span class="from"><small>from</small> $9,500 <small>· 2 weeks</small></span></div>
        <p>Real people use your AI for real tasks, and every answer gets graded.</p>
        <ul><li>15–20 people who match your customers</li><li>Every answer graded by at least two people</li><li>Old vs. new model or prompt, side by side</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Auto-Grader Tune-Up</h3><span class="from"><small>from</small> $6,000 <small>· 2 weeks</small></span></div>
        <p>Make your automated evals agree with real people, so you can trust them on every release.</p>
        <ul><li>A test set graded by people, built from your own data</li><li>Your LLM-as-judge prompt fixed where it disagrees with people</li><li>A pass/fail check to run before every launch</li></ul>
      </div>
      <div class="offer">
        <div class="row"><h3>Ongoing AI quality checks</h3><span class="from">Monthly</span></div>
        <p>A regular check-up as your models and prompts change.</p>
        <ul><li>Monthly real-user test rounds</li><li>New problems added to your checklist as they show up</li><li>Quick answers to your team's eval questions</li></ul>
      </div>
    </div>
    <div class="strip">
      <p>Every project starts with a short call to see your product and what "good" means for it. NDA available.</p>
      <div class="links">
        <a href="{call}" class="btn btn-mint">Book a call</a>
        <a class="more" href="mailto:hello@rapid-research.com">or email hello@rapid-research.com</a>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="faq">
      <details><summary>What kinds of AI products do you test?</summary><p>Chatbots and assistants, copilots, agents, AI search and recommendations, and anything that writes or generates content.</p></details>
      <details><summary>Why not just have our team check the answers?</summary><p>Your team knows too much. They phrase questions the way the AI expects and forgive its mistakes. Customers don't.</p></details>
      <details><summary>We already have automated evals. Why add people?</summary><p>An automated grader is only useful if it agrees with real people. I check that on your own data and fix the places where it doesn't.</p></details>
      <details><summary>How do I know the grades are reliable?</summary><p>Each answer is graded by at least two people using the same checklist, and I report how often they agree (Cohen's kappa, for the technical folks). If they don't agree, the checklist gets fixed before you see results.</p></details>
      <details><summary>Do you need access to our data?</summary><p>Just an export of sample conversations, under NDA. Remove personal details before sharing.</p></details>
    </div>
  </div>
</section>
"""
    out += footer(p)
    write("ai-evals/index.html", out)

def sitemap():
    pages = ["/", "/builders/", "/startups/", "/teams/", "/learn/", "/ai-evals/", "/check/", "/sample-report.pdf"]
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    home(); builders(); startups(); teams(); learn(); evals(); check(); sitemap()
    print("built")
