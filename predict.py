import os
import sys
import pickle
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import RANKING_CSV, MODEL_PATH, FEATURE_COLS


def load_ranking():
    df = pd.read_csv(RANKING_CSV)
    return {row["team_name"]: {"rank": row["rank"], "points": row["points"]}
            for _, row in df.iterrows()}


def predict(team_a: str, team_b: str):
    ranking = load_ranking()

    if team_a not in ranking:
        print(f"Warning: '{team_a}' not in rankings, using rank=100, points=0")
        a = {"rank": 100, "points": 0}
    else:
        a = ranking[team_a]

    if team_b not in ranking:
        print(f"Warning: '{team_b}' not in rankings, using rank=100, points=0")
        b = {"rank": 100, "points": 0}
    else:
        b = ranking[team_b]

    features = [[
        a["rank"], b["rank"],
        a["rank"] - b["rank"],
        a["points"], b["points"],
        a["points"] - b["points"],
    ]]

    with open(MODEL_PATH, "rb") as f:
        artifact = pickle.load(f)

    model = artifact["model"]
    scaler = artifact["scaler"]

    if artifact["name"] == "logistic_regression":
        features = scaler.transform(features)

    prob = model.predict_proba(features)[0]
    win_a = prob[1]
    win_b = prob[0]

    print(f"\n{team_a} vs {team_b}")
    print(f"  {team_a} win probability: {win_a:.1%}")
    print(f"  {team_b} win probability: {win_b:.1%}")
    print(f"  Prediction: {team_a if win_a > win_b else team_b}")

    return win_a, win_b


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Predict CS2 match outcome")
    parser.add_argument("team_a", help="First team name")
    parser.add_argument("team_b", help="Second team name")
    args = parser.parse_args()
    predict(args.team_a, args.team_b)