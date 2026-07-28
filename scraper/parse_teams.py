import re
from bs4 import BeautifulSoup

def parse_team_stats_page(html: str) -> list[dict]:
    """
    Parse an HLTV /stats/teams page into a list of team stat dicts
    Each dict: team_id, team_name, maps_played, kd_diff, kd, rating
    """
    soup = BeautifulSoup(html, "html.parser")
    teams = []

    table = soup.select_one("table.stats-table")
    if not table:
        return teams

    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 5:
            continue

        team_link = cells[0].select_one("a")
        if not team_link:
            continue

        href = team_link.get("href", "")
        id_match = re.search(r"/stats/teams/(\d+)/", href)
        if not id_match:
            continue
        team_id = int(id_match.group(1))

        team_name = team_link.get_text(strip=True)
        maps_played = cells[1].get_text(strip=True)
        kd_diff = cells[2].get_text(strip=True)
        kd = cells[3].get_text(strip=True)
        rating = cells[4].get_text(strip=True)

        teams.append({
            "team_id": team_id,
            "team_name": team_name,
            "maps_played": maps_played,
            "kd_diff": kd_diff,
            "kd": kd,
            "rating": rating,
        })

    return teams

def parse_ranking_page(html: str) -> list[dict]:
    """
    Parse an HLTV /ranking/teams page into a list of team ranking dicts
    Each dict: rank, team_id, team_name, points
    """
    soup = BeautifulSoup(html, "html.parser")
    teams = []

    for team_block in soup.select(".ranked-team"):
        position_el = team_block.select_one(".position")
        if not position_el:
            continue
        rank_text = position_el.get_text(strip=True).lstrip("#")
        if not rank_text.isdigit():
            continue
        rank = int(rank_text)

        name_el = team_block.select_one(".name")
        team_name = name_el.get_text(strip=True) if name_el else None

        points_el = team_block.select_one(".points")
        points = None
        if points_el:
            points_match = re.search(r"([\d,]+)", points_el.get_text(strip=True))
            if points_match:
                points = int(points_match.group(1).replace(",", ""))

        team_link = team_block.select_one("a[href^='/team/']")
        team_id = None
        if team_link:
            id_match = re.search(r"/team/(\d+)/", team_link.get("href", ""))
            if id_match:
                team_id = int(id_match.group(1))

        if team_name and team_id:
            teams.append({
                "rank": rank,
                "team_id": team_id,
                "team_name": team_name,
                "points": points,
            })

    return teams