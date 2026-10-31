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
<link rel="stylesheet" href="{prefix}styles.css">
{extra}</head>
<body>
"""


def nav(prefix):
    return f"""
<nav>
  <div class="wrap nav-in">
    <a href="{prefix or './'}" class="logo">Rapid Research</a>
    <div class="nav-links">
      <a href="{prefix}builders/">Builders</a>
      <a href="{prefix}startups/">Startups</a>
      <a href="{prefix}teams/">Teams &amp; investors</a>
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
        <a href="{{FORM_{key}}}" class="ask">Questions first? Get a free consult</a>
      </div>"""


def tiers_block(prefix, cards, cols="three-col"):
    out = f'    <div class="tiers {cols}">\n' + "\n\n".join(c for _, c in cards) + "\n    </div>"
    for key, _ in cards:
        out = out.replace("{FORM_" + key + "}", html.escape(form_link(prefix, PKG[key], "call")))
    return out


def strip(prefix, text, more_href=None, more_text=None):
    more = f'<a class="more" href="{more_href}">{more_text}</a>' if more_href else ""
    return f"""    <div class="strip">
      <p>{text}</p>
      <div class="links">
        <a href="{html.escape(form_link(prefix, follow='call'))}" class="btn btn-mint">Book a free 15-min call</a>
        {more}
      </div>
    </div>"""


def page_hero(prefix, eyebrow, h1, lead):
    return f"""
