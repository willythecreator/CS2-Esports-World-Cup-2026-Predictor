import re
from bs4 import BeautifulSoup


def parse_results_page(html: str) -> list[dict]:
    """
    Parse an HLTV /results page into a list of match dicts.
    Each dict: match_id, team_a, team_b, score_a, score_b, event, format
    """
    soup = BeautifulSoup(html, "html.parser")
    matches = []

    # Each match result is wrapped in an <a> tag linking to /matches/<id>/...
    for match_link in soup.select("a.a-reset[href^='/matches/']"):
        href = match_link.get("href", "")

        # Extract numeric match ID from the URL, e.g. /matches/2395826/...
        id_match = re.search(r"/matches/(\d+)/", href)
        if not id_match:
            continue
        match_id = int(id_match.group(1))

        # Team names
        team_cells = match_link.select(".team")
        if len(team_cells) < 2:
            continue
        team_a = team_cells[0].get_text(strip=True)
        team_b = team_cells[1].get_text(strip=True)

        # Score
        score_won = match_link.select_one(".score-won")
        score_lost = match_link.select_one(".score-lost")
        if not score_won or not score_lost:
            continue

        score_a_text = score_won.get_text(strip=True)
        score_b_text = score_lost.get_text(strip=True)

        # Event name
        event_el = match_link.select_one(".event-name")
        event = event_el.get_text(strip=True) if event_el else None

        # Format (bo3, bo5, def, etc.)
        format_el = match_link.select_one(".map-text")
        raw_format = format_el.get_text(strip=True) if format_el else None

        # Skip defaults/forfeits - not real gameplay outcomes
        if raw_format == "def":
            continue

        MAP_CODES = {"d2", "inf", "nuke", "anc", "mrg", "anb", "vtg", "trn"}
        if raw_format in MAP_CODES:
            match_format = "bo1"
            map_played = raw_format
        else:
            match_format = raw_format
            map_played = None

        matches.append({
            "match_id": match_id,
            "team_a": team_a,
            "team_b": team_b,
            "score_a": score_a_text,
            "score_b": score_b_text,
            "event": event,
            "format": match_format,
            "map_played": map_played,
        })
        
    return matches