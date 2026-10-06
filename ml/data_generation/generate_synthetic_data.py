"""Synthetic data generator for Planova goal completion trajectories.

Status: Phase 0 Stub. Implementation scheduled for Phase 7.
"""

import argparse


def generate_synthetic_goals(num_samples: int = 5000, seed: int = 42) -> None:
    """Generate synthetic user goal trajectories with realistic causal relationships and archetypes.

    Raises:
        NotImplementedError: Phase 7 synthetic data generator implementation pending.
    """
    raise NotImplementedError(
        "Phase 7: Synthetic data generator is stubbed in Phase 0."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Planova data.")
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data/synthetic_goals.csv")
    args = parser.parse_args()

    raise NotImplementedError(
        "Phase 7: Synthetic data generation CLI entrypoint is stubbed in Phase 0."
    )