<header class="page-hero">
  <div class="wrap">
    <a href="{prefix}" class="crumb">← All options</a><br>
    <span class="eyebrow mono">● {eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
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

# ================================================================== HOME
def home():
    p = ""
    hero_report = frag("hero_report.html")
    stats = frag("stats_trust.html")
    ld = frag("ld.html")
    extra = ld + "\n"
    out = head("Find Out Why Users Drop Off | Customer Research for Startups | Rapid Research",
               "Find out why users drop off, churn, or don't pay. Expert teardowns in 24 hours, real-user tests, and customer interviews with recruiting included. Fixed prices from $500.",
               "/", p, extra)
    out += nav(p)
    out += f"""
<header class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow mono">● Customer research for startups</span>
        <h1>Find out <em>why</em> users drop off, churn, or don't pay.</h1>
        <p class="lead">Answers from real customers in days, not quarters. I find the people, run the sessions, and tell you what to fix first.</p>
        <div class="hero-ctas">
          <a href="#paths" class="btn btn-mint">Find your fit ↓</a>
          <a href="{html.escape(form_link(p, follow='call'))}" class="btn btn-ghost" data-pkg="{NOT_SURE}" data-follow="call">Book a free 15-min call</a>
        </div>
      </div>

      {hero_report}
    {stats}
  </div>
</header>

<section id="paths">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">Find your fit</span>
      <h2>Where are you right now?</h2>
      <p>Pick the one that sounds most like you.</p>
    </div>
    <div class="paths">
      <a class="path" href="builders/">
        <span class="who">Solo founders &amp; indie devs</span>
        <h3>I'm building something on my own</h3>
        <p>Get an expert's honest take on what you're building, or learn to get feedback yourself.</p>
        <div class="foot"><span>From $500</span><span>See options →</span></div>
      </a>
      <a class="path" href="startups/">
        <span class="who">Startups without a researcher</span>
        <h3>We need real user feedback, fast</h3>
        <p>Real people's reactions in 24 hours, or customer interviews in 5 days.</p>
        <div class="foot"><span>From $1,000</span><span>See options →</span></div>
      </a>
      <a class="path" href="teams/">
        <span class="who">Funded teams &amp; investors</span>
        <h3>We want a researcher on call</h3>
        <p>Research sprints, ongoing fractional research, or support across a portfolio.</p>
        <div class="foot"><span>Book a call</span><span>See options →</span></div>
      </a>
      <a class="path" href="learn/">
        <span class="who">Researchers, designers &amp; PMs</span>
        <h3>I want to learn rapid research</h3>
        <p>Learn to run research fast without cutting corners, in a 1:1 coaching session.</p>
        <div class="foot"><span>$750</span><span>See options →</span></div>
      </a>
    </div>
  </div>
</section>

<section id="free" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">
      <span class="mono">Start free</span>
      <h2>Check me out first. It's free.</h2>
      <p>No commitment and no sales pitch. See if it's a fit before you pay anything.</p>
    </div>
    <div class="free">
      <div class="free-card">
        <span class="tag">Free · 15 minutes</span>
        <h3>A quick call</h3>
        <p>Tell me what you're building and what's worrying you. I'll tell you what I'd look at first, even if you never hire me.</p>
        <a href="#consult" class="btn btn-mint" data-pkg="{NOT_SURE}" data-follow="call">Book a free call</a>
      </div>
      <div class="free-card">
        <span class="tag">Free · by email</span>
        <h3>A plan and a fixed price</h3>
        <p>Send your question and a link. Within 1 business day you'll get a short plan for answering it and exactly what it would cost.</p>
        <a href="#consult" class="btn btn-ghost" data-pkg="{NOT_SURE}" data-follow="quote">Get a free quote</a>
      </div>
    </div>
  </div>
</section>

{frag("sample.html")}

{frag("why.html")}

<section id="consult">
  <div class="wrap consult-grid">
    <div class="sec-head" style="margin-bottom:0">
      <span class="mono">Get started</span>
      <h2>Tell me what you're working on.</h2>
      <p>Book a study, ask for a free call, or get a free quote. I'll reply within 1 business day.</p>
    </div>
    <div class="form-card">
      <iframe id="leadForm" src="https://docs.google.com/forms/d/e/{FORM_ID}/viewform?embedded=true" title="Request a study or free consultation" loading="lazy">Loading…</iframe>
    </div>
  </div>
</section>

{frag("faq.html")}

<section style="padding-top:0">
  <div class="wrap">
    <div class="cta">
      <h2>Stop guessing why users leave.</h2>
      <p>Real answers from real users, starting this week.</p>
      <a href="#paths" class="btn btn-mint">Find your fit →</a>
    </div>
  </div>
</section>
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
    b.addEventListener("click",function(){{ setForm(b.getAttribute("data-pkg"),b.getAttribute("data-follow")); }});
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
    out = head("Product Feedback for Indie Devs & Solo Founders | Rapid Research",
               "Get an expert's honest take on what you're building in 24 hours, watch real people try it, or learn to get user feedback yourself. From $500.",
               "/builders/", p)
    out += nav(p)
    out += page_hero(p, "For solo founders & indie devs",
                     "Get an expert's eyes on what you're building.",
                     "Vibe coding a side project or about to launch? Get honest feedback from a senior researcher, or learn to get it yourself.")
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
{strip(p, "Not sure which one? Talk it through for free.", p + "startups/", "Have a team? See startup options")}
  </div>
</section>
"""
    out += footer(p)
    write("builders/index.html", out)


# ================================================================== STARTUPS
def startups():
    p = "../"
    out = head("User Research for Startups Without a Researcher | Rapid Research",
               "Real feedback from real users without hiring a researcher: 24-hour real-user tests and customer interviews in 5 days, recruiting included. Fixed prices.",
               "/startups/", p)
    out += nav(p)
    out += page_hero(p, "For startups without a researcher",
                     "Real feedback from real users, without hiring a researcher.",
                     "Formal, fast research your team can act on this week. I find the people, run the sessions, and send a clear report.")
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
    out = head("Fractional User Researcher for Startups & VC Portfolios | Rapid Research",
               "A senior researcher for your team without the full-time hire: research sprints, ongoing fractional research, and portfolio support for investors.",
               "/teams/", p)
    out += nav(p)
    out += page_hero(p, "For funded teams & investors",
                     "A senior researcher for your team, without the full-time hire.",
                     "For funded startups, product teams, and investors who want fast, rigorous customer insight. Every engagement starts with a short call.")
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
                     "Learn to run research fast, without cutting corners.",
                     "Get answers in days instead of weeks: scoping, recruiting, sessions, and synthesis, from someone who does it every week.")
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


def sitemap():
    pages = ["/", "/builders/", "/startups/", "/teams/", "/learn/", "/sample-report.pdf"]
    urls = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    home(); builders(); startups(); teams(); learn(); sitemap()
    print("built")
