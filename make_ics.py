#!/usr/bin/env python3
"""Rebuild planner.ics from data.json. Run by GitHub Actions on every change."""
import json, datetime

BH = {
 "2026-01-01","2026-04-03","2026-04-06","2026-05-04","2026-05-25","2026-08-31","2026-12-25","2026-12-28",
 "2027-01-01","2027-03-26","2027-03-29","2027-05-03","2027-05-31","2027-08-30","2027-12-27","2027-12-28",
 "2028-01-03","2028-04-14","2028-04-17","2028-05-01","2028-05-29","2028-08-28","2028-12-25","2028-12-26",
 "2029-01-01","2029-03-30","2029-04-02","2029-05-07","2029-05-28","2029-08-27","2029-12-25","2029-12-26",
}

def d(s): return datetime.date.fromisoformat(s)

def workdays(a, b):
    n, c = 0, d(a)
    while c <= d(b):
        if c.weekday() < 5 and c.isoformat() not in BH:
            n += 1
        c += datetime.timedelta(days=1)
    return n

def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\;").replace(",", "\\,").replace("\n", "\\n")

def fold(line):
    out, b = [], line.encode("utf-8")
    while len(b) > 73:
        cut = 73
        while cut > 1 and (b[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(b[:cut].decode("utf-8"))
        b = b" " + b[cut:]
    out.append(b.decode("utf-8"))
    return out

doc = json.load(open("data.json"))
names = {p["id"]: p.get("name", p["id"]) for p in doc.get("pens", [])}
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Markus Planner//EN",
     "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
     "X-WR-CALNAME:Markus Planner", "X-WR-TIMEZONE:Europe/London",
     "REFRESH-INTERVAL;VALUE=DURATION:PT2H", "X-PUBLISHED-TTL:PT2H"]

for e in sorted(doc.get("events", []), key=lambda x: (x["start"], x.get("id", ""))):
    cat = e.get("cat", "")
    name = names.get(cat, cat)
    L += ["BEGIN:VEVENT",
          "UID:%s@markus-planner" % e.get("id", e["start"]),
          "DTSTAMP:" + stamp,
          "DTSTART;VALUE=DATE:" + e["start"].replace("-", ""),
          "DTEND;VALUE=DATE:" + (d(e["end"]) + datetime.timedelta(days=1)).isoformat().replace("-", ""),
          "SUMMARY:" + esc(e.get("label") or name),
          "CATEGORIES:" + esc(name),
          "DESCRIPTION:" + esc("%s. %d working day(s)." % (name, workdays(e["start"], e["end"]))),
          "TRANSP:TRANSPARENT", "END:VEVENT"]

L.append("END:VCALENDAR")
outl = []
for line in L:
    outl.extend(fold(line))
open("planner.ics", "w", newline="").write("\r\n".join(outl) + "\r\n")
print("wrote planner.ics with %d events" % len(doc.get("events", [])))
