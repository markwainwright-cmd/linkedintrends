# -*- coding: utf-8 -*-
"""
Topic model for the LinkedIn trending-topics dashboard.

This is the file to edit per client. Each topic is a label plus a list of
match terms. Terms are matched case-insensitively on whole words, so "ai"
matches "AI" and "ai." but not "said" or "detail". Use a space in a term to
match a phrase ("brand building"), or "|" inside a term for alternatives
("burnout|burn out").

Keep terms specific. A term like "team" or "content" will match half the
corpus and drown out the real signal.
"""

TOPICS = {
    "AI and creative work": [
        "ai", "a.i.", "artificial intelligence", "chatgpt", "genai", "gen ai",
        "llm", "machine learning", "midjourney", "sora", "agentic",
        "prompt", "synthetic", "automation", "automated", "data centre|data center",
        "effort atrophy", "deepfake", "openai", "anthropic", "claude",
    ],
    "Advertising craft and standout work": [
        "best ad", "great ad", "the ad", "art direction", "art directed",
        "copywriting", "copywriter", "print ad", "outdoor ad", "billboard",
        "direct mail", "poster", "creative idea", "one minute briefs",
        "craft", "casting", "typography", "campaign film", "the execution",
    ],
    "Brand building vs performance": [
        "brand building", "brand build", "building a brand", "brand equity",
        "performance marketing", "share of voice", "distinctiveness",
        "distinctive asset", "mental availability", "salience", "brand codes",
        "long term|long-term", "short termism|short-termism", "60/40",
        "binet", "brand positioning", "positioning",
    ],
    "Effectiveness and attention": [
        "effectiveness", "system1|system 1", "measurement", "incrementality",
        "econometric", "market mix|mmm", "benchmark", "creative effectiveness",
        "roi", "return on investment", "attention research",
        "attention economy", "attention data", "attention metric",
        "eye tracking", "brand lift", "ad testing", "pre-testing|pretesting",
    ],
    "Leadership and management culture": [
        "leadership", "leader", "manager", "managing people", "micromanage",
        "micromanagement", "boss", "workplace culture", "company culture",
        "empower", "psychological safety", "toxic", "delegate",
        "one to one|1:1", "line manager", "direct report", "kind leadership",
    ],
    "Careers, hiring and the job market": [
        "hiring", "hire", "recruit", "recruiter", "resume|résumé", "cv",
        "interview", "job hunt", "job market", "redundant|redundancy",
        "layoff|laid off", "entry level|entry-level", "graduate scheme",
        "promotion", "salary", "gardening leave", "the great stay",
        "headcount", "junior role", "career change", "notice period",
    ],
    "Mental health and burnout": [
        "mental health", "burnout|burn out|burnt out", "therapy", "therapist",
        "anxiety", "anxious", "depression", "wellbeing|well-being",
        "exhausted", "exhaustion", "stress", "overwhelmed", "sobriety|sober",
        "asking for help",
    ],
    "Work, life and family": [
        "kids", "children", "parenting", "my son", "my daughter",
        "4,000 weeks|4000 weeks", "school run", "family time",
        "work life balance|work-life balance", "annual leave",
        "paternity", "maternity", "childcare", "time with my",
    ],
    "LinkedIn and creator strategy": [
        "the algorithm", "engagement bait", "commenting", "carousel",
        "the hook", "personal brand", "creator", "creators",
        "thought leadership", "organic reach", "followers",
        "posting cadence", "creator effectiveness", "b2b creator",
        "linkedin post", "linkedin voices", "on linkedin",
    ],
    "Social media management and brand accounts": [
        "social media manager", "community manager", "social team",
        "brand account", "tone of voice", "went viral|going viral",
        "trend jacking|jumping on trends", "social listening",
        "brand page", "reply guy", "comment section", "moderation",
    ],
    "Agency life and the client relationship": [
        "agency", "adland", "the brief", "off brief|off-brief", "pitching",
        "new business", "account management", "timesheet", "holding company",
        "in housing|in-housing", "scope", "retainer", "procurement",
        "client feedback", "sign off|signoff", "creative review",
    ],
    "Awards, events and industry moments": [
        "cannes", "cannes lions", "awards", "award show", "d&ad", "effies",
        "festival", "conference", "keynote", "panel", "speaker",
        "un//scene|unscene", "ideas fest", "shortlist", "jury",
    ],
    "Podcasts, newsletters and owned media": [
        "podcast", "substack", "newsletter", "this episode", "new episode",
        "youtube channel", "going live", "live stream|livestream", "my blog",
        "video series", "subscribe",
    ],
    "Startups, funding and founders": [
        "startup|start-up", "founder", "co-founder", "funding", "fundraise",
        "raising", "investor", "vc", "seed round", "pitch deck", "valuation",
        "bootstrap", "scaling", "connectd", "angel", "runway",
    ],
    "Sport": [
        "world cup", "england", "football", "premier league", "rugby",
        "olympics", "formula 1|f1", "semi final|semi-final", "team gb",
        "cricket", "the match", "manchester united", "everton", "wembley",
    ],
    "Retail, FMCG and big brand campaigns": [
        "aldi", "tesco", "sainsbury", "lidl", "m&s|marks & spencer", "ikea",
        "apple", "guinness", "heineken", "mcdonald", "burger king", "kfc",
        "coca cola|coca-cola", "pepsi", "supermarket", "retail media",
        "fmcg", "pack shot|packshot", "uber", "nike",
    ],
    "Crisis and corporate comms": [
        "crisis", "product recall", "recall", "apology", "apologise",
        "reputation", "backlash", "boycott", "pr disaster", "press office",
        "spokesperson", "holding statement", "corporate comms", "damage control",
    ],
    "Data, research and insight": [
        "the data", "the research", "new research", "research shows",
        "the study", "new study", "survey", "sample size", "the numbers",
        "dataset", "correlation", "statistically", "heatmap", "the chart",
        "the report", "data set", "methodology",
    ],
}
