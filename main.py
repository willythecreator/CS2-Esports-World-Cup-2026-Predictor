import subprocess
import sys
import os

PYTHON = sys.executable


def run(label, cmd):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=False)
    if result.returncode != 0:
        print(f"FAILED: {label}")
        sys.exit(1)


if __name__ == "__main__":
    print("CS2 Esports World Cup 2026 Predictor Pipeline")
    print("Make sure you have scraped data before running this.\n")

    # Step 1: Build features from scraped data
    run("Step 1: Building features", [PYTHON, "features/build_features.py"])

    # Step 2: Train and evaluate models
    run("Step 2: Training models", [PYTHON, "-m", "models.train"])

    # Step 3: Quick demo prediction
    run("Step 3: Demo prediction", [PYTHON, "predict.py", "Falcons", "Vitality"])