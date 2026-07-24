import csv
import os
from scraper.fetch import fetch_page
from scraper.parse_results import parse_results_page

OUTPUT_PATH = os.path.join("data", "processed", "results.csv")
FIELDNAMES = ["match_id", "team_a", "team_b", "score_a","score_b", "event", "format", "map_played"]

def collect_results(max_pages: int = 5, stars: int = 3):
    """
    Scrape multiple pages of HLTV results and save to a CSV
    Deduplicates by match_id in case pages overlap across runs
    """
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Load existing match IDs if the file already exists, to avoid duplicates
    seen_ids = set()
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                seen_ids.add(int(row["match_id"]))

    all_new_matches = []

    for page_num in range(max_pages):
        offset = page_num * 100
        url = f"https://www.hltv.org/results?offset={offset}&stars={stars}"
        html = fetch_page(url)
        matches = parse_results_page(html)

        new_matches = [m for m in matches if m["match_id"] not in seen_ids]
        for m in new_matches:
            seen_ids.add(m["match_id"])

        print(f"Page offset={offset}: {len(matches)} parsed, {len(new_matches)} new")
        all_new_matches.extend(new_matches)

    if not all_new_matches:
        print("No new matches found")
        return

    file_exists = os.path.exists(OUTPUT_PATH)
    with open(OUTPUT_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerows(all_new_matches)

    print(f"Saved {len(all_new_matches)} new matches to {OUTPUT_PATH}")

if __name__ == "__main__":
    collect_results(max_pages=5, stars=3)