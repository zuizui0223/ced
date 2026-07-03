"""One-sided imperfect detection limits and risk-limited repeat design.

The model is intentionally narrow.  A latent binary coordinate is either absent
(then every read is negative) or present (then each conditionally independent
read is positive with probability at least ``p_min``).  False positives are
excluded by contract.  Consequently, a positive is a certificate of presence,
while finitely many negatives need not certify absence.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isfinite, log
from typing import Iterable


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _open_unit_interval(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 < probability < 1.0:
        raise ValueError(f"{name} must lie strictly between zero and one")
    return probability


@dataclass(frozen=True)
class OneSidedDetector:
    """Declared lower sensitivity for a zero-false-positive detector.

    For a truly present coordinate, each resettable read is positive with
    probability at least ``sensitivity_lower_bound`` and reads are conditionally
    independent.  For a truly absent coordinate every read is negative.
    """

    sensitivity_lower_bound: float

    def __post_init__(self) -> None:
        if not isinstance(self.sensitivity_lower_bound, (int, float)) or isinstance(
            self.sensitivity_lower_bound, bool
        ):
            raise ValueError("sensitivity_lower_bound must be a finite probability")
        probability = float(self.sensitivity_lower_bound)
        if not isfinite(probability) or not 0.0 < probability <= 1.0:
            raise ValueError("sensitivity_lower_bound must lie in (0, 1]")
        object.__setattr__(self, "sensitivity_lower_bound", probability)

    def all_negative_probability_if_present(self, repetitions: int) -> float:
        """Largest all-negative probability compatible with the sensitivity bound."""
        repetitions = _nonnegative_int("repetitions", repetitions)
        return (1.0 - self.sensitivity_lower_bound) ** repetitions

    def any_positive_probability_if_present(self, repetitions: int) -> float:
        """Lower probability of at least one positive for a present coordinate."""
        return 1.0 - self.all_negative_probability_if_present(repetitions)

    def all_negative_is_compatible_with_presence(self, repetitions: int) -> bool:
        """Whether an all-negative record has positive probability under presence."""
        return self.all_negative_probability_if_present(repetitions) > 0.0

    @staticmethod
    def positive_observation_certifies_presence(any_positive: bool) -> bool:
        """Under the declared zero-false-positive contract, only a positive certifies."""
        if not isinstance(any_positive, bool):
            raise ValueError("any_positive must be bool")
        return any_positive

    def repetitions_for_single_coordinate_confidence(self, confidence: float) -> int:
        """Least positive repeat count whose detection lower bound reaches confidence."""
        confidence = _open_unit_interval("confidence", confidence)
        if self.sensitivity_lower_bound == 1.0:
            return 1
        repeats = max(
            1,
            ceil(log(1.0 - confidence) / log(1.0 - self.sensitivity_lower_bound)),
        )
        while self.any_positive_probability_if_present(repeats) < confidence:
            repeats += 1
        while (
            repeats > 1
            and self.any_positive_probability_if_present(repeats - 1) >= confidence
        ):
            repeats -= 1
        return repeats

    def repetitions_for_joint_detection_confidence(
        self, coordinate_count: int, confidence: float
    ) -> int:
        """Least uniform repeat count for joint detection of present coordinates.

        The guarantee is ``[1 - (1 - p_min)**r]**k >= confidence`` for ``k``
        required coordinates, conditional on the declared independence contract.
        """
        coordinate_count = _positive_int("coordinate_count", coordinate_count)
        confidence = _open_unit_interval("confidence", confidence)
        per_coordinate_confidence = confidence ** (1.0 / coordinate_count)
        return self.repetitions_for_single_coordinate_confidence(per_coordinate_confidence)


@dataclass(frozen=True)
class OneSidedDetectionPanel:
    """A resettable repeated-read panel under one-sided imperfect detection."""

    coordinate_count: int
    repetitions_per_coordinate: int
    detector: OneSidedDetector

    def __post_init__(self) -> None:
        _positive_int("coordinate_count", self.coordinate_count)
        _nonnegative_int("repetitions_per_coordinate", self.repetitions_per_coordinate)
        if not isinstance(self.detector, OneSidedDetector):
            raise ValueError("detector must be a OneSidedDetector")

    @property
    def total_reads(self) -> int:
        return self.coordinate_count * self.repetitions_per_coordinate

    @property
    def joint_detection_lower_bound(self) -> float:
        return self.detector.any_positive_probability_if_present(
            self.repetitions_per_coordinate
        ) ** self.coordinate_count

    @property
    def all_negative_record_is_ambiguous(self) -> bool:
        """A full negative panel still permits the all-present latent state."""
        return self.detector.all_negative_is_compatible_with_presence(
            self.repetitions_per_coordinate
        )

    def positive_signature(self, observations: Iterable[Iterable[bool]]) -> frozenset[int]:
        """Coordinates certified present by at least one observed positive.

        The input has one iterable of binary reads per coordinate.  A coordinate
        without a positive remains undecided rather than certified absent.
        """
        rows = tuple(tuple(row) for row in observations)
        if len(rows) != self.coordinate_count:
            raise ValueError("observations must provide one row per coordinate")
        certified: set[int] = set()
        for index, row in enumerate(rows):
            if len(row) != self.repetitions_per_coordinate:
                raise ValueError("each observation row must match repetitions_per_coordinate")
            if any(not isinstance(value, bool) for value in row):
                raise ValueError("observations must be bool")
            if any(row):
                certified.add(index)
        return frozenset(certified)

    def verify(self) -> bool:
        return (
            self.total_reads
            == self.coordinate_count * self.repetitions_per_coordinate
            and 0.0 <= self.joint_detection_lower_bound <= 1.0
        )
