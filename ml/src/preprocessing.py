"""Preprocessing, scaling, and dataset splitting module.

Status: Phase 0 Stub. Implementation scheduled for Phase 7 / Phase 8.
"""

from typing import Any, Tuple
import pandas as pd


def build_preprocessor() -> Any:
    """Build scikit-learn ColumnTransformer for categorical & numeric features.

    Raises:
        NotImplementedError: Phase 7 preprocessing implementation pending.
    """
    raise NotImplementedError(
        "Phase 7: Preprocessing pipeline is stubbed in Phase 0."
    )


def grouped_split(
    df: pd.DataFrame, group_col: str = "user_id"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform group-isolated train/validation/test split based on user_id or goal_id.

    Raises:
        NotImplementedError: Phase 7 dataset splitting implementation pending.
    """
    raise NotImplementedError(
        "Phase 7: Grouped splitting is stubbed in Phase 0."
    )
