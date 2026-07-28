import csv
import os
from scraper.fetch import fetch_page
from scraper.parse_teams import parse_team_stats_page

# NOTE: This targets HLTV's /stats/teams page, which is protected by a
# Cloudflare Turnstile challenge that blocks headless browsers even with
# stealth patches (tried: headless, non-headless, playwright-stealth,
# extended waits). Abandoned in favor of /ranking/teams instead
# (see collect_ranking.py), which isn't behind the same protection.

OUTPUT_PATH = os.path.join("data", "processed", "team_stats.csv")
FIELDNAMES = ["team_id", "team_name", "maps_played", "kd_diff", "kd", "rating"]

URL = "https://www.hltv.org/stats/teams?startDate=2025-07-25&endDate=2026-07-25&rankingFilter=Top30"

def collect_team_stats():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    html = fetch_page(URL)
    teams = parse_team_stats_page(html)

    print(f"Saved {len(teams)} teams to {OUTPUT_PATH}")

if __name__ == "__main__":
    collect_team_stats()