import csv
import os
from scraper.fetch import fetch_page
from scraper.parse_teams import parse_ranking_page

OUTPUT_PATH = os.path.join("data", "processed", "team_ranking.csv")
FIELDNAMES = ["rank", "team_id", "team_name", "points"]

URL = "https://www.hltv.org/ranking/teams"

def collect_ranking():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    html = fetch_page(URL)
    teams = parse_ranking_page(html)

    print(f"Found {len(teams)} ranked teams")

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(teams)

    print(f"Saved {len(teams)} teams to {OUTPUT_PATH}")

if __name__ == "__main__":
    collect_ranking()