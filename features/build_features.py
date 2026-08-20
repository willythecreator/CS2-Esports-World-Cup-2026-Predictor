import csv
import os
import random
import hashlib

RESULTS_PATH = os.path.join("data", "processed", "results.csv")
RANKING_PATH = os.path.join("data", "processed", "team_ranking.csv")
OUTPUT_PATH = os.path.join("data", "processed", "features.csv")

FIELDNAMES = [
    "match_id", "team_a", "team_b", "event", "format",
    "team_a_rank", "team_b_rank", "rank_diff",
    "team_a_points", "team_b_points", "points_diff",
    "score_a", "score_b",
    "team_a_win",
]


def load_ranking():
    ranking = {}
    with open(RANKING_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ranking[row["team_name"]] = {
                "rank": int(row["rank"]),
                "points": int(row["points"]) if row["points"] else 0,
            }
    return ranking


def deterministic_swap(match_id):
    """Use match_id to deterministically decide orientation so the same
    match always maps to the same label, but overall ~50% are swapped."""
    h = hashlib.md5(str(match_id).encode()).hexdigest()
    return int(h, 16) % 2 == 0


def build_features():
    ranking = load_ranking()
    rows = []
    unmatched_teams = set()

    with open(RESULTS_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for match in reader:
            team_a = match["team_a"]
            team_b = match["team_b"]

            a_info = ranking.get(team_a)
            b_info = ranking.get(team_b)

            if a_info is None:
                unmatched_teams.add(team_a)
            if b_info is None:
                unmatched_teams.add(team_b)

            if a_info is None or b_info is None:
                continue

            score_a = int(match["score_a"])
            score_b = int(match["score_b"])

            # Deterministic swap so team_a isn't always the winner
            swap = deterministic_swap(match["match_id"])
            if swap:
                team_a, team_b = team_b, team_a
                a_info, b_info = b_info, a_info
                score_a, score_b = score_b, score_a

            team_a_win = 1 if score_a > score_b else 0

            # Score dominance: how decisively was it won (max possible maps)
            fmt = match.get("format", "bo3")
            max_maps = 5 if fmt == "bo5" else 3 if fmt == "bo3" else 1
            total_maps = score_a + score_b
            score_diff = score_a - score_b
            dominance = score_diff / max_maps if max_maps > 0 else 0

            rows.append({
                "match_id": match["match_id"],
                "team_a": team_a,
                "team_b": team_b,
                "event": match.get("event", ""),
                "format": fmt,
                "team_a_rank": a_info["rank"],
                "team_b_rank": b_info["rank"],
                "rank_diff": a_info["rank"] - b_info["rank"],
                "team_a_points": a_info["points"],
                "team_b_points": b_info["points"],
                "points_diff": a_info["points"] - b_info["points"],
                "score_a": score_a,
                "score_b": score_b,
                "team_a_win": team_a_win,
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Built {len(rows)} feature rows from {RESULTS_PATH}")
    print(f"Skipped matches due to {len(unmatched_teams)} unmatched teams: {sorted(unmatched_teams)[:20]}")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_features()