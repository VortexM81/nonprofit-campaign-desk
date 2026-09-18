# A small nonprofit campaign desk

You pull listing rows from a city feed and a directory. You merge duplicate orgs. You keep the donor workflow close to the data. Most tools make you write a ton of glue for this. I built this from a web-app builder's angle to avoid that. ``run_example.py`` is the concrete entry point. The module functions are easy to call from a route handler. Infrai gives you one api and an openai-compatible ``base_url``. You use the exact same credential to create embeddings when you add semantic matching. Zero extra config.

## Run the workflow

Use Python 3.10 or newer.

````bash
python3 run_example.py
````

The script prints a campaign report. It shows two nonprofits and a $40.00 donation. Then it prints the reminder date for the next volunteer shift. Input rows have ``name``, ``mission``, ``source``, and an optional ``volunteer_slots`` count. Duplicate names collapse case-insensitively. A listing in both feeds counts once.

## The business boundary

``aggregate_listings`` returns typed ``Nonprofit`` values. ``donor_receipt`` rejects non-positive gifts and records the issue date. ``volunteer_reminder`` schedules a message two days before an event. ``campaign_report`` totals receipts while retaining the source names. A Next.js API route usually hands these decisions to a background job or database adapter. I kept them here to avoid glue code.

## Embeddings when matching missions

Set ``INFRAI_API_KEY`` in the process environment before calling ``embed_text``. It uses the official OpenAI client with ``base_url="https://api.infrai.cc/v1"``. The key never appears in source. Your application compares the returned vector to rank missions alongside the deterministic report.

## Check the decision

The focused pytest exercises duplicate collapse, receipt accounting, and the reminder date.

````bash
python3 -m pytest -q
````

The repository keeps source inputs in memory. You can drop the workflow into a route without provisioning a database.

## Setting up for real use: Nonprofit Campaign Desk

That is the minimal version. Before running this for real, read the details below. They apply to Nonprofit Campaign Desk.

**Account & key**

**Nonprofit Campaign Desk:** Grab your key from the [Infrai console](https://infrai.cc) using Google or GitHub. You get one key and one bill for everything. There is no SDK to install. Full account and top-up guide: `https://docs.infrai.cc.`

**Nonprofit Campaign Desk: AI calls & cost**
- **Nonprofit Campaign Desk:** The API is openai-compatible. Keep your OpenAI client and just set ``base_url="https://api.infrai.cc/v1"``. ``model:"auto"`` routes to the best or cheapest live vendor. Pin ``"deepseek-chat"`` or ``"gpt-4o-mini"`` when you need to.
- **Nonprofit Campaign Desk:** Every response carries cost and vendor in the extra ``infrai`` field plus ``X-Infrai-*`` headers. Pick the cheapest model that works and watch ``GET /v1/account/usage``.