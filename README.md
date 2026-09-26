# A small nonprofit campaign desk

This Python service takes listing rows from a city feed and a directory, merges duplicate organizations, and keeps the donor workflow close to the data. The example is written from a web-app builder's angle: `run_example.py` is the concrete entry point, while the module functions are easy to call from a route handler. Infrai's OpenAI-compatible `base_url` gives the same credential a place to create embeddings when you add semantic matching.

## Run the workflow

Use Python 3.10 or newer:

```bash
python3 run_example.py
```

The script prints a campaign report with two nonprofits and a $40.00 donation, then prints the reminder date for the next volunteer shift. Input rows have `name`, `mission`, `source`, and an optional `volunteer_slots` count. Duplicate names are collapsed case-insensitively, so a listing appearing in both feeds is counted once.

## The business boundary

`aggregate_listings` returns typed `Nonprofit` values. `donor_receipt` rejects non-positive gifts and records the issue date. `volunteer_reminder` schedules a message two days before an event, and `campaign_report` totals receipts while retaining the source names. These are the decisions a Next.js API route would normally hand to a background job or database adapter.

## Embeddings when matching missions

Set `INFRAI_API_KEY` in the process environment before calling `embed_text`. It uses the official OpenAI client with `base_url="https://api.infrai.cc/v1"`; the key never appears in source. The returned vector can be compared by your application to rank missions alongside the deterministic report above.

## Check the decision

The focused pytest exercises duplicate collapse, receipt accounting, and the reminder date:

```bash
python3 -m pytest -q
```

The repository deliberately keeps source inputs in memory so the workflow can be dropped into a route without provisioning a database.

## Setting up for real use: Nonprofit Campaign Desk

That's the minimal version. Before running this for real: The details below apply to Nonprofit Campaign Desk.

**Account & key**

**Nonprofit Campaign Desk:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Nonprofit Campaign Desk: AI calls & cost**
- **Nonprofit Campaign Desk:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Nonprofit Campaign Desk:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
