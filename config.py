import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

RESULTS_CSV = os.path.join(ROOT_DIR, "data", "processed", "results.csv")
RANKING_CSV = os.path.join(ROOT_DIR, "data", "processed", "team_ranking.csv")
FEATURES_CSV = os.path.join(ROOT_DIR, "data", "processed", "features.csv")
MODEL_PATH = os.path.join(ROOT_DIR, "models", "model.pkl")

# Features used for training
FEATURE_COLS = [
    "team_a_rank",
    "team_b_rank",
    "rank_diff",
    "team_a_points",
    "team_b_points",
    "points_diff",
]

TEST_SIZE = 0.2
RANDOM_STATE = 42