import requests
from datetime import datetime, timezone
from email.utils import format_datetime
import html

JSON_URL = "https://apply.workable.com/api/v1/widget/accounts/pxo"

data = requests.get(JSON_URL, timeout=30).json()
jobs = data.get("jobs", [])

now = format_datetime(datetime.now(timezone.utc))

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<rss version="2.0">')
print('<channel>')
print('<title>PXO Jobs</title>')
print('<link>https://apply.workable.com/pxo/</link>')
print('<description>Latest job openings at PXO (Workable)</description>')
print(f'<lastBuildDate>{now}</lastBuildDate>')

for job in jobs:
    title = html.escape(job["title"])
    link = html.escape(job["url"])
    location = html.escape(job.get("location", ""))
    guid = link

    print('<item>')
    print(f'<title>{title}</title>')
    print(f'<link>{link}</link>')
    print(f'<guid isPermaLink="true">{guid}</guid>')
    print(f'<description>{location}</description>')
    print(f'<pubDate>{now}</pubDate>')
    print('</item>')

print('</channel>')
print('</rss>')
