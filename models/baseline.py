from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
import numpy as np


def get_models():
    """Return dict of named models to compare."""
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, C=1.0),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=3,
            random_state=42,
        ),
    }


def evaluate(model, X_test, y_test):
    """Return dict of evaluation metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "log_loss": log_loss(y_test, y_proba),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }