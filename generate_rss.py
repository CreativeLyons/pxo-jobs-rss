import requests
from datetime import datetime, timezone
from email.utils import format_datetime
import html

# Workable JSON endpoint for the "pxo" account
JSON_URL = "https://apply.workable.com/api/v1/widget/accounts/pxo"

def main():
    data = requests.get(JSON_URL, timeout=30).json()
    jobs = data.get("jobs", [])

    now = format_datetime(datetime.now(timezone.utc))

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<rss version="2.0">')
    print("<channel>")
    print("<title>PXO Jobs</title>")
    print("<link>https://apply.workable.com/pxo/</link>")
    print("<description>Latest job openings at PXO (Workable)</description>")
    print(f"<lastBuildDate>{now}</lastBuildDate>")

    # remove duplicates by job URL
    seen = set()

    for job in jobs:
        url = job.get("url", "")
        if not url or url in seen:
            continue
        seen.add(url)

        title = html.escape(job.get("title", ""))
        link = html.escape(url)
        location = html.escape(job.get("location", ""))

        print("<item>")
        print(f"<title>{title}</title>")
        print(f"<link>{link}</link>")
        print(f'<guid isPermaLink="true">{link}</guid>')
        if location:
            print(f"<description>{location}</description>")
        print(f"<pubDate>{now}</pubDate>")
        print("</item>")

    print("</channel>")
    print("</rss>")

if __name__ == "__main__":
    main()
