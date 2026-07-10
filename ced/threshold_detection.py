"""Threshold evidence under bounded false positives.

This extension drops the zero-false-positive certificate. A positive read is no
longer proof of presence. Instead, repeated reads are summarized by a threshold
event: at least ``t`` positives in ``n`` reads. Given a sensitivity lower bound
``p_min`` under presence and a false-positive upper bound ``f_max`` under
absence, the threshold event has a posterior-free evidence-ratio lower bound:

    P(event | present) / P(event | absent)

using the conservative binomial tail at ``p_min`` divided by the binomial tail at
``f_max``. The model is a design contract, not an inference of the bounds from
the observed record.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb, fsum, inf, isfinite


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _probability(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return probability


def binomial_probability(trials: int, positives: int, probability: float) -> float:
    """Probability of exactly ``positives`` successes in ``trials`` Bernoulli reads."""
    trials = _positive_int("trials", trials)
    if not isinstance(positives, int) or isinstance(positives, bool) or not 0 <= positives <= trials:
        raise ValueError("positives must be an integer in [0, trials]")
    probability = _probability("probability", probability)
    return comb(trials, positives) * probability**positives * (1.0 - probability) ** (
        trials - positives
    )


def binomial_tail(trials: int, threshold: int, probability: float) -> float:
    """Probability of at least ``threshold`` successes in ``trials`` reads."""
    trials = _positive_int("trials", trials)
    if not isinstance(threshold, int) or isinstance(threshold, bool) or not 0 <= threshold <= trials:
        raise ValueError("threshold must be an integer in [0, trials]")
    probability = _probability("probability", probability)
    if threshold == 0:
        return 1.0
    return fsum(binomial_probability(trials, k, probability) for k in range(threshold, trials + 1))


@dataclass(frozen=True)
class ThresholdEvidenceDesign:
    """Repeated binary reads with a positive-count evidence threshold.

    ``sensitivity_lower_bound`` is the smallest allowed per-read positive
    probability when the coordinate is present. ``false_positive_upper_bound`` is
    the largest allowed per-read positive probability when the coordinate is
    absent. Reads are conditionally independent under both hypotheses.
    """

    read_count: int
    positive_threshold: int
    sensitivity_lower_bound: float
    false_positive_upper_bound: float

    def __post_init__(self) -> None:
        _positive_int("read_count", self.read_count)
        if (
            not isinstance(self.positive_threshold, int)
            or isinstance(self.positive_threshold, bool)
            or not 1 <= self.positive_threshold <= self.read_count
        ):
            raise ValueError("positive_threshold must be an integer in [1, read_count]")
        sensitivity = _probability("sensitivity_lower_bound", self.sensitivity_lower_bound)
        false_positive = _probability(
            "false_positive_upper_bound", self.false_positive_upper_bound
        )
        if not false_positive < sensitivity:
            raise ValueError(
                "false_positive_upper_bound must be strictly below sensitivity_lower_bound"
            )
        object.__setattr__(self, "sensitivity_lower_bound", sensitivity)
        object.__setattr__(self, "false_positive_upper_bound", false_positive)

    @property
    def detection_probability_lower_bound(self) -> float:
        """Lower probability of crossing the threshold when the coordinate exists."""
        return binomial_tail(
            self.read_count, self.positive_threshold, self.sensitivity_lower_bound
        )

    @property
    def false_alert_probability_upper_bound(self) -> float:
        """Upper probability of crossing the threshold when the coordinate is absent."""
        return binomial_tail(
            self.read_count, self.positive_threshold, self.false_positive_upper_bound
        )

    @property
    def evidence_ratio_lower_bound(self) -> float:
        """Posterior-free likelihood-ratio lower bound for the threshold event."""
        false_alert = self.false_alert_probability_upper_bound
        if false_alert == 0.0:
            return inf
        return self.detection_probability_lower_bound / false_alert

    @property
    def threshold_is_presence_certificate(self) -> bool:
        """Whether crossing the threshold is deductive evidence of presence."""
        return self.false_alert_probability_upper_bound == 0.0

    def accepts(self, positive_count: int) -> bool:
        """Whether an observed positive count crosses the evidence threshold."""
        if (
            not isinstance(positive_count, int)
            or isinstance(positive_count, bool)
            or not 0 <= positive_count <= self.read_count
        ):
            raise ValueError("positive_count must be an integer in [0, read_count]")
        return positive_count >= self.positive_threshold

    @classmethod
    def minimum_threshold_for_evidence_ratio(
        cls,
        read_count: int,
        sensitivity_lower_bound: float,
        false_positive_upper_bound: float,
        target_ratio: float,
    ) -> int:
        """Smallest threshold whose event-level evidence ratio meets the target."""
        read_count = _positive_int("read_count", read_count)
        if not isinstance(target_ratio, (int, float)) or isinstance(target_ratio, bool):
            raise ValueError("target_ratio must be finite and positive")
        target = float(target_ratio)
        if not isfinite(target) or target <= 0.0:
            raise ValueError("target_ratio must be finite and positive")
        for threshold in range(1, read_count + 1):
            design = cls(
                read_count,
                threshold,
                sensitivity_lower_bound,
                false_positive_upper_bound,
            )
            if design.evidence_ratio_lower_bound >= target:
                return threshold
        raise ValueError("no threshold reaches the requested evidence ratio")

    def verify(self) -> bool:
        return (
            0.0 <= self.false_alert_probability_upper_bound <= 1.0
            and 0.0 <= self.detection_probability_lower_bound <= 1.0
            and self.evidence_ratio_lower_bound >= 1.0
        )
