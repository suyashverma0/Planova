"""Model training and MLflow experiment logging pipeline.

Status: Phase 0 Stub. Implementation scheduled for Phase 7 / Phase 8.
"""

from typing import Any, Dict


def train_model(
    train_data_path: str, val_data_path: str, model_type: str = "xgboost"
) -> Dict[str, Any]:
    """Train candidate machine learning model and log artifacts to MLflow.

    Raises:
        NotImplementedError: Phase 8 training & MLflow logging implementation pending.
    """
    raise NotImplementedError(
        "Phase 8: Model training pipeline is stubbed in Phase 0."
    )


if __name__ == "__main__":
    raise NotImplementedError(
        "Phase 8: Training CLI entrypoint is stubbed in Phase 0."
    )
