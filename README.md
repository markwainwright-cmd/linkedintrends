# LinkedIn trends dashboard

Turns an Apify LinkedIn-posts export into a single self-contained HTML dashboard
you can email to a client. No server, no token in the output, no dependencies
beyond the Python standard library.

## Files

| File | What it does |
|---|---|
| `entities.py` | Named-subject extraction and its filter lists. |
| `topics.py` | The broad-theme keyword model. **Edit this per client.** |
| `prepare.py` | Normalises the Apify records, tags topics, scores engagement. |
| `template.html` | The dashboard itself. Edit for layout, palette, copy. |
| `build_dashboard.py` | Pulls the data and writes the dated output file. |

## Running it

Rebuild from an export already on disk:

```bash
python build_dashboard.py --file dataset_linkedin-posts-scraper-pro.json \
  --client "Client name" --title "LinkedIn signal board"
```

Pull the last successful run of a saved Apify task instead:

```bash
export APIFY_TOKEN=apify_api_xxxxxxxx
python build_dashboard.py --task my-linkedin-task --client "Client name"
```

Other sources: `--dataset <id>` for a specific dataset, `--run-actor <actor-id>
--actor-input input.json` to run the scrape inline (five-minute ceiling — use a
schedule plus `--task` for anything longer).

Output lands in `out/` as `<client>-linkedin-signal-<date>.html`.

## The two board modes

**Named subjects** (default) works at the level of specific things — Dolly Parton,
System1, Cannes, Monzo. Pulled from LinkedIn's @-mentions, hashtags, and runs of
capitalised words in the post body and article titles. This is the mode that
generates content ideas.

**Broad themes** uses the keyword model in `topics.py`. Useful for the shape of
the conversation, too general to brief a post against.

`EXCLUDE` and `EXCLUDE_CONTAINS` in `entities.py` drop subjects that are
self-referential rather than informative. LinkedIn is in there by default. Worth
adding the client's own brand for most jobs, so the board shows the conversation
around them rather than every mention of their name.

Extraction noise lives in `entities.py`: `FUNCTION`, `GENERIC`, `ROLE`,
`FIRST_NAMES`, `PLACES` and `HASHTAG_BLOCK` are the lists to add to when
something junky keeps appearing on the board. `MAX_TOKENS` caps candidate
length — raise it only if real subjects are being truncated.

## Editing the theme model

`topics.py` is a dict of `label: [match terms]`. Terms match whole words, so
`ai` catches "AI" but not "said". Use a space for a phrase (`"brand building"`)
and `|` for alternatives (`"burnout|burn out"`).

Keep terms specific. Anything as broad as `team`, `content` or `insight` will
match a third of the corpus and flatten the signal. After editing, rebuild and
check the voices column — a topic sitting on every voice in every period is
usually a term that's too loose.

## Accumulating history

The scraper caps posts per profile, so one run gives very uneven history per
voice — see the methodology note in the dashboard. Fix it by merging each pull
into an archive:

```bash
python build_dashboard.py --task my-task \
  --history data/history.json --max-age-days 365 --client "Client name"
```

Posts are keyed on their LinkedIn post id. A post already held is refreshed from
the newer pull, since engagement keeps climbing after publication. Run it daily
for a month and every voice has a month of history.

## Hosting it live

`workflow-build.yml` goes in `.github/workflows/`. It runs on a schedule, pulls
from Apify, merges the history, commits it back and publishes to GitHub Pages.

Repository setup:

1. Settings → Secrets and variables → Actions → **New repository secret**:
   `APIFY_TOKEN`.
2. Same page, **Variables** tab: `APIFY_TASK_ID` and `CLIENT_NAME`.
3. Settings → Pages → Source: **GitHub Actions**.
4. Commit an empty `data/` directory (or let the first run create it).
5. Actions tab → Build signal board → **Run workflow** to test it.

Set the cron to sit after your Apify schedule, not before it. The build also
writes `out/index.html` so the dashboard serves as the site root.

**GitHub Pages on a public repo is world-readable.** Private-repo Pages needs
Enterprise Cloud. If the URL can't be public, deploy the same `out/` directory
to Cloudflare Pages and put Cloudflare Access in front of it — that gives you
email-based login on the free tier.
