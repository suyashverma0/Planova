"""Feature extraction & computation module for Planova ML pipeline.

Status: Phase 0 Stub. Implementation scheduled for Phase 7 / Phase 8.
"""

from typing import Any
import pandas as pd


def extract_features(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Extract and engineer tabular features from raw goal telemetry.

    Raises:
        NotImplementedError: Phase 7 feature engineering pipeline implementation pending.
    """
    raise NotImplementedError(
        "Phase 7: Feature extraction pipeline is stubbed in Phase 0."
    )


def compute_deadline_pressure(remaining_hours: float, remaining_days: float, daily_hours: float) -> float:
    """Compute workload ratio: remaining_hours / (remaining_days * daily_hours).

    Raises:
        NotImplementedError: Phase 7 feature engineering pipeline implementation pending.
    """
    raise NotImplementedError(
        "Phase 7: Feature extraction pipeline is stubbed in Phase 0."
    )
