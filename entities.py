# -*- coding: utf-8 -*-
"""
Pulls specific named things out of post text — people, brands, programmes,
places, events — so the overlap board can show "Dolly Parton" rather than
"Retail and FMCG".

Three sources, in order of reliability:
  1. LinkedIn's own @-mentions, which come with a type (person or company).
  2. Hashtags.
  3. Runs of capitalised words in the post body and any article title.

Source 3 is the noisy one, so most of this file is filtering it.
"""
import re
import collections

# Words that are capitalised for grammatical reasons, not because they name
# something. Stripped from the edges of a candidate, and rejected on their own.
FUNCTION = set("""
i i'm i've i'll i'd my me mine we we're us our ours you you're you've your yours
he he's she she's they they're them their it it's its this that these those there
here what what's why how how's who whom which when where whose
a an the and or but so if then than as at by for from in into of on to up with
without about after before during over under again once
is are was were be been being am do does did doing done have has had having
will would shall should can could may might must
no not nor yes ok okay just also only even still now next last first second
more most best good great big small many much few less least other another
happy morning afternoon evening night monday tuesday wednesday thursday friday
saturday sunday january february march april june july august september october
november december today tomorrow yesterday week month year weekend
thanks thank hi hey hello ps pps edit update congrats congratulations sorry
yeah yep nope oh ah hmm lol wow please listen look remember imagine
everyone everybody someone somebody anyone anybody nobody nothing something
anything everything people person guy guys folks friends team
jan feb mar apr jun jul aug sept sep oct nov dec
mr mrs ms miss dr prof sir dame lord lady rev
mum mom mother dad father son daughter grandma grandad nan gran
""".split())

# Bare first names show up constantly in anecdotes ("Karl told me...") and are
# never the subject of a post on their own. Only blocked when they stand alone.
FIRST_NAMES = set("""
james john david michael paul mark peter andrew richard robert simon stephen
chris christopher daniel matthew tom thomas will william sam jack george harry
charlie ben jamie luke adam alex nick oliver joe joseph ryan sean shaun dan
jonathan tim timothy anthony martin gary jason keith kevin craig neil ian
sarah emma laura claire clare rachel rebecca hannah jessica lucy sophie amy
katie kate helen jane julie karen lisa nicola michelle louise victoria anna
charlotte olivia emily chloe holly zoe eleanor beth jo joanne fiona
donald elon karl greta oprah
""".split())

# Capitalised but generic: job titles, jargon, metric acronyms. These are how
# this community talks, not what it is talking about.
GENERIC = set("""
ceo ceos cmo cmos cfo coo cto cro chro md mds vp svp evp gm
cv cvs cvs' mba mbas phd bsc msc ba hr ir pr comms
roi roas cac ltv cpm cpc ctr cpa kpi kpis kpi's aov mrr arr nps sov
tv ooh ctv dooh sem seo ppc crm cms cdp dsp ssp ugc b2b b2c d2c dtc saas fmcg
ai ml llm llms nlp api apis ux ui dna pov dm dms faq q&a rsvp asap eta usp
gen genz gen-z millennial millennials boomer boomers
corp inc ltd llc plc gmbh
am pm est pst gmt bst utc
covid covid-19
""".split())

# Big geographies. Almost always context, not the subject of the post. Tagged
# as places so the dashboard can filter them out by default.
PLACES = set("""
uk u.k. usa u.s. u.s.a. us britain british england english scotland scottish
wales welsh ireland irish america american americas europe european eu asia
asian africa african australia australian nz new zealand canada canadian
london manchester birmingham leeds bristol liverpool glasgow edinburgh dublin
new york nyc san francisco los angeles la chicago boston miami austin seattle
paris berlin madrid barcelona amsterdam milan rome lisbon dubai singapore
tokyo sydney melbourne mumbai delhi toronto
france french germany german spain spanish italy italian netherlands dutch
india indian china chinese japan japanese brazil mexico
""".split()) | {"new york", "san francisco", "los angeles", "new zealand", "middle east"}

# "and" is left out on purpose: it glues unrelated names together far more
# often than it holds one together ("TikTok and WPP"). "&" is kept.
CONNECTORS = {"of", "the", "for", "de", "van", "von", "da", "di", "du",
              "des", "la", "le", "el", "&"}

# Longest candidate we accept. Anything longer is a production credit list or a
# chunk of headline, never a single named thing.
MAX_TOKENS = 4

# Role and seniority words. A candidate made up entirely of these is a job
# title ("Chief Growth Officer"), not a subject.
ROLE = set("""
chief growth officer director head manager management president vice senior
junior global regional lead leader executive partner associate assistant
founder co-founder owner principal specialist consultant advisor adviser
marketing brand digital creative strategy strategic commercial operations
social content media communications comms account client group deputy
""".split())

# The platform the posts are on. It gets named constantly and it never tells
# you anything about what the conversation is about, so it is excluded from the
# subject board entirely. Add other self-referential subjects here — the client's
# own brand is usually worth adding too, so the board shows the conversation
# around them rather than about them.
EXCLUDE = set()

# Substring version: anything containing one of these is dropped. "linkedin"
# needs this rather than an exact match, because extraction throws up dozens of
# fragments around it ("New LinkedIn", "CMO of LinkedIn", "#LinkedInStrategy")
# that are all the same self-reference. The cost is that a genuinely distinct
# subject with the platform in its name — LinkedIn Learning, say — goes too.
EXCLUDE_CONTAINS = {"linkedin"}


