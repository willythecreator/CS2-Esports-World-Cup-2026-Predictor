from scraper.fetch import fetch_page
from scraper.parse_results import parse_results_page

html = fetch_page("https://www.hltv.org/results?stars=3")
results = parse_results_page(html)

print(f"Found {len(results)} matches")
print(results[:3])