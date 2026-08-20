import os
import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FEATURES_CSV, FEATURE_COLS, MODEL_PATH, TEST_SIZE, RANDOM_STATE
from models.baseline import get_models, evaluate


def load_data():
    df = pd.read_csv(FEATURES_CSV)
    X = df[FEATURE_COLS].values
    y = df["team_a_win"].values
    return X, y, df


def train():
    X, y, df = load_data()
    print(f"Loaded {len(X)} samples, {X.shape[1]} features")
    print(f"Label distribution: {np.mean(y):.2%} team_a wins")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = get_models()
    best_model = None
    best_auc = 0
    best_name = ""

    for name, model in models.items():
        # Scale for logistic regression, not for tree-based
        if name == "logistic_regression":
            model.fit(X_train_s, y_train)
            metrics = evaluate(model, X_test_s, y_test)
        else:
            model.fit(X_train, y_train)
            metrics = evaluate(model, X_test, y_test)

        print(f"\n--- {name} ---")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

        if metrics["roc_auc"] > best_auc:
            best_auc = metrics["roc_auc"]
            best_model = model
            best_name = name

    print(f"\nBest model: {best_name} (AUC={best_auc:.4f})")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"model": best_model, "scaler": scaler, "name": best_name}, f)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train()