# Hashtags that are themes rather than topics, plus sign-off boilerplate.
HASHTAG_BLOCK = set("""
marketing advertising ad ads adland brand branding business content social
socialmedia digital media strategy creative creativity leadership hiring jobs
motivation growth sales linkedin post partnership sponsored gifted ad
""".split())

TOKEN = re.compile(r"[A-Za-z][A-Za-z'&.\-]*|\d{2,4}")
# Split on sentence enders *and* list punctuation. Without the second group a
# comma-separated list of brands merges into one entity.
SENT = re.compile(r"[.!?\n,;:|/()\[\]{}\"\u201c\u201d\u2014\u2013\u2022>]+|(?<=[.!?])\s+")
CONTRACTION = re.compile(r"'(s|t|d|ll|ve|re|m)$", re.IGNORECASE)


def casing_stats(texts):
    """How often is each word seen lower-case across the whole corpus?

    A word that mostly appears lower-case ("marketing", "brand") is a common
    noun that happened to start a sentence, not a name.
    """
    low, up = collections.Counter(), collections.Counter()
    for t in texts:
        for w in re.findall(r"[A-Za-z][A-Za-z'\-]+", t):
            (low if w[0].islower() else up)[w.lower()] += 1
    return low, up


def _trim(run):
    """Strip function words from both ends of a candidate run."""
    while run and run[0].lower() in FUNCTION | CONNECTORS:
        run = run[1:]
    while run and run[-1].lower() in FUNCTION | CONNECTORS:
        run = run[:-1]
    return run


def _normalise(name):
    name = name.strip(" .,;:-'\"")
    name = re.sub(r"[''`]s$", "", name)          # possessive
    name = re.sub(r"\s+", " ", name)
    return name


def extract(text, low, up):
    """Capitalised-run extraction. Returns a list of surface forms."""
    found = []
    for sent in SENT.split(text):
        toks = TOKEN.findall(sent)
        i, at_start = 0, True
        while i < len(toks):
            t = toks[i]
            if len(t) > 1 and t[:1].isupper():
                run, j = [t], i + 1
                while j < len(toks):
                    nxt = toks[j]
                    if len(nxt) > 1 and nxt[:1].isupper():
                        run.append(nxt)
                        j += 1
                    elif (nxt.lower() in CONNECTORS and j + 1 < len(toks)
                          and toks[j + 1][:1].isupper() and len(toks[j + 1]) > 1):
                        run.append(nxt.lower())
                        j += 1
                    else:
                        break
                lone = len(run) == 1
                run = [w for w in run if not CONTRACTION.search(w) or w.lower() not in FUNCTION]
                run = _trim(run)
                if run and len(run) <= MAX_TOKENS:
                    cand = _normalise(" ".join(run))
                    key = cand.lower()
                    words = [w for w in key.split() if w not in CONNECTORS]
                    keep = (bool(cand) and key not in GENERIC and key not in FUNCTION
                            and bool(words) and not all(w in ROLE for w in words))
                    if keep and len(words) == 1 and words[0] in FIRST_NAMES:
                        keep = False
                    if keep and len(run) == 1:
                        w = key
                        total = low[w] + up[w]
                        # a lone word that is often lower-case elsewhere, or that
                        # opened the sentence, is not a name
                        if (total and low[w] / total > 0.25) or (at_start and lone):
                            keep = False
                    if keep:
                        found.append(cand)
                at_start = False
                i = j
            else:
                if len(t) > 1:
                    at_start = False
                i += 1
    return found


def excluded(key):
    """True if this subject should never reach the board."""
    k = key.lower().strip()
    if k in EXCLUDE:
        return True
    return any(frag in k for frag in EXCLUDE_CONTAINS)


def classify(name, mention_types):
    """Type an entity, only claiming person/org where LinkedIn's own @-mention
    data says so. Everything else stays "other" rather than guessing."""
    key = name.lower()
    if key in PLACES:
        return "place"
    if key in mention_types:
        return mention_types[key]
    if name.startswith("#"):
        return "hashtag"
    bare = name.replace(".", "")
    if bare.isupper() and 2 <= len(bare) <= 6:
        return "acronym"
    return "other"


def fold_aliases(counts):
    """Merge a bare surname into the full name when the full name is commoner.

    "Ritson" and "Mark" both collapse into "Mark Ritson"; "TikToks" into
    "TikTok". Keeps the board from listing the same subject three times.
    """
    keys = sorted(counts, key=lambda k: (-counts[k], k))
    alias = {}
    multi = [k for k in keys if " " in k]
    for k in keys:
        if " " in k:
            continue
        for m in multi:
            parts = m.split()
            if k in parts and counts[m] >= counts[k] * 0.4:
                alias[k] = m
                break
    for k in list(counts):
        if k in alias:
            continue
        if k.endswith("s") and k[:-1] in counts and counts[k[:-1]] >= counts[k]:
            alias[k] = k[:-1]
    # resolve one hop of chaining
    for k, v in list(alias.items()):
        seen = {k}
        while v in alias and v not in seen:
            seen.add(v)
            v = alias[v]
        alias[k] = v
    return alias
