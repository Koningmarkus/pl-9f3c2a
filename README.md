# Markus Planner

A paper style annual wall planner. Twelve months at a time, one row per month,
entries written across the days they span.

Everything lives in this repository. There is no server and no account to lose.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The planner. This is what GitHub Pages serves. |
| `data.json` | The entries, the pens and the leave allowance. The master copy. |
| `planner.ics` | Calendar feed, rebuilt automatically whenever `data.json` changes. |
| `make_ics.py` | Builds `planner.ics` from `data.json`. |
| `.github/workflows/ics.yml` | Runs `make_ics.py` on every change. |

## Setting it up

1. Create a repository. A name nobody would guess is wise, because GitHub Pages
   on a free account is public.
2. Upload every file in this folder, keeping `.github/workflows/ics.yml` in its
   folder.
3. Settings, Pages, Source "Deploy from a branch", branch `main`, folder `/ (root)`.
   A minute later the planner is at `https://<user>.github.io/<repo>/`.
4. Settings, Actions, General, Workflow permissions, set "Read and write
   permissions" so the feed can rebuild itself.
5. Open the planner, press the cog, and fill in your GitHub user and the
   repository name.

## Letting the planner save

Saving writes `data.json` back through the GitHub API, so it needs a token.

1. github.com, Settings, Developer settings, Personal access tokens,
   Fine grained tokens, Generate new token.
2. Repository access: only this repository.
3. Permissions: Repository permissions, Contents, Read and write. Nothing else.
4. Expiry: whatever you are comfortable with. You will need to replace it when
   it lapses.
5. Paste it into the cog panel in the planner.

The token is kept in that browser's own storage on that device. It is never
written into the repository and never sent anywhere except github.com. Put it in
once on the laptop and once on the phone. Without a token the planner still
loads and displays, it just cannot save.

## Subscribing in Outlook or on a phone

The feed is at `https://<user>.github.io/<repo>/planner.ics`.

- Outlook on the web: Add calendar, Subscribe from web, paste the URL.
- iPhone: Settings, Calendar, Accounts, Add Account, Other, Add Subscribed Calendar.

It arrives as a separate read only calendar alongside your own. Outlook refreshes
subscribed calendars on its own schedule, often several hours behind rather than
instantly, and some work tenants block external calendars altogether.

## The data format

```json
{
  "version": 1,
  "leaveAllowance": 24,
  "pens":   [ { "id": "leave", "name": "Annual leave", "color": "#E0362A", "leave": true } ],
  "events": [ { "id": "ev01", "start": "2026-05-26", "end": "2026-06-01",
                "label": "Leave", "cat": "leave" } ]
}
```

`start` and `end` are both inclusive. `cat` points at a pen `id`. A pen with
`"leave": true` counts towards the allowance, and only working days count, so
weekends and England and Wales bank holidays inside a span are free.

Any agent that can fetch a URL can read `data.json` or `planner.ics` directly.
Any agent with a GitHub token can edit `data.json` the same way the page does.
