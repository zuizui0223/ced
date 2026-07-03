"""Mode-diverse one-sided detection under common-mode observation failure.

A mode is a shared exposure domain such as a camera-power-weather combination,
a sampling date, or an observer route. If a mode fails, every coordinate and
repeat assigned to that mode is negative together. Repeats within an operating
mode improve sensitivity, but only additional independent modes reduce the
probability that every assigned observation is lost together.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, comb, fsum, isfinite, log
from typing import Iterable

from .detection import OneSidedDetector


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _unit_interval_closed(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 < probability <= 1.0:
        raise ValueError(f"{name} must lie in (0, 1]")
    return probability


def _open_unit_interval(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 < probability < 1.0:
        raise ValueError(f"{name} must lie strictly between zero and one")
    return probability


@dataclass(frozen=True)
class ModeDiverseDetectionPanel:
    """Repeated one-sided reads distributed across independent failure modes.

    Every one of ``mode_count`` declared modes operates with probability at least
    ``availability_lower_bound`` independently of the other modes. A failed mode
    makes every assigned read negative. Conditional on an operating mode, each
    present coordinate receives ``repetitions_per_mode`` independent read attempts
    with the detector's declared sensitivity lower bound. False positives are
    excluded by the detector contract.

    The closed form is exact when both lower bounds are attained. With lower
    bounds it is a valid lower bound on the probability of detecting every truly
    present coordinate at least once.
    """

    coordinate_count: int
    mode_count: int
    repetitions_per_mode: int
    availability_lower_bound: float
    detector: OneSidedDetector

    def __post_init__(self) -> None:
        _positive_int("coordinate_count", self.coordinate_count)
        _positive_int("mode_count", self.mode_count)
        _nonnegative_int("repetitions_per_mode", self.repetitions_per_mode)
        object.__setattr__(
            self,
            "availability_lower_bound",
            _unit_interval_closed("availability_lower_bound", self.availability_lower_bound),
        )
        if not isinstance(self.detector, OneSidedDetector):
            raise ValueError("detector must be a OneSidedDetector")

    @property
    def total_reads(self) -> int:
        return self.coordinate_count * self.mode_count * self.repetitions_per_mode

    @property
    def within_mode_miss_probability_upper_bound(self) -> float:
        """Probability a present coordinate has no positive in one operating mode."""
        return (1.0 - self.detector.sensitivity_lower_bound) ** self.repetitions_per_mode

    @property
    def availability_ceiling(self) -> float:
        """Supremum obtainable by unlimited within-mode replication.

        If every mode fails, no coordinate can be detected. Hence even perfect
        within-mode sensing cannot exceed the probability that at least one
        independent mode operates.
        """
        return 1.0 - (1.0 - self.availability_lower_bound) ** self.mode_count

    @property
    def joint_detection_lower_bound(self) -> float:
        """Probability lower bound that all present coordinates are detected.

        Inclusion-exclusion is over the coordinates still missing at the end. For
        a specified set of ``s`` coordinates, one mode misses all of them with
        probability at most ``1-a + a*q**s``, where ``a`` is mode availability and
        ``q`` is the within-mode all-negative probability of one coordinate.
        """
        a = self.availability_lower_bound
        q = self.within_mode_miss_probability_upper_bound
        terms = [
            (-1.0) ** subset_size
            * comb(self.coordinate_count, subset_size)
            * (1.0 - a + a * q**subset_size) ** self.mode_count
            for subset_size in range(self.coordinate_count + 1)
        ]
        return min(1.0, max(0.0, fsum(terms)))

    @property
    def all_negative_probability_if_all_present_upper_bound(self) -> float:
        """Probability upper bound of a fully negative panel under all presence."""
        a = self.availability_lower_bound
        p = self.detector.sensitivity_lower_bound
        reads_in_mode = self.coordinate_count * self.repetitions_per_mode
        per_mode_negative = 1.0 - a + a * (1.0 - p) ** reads_in_mode
        return per_mode_negative**self.mode_count

    @property
    def all_negative_record_is_ambiguous(self) -> bool:
        """Whether a fully negative record remains possible when all coordinates exist."""
        return self.all_negative_probability_if_all_present_upper_bound > 0.0

    @classmethod
    def minimum_mode_count_for_availability_ceiling(
        cls, availability_lower_bound: float, confidence: float
    ) -> int:
        """Necessary number of independent modes for a target confidence.

        This only clears the common-mode availability ceiling. It is not
        sufficient: finite within-mode sensitivity can require still more modes or
        repeated reads within the selected modes.
        """
        availability = _unit_interval_closed(
            "availability_lower_bound", availability_lower_bound
        )
        confidence = _open_unit_interval("confidence", confidence)
        if availability == 1.0:
            return 1
        modes = max(1, ceil(log(1.0 - confidence) / log(1.0 - availability)))
        while 1.0 - (1.0 - availability) ** modes < confidence:
            modes += 1
        while modes > 1 and 1.0 - (1.0 - availability) ** (modes - 1) >= confidence:
            modes -= 1
        return modes

    def can_reach_joint_confidence(self, confidence: float) -> bool:
        """Whether some finite within-mode repetition count can reach confidence."""
        confidence = _open_unit_interval("confidence", confidence)
        if self.detector.sensitivity_lower_bound == 1.0:
            return confidence <= self.availability_ceiling
        return confidence < self.availability_ceiling

    def minimum_repetitions_for_joint_confidence(self, confidence: float) -> int:
        """Least nonzero within-mode repeat count meeting the joint target.

        The mode count and coordinate count are held fixed. If the target meets
        or exceeds the strict availability ceiling under imperfect sensitivity, no
        finite number of within-mode repeats can reach it.
        """
        confidence = _open_unit_interval("confidence", confidence)
        if not self.can_reach_joint_confidence(confidence):
            raise ValueError(
                "target confidence cannot be reached with this mode count because of the common-mode availability ceiling"
            )
        repeats = 1
        while ModeDiverseDetectionPanel(
            self.coordinate_count,
            self.mode_count,
            repeats,
            self.availability_lower_bound,
            self.detector,
        ).joint_detection_lower_bound < confidence:
            repeats *= 2
        lower, upper = 1, repeats
        while lower < upper:
            middle = (lower + upper) // 2
            candidate = ModeDiverseDetectionPanel(
                self.coordinate_count,
                self.mode_count,
                middle,
                self.availability_lower_bound,
                self.detector,
            )
            if candidate.joint_detection_lower_bound >= confidence:
                upper = middle
            else:
                lower = middle + 1
        return lower

    def positive_signature(
        self, observations: Iterable[Iterable[Iterable[bool]]]
    ) -> frozenset[int]:
        """Coordinates with at least one positive across all modes and repeats."""
        mode_rows = tuple(tuple(tuple(reads) for reads in mode) for mode in observations)
        if len(mode_rows) != self.mode_count:
            raise ValueError("observations must provide one block per mode")
        certified: set[int] = set()
        for mode in mode_rows:
            if len(mode) != self.coordinate_count:
                raise ValueError("each mode must provide one row per coordinate")
            for coordinate, reads in enumerate(mode):
                if len(reads) != self.repetitions_per_mode:
                    raise ValueError("each row must match repetitions_per_mode")
                if any(not isinstance(value, bool) for value in reads):
                    raise ValueError("observations must be bool")
                if any(reads):
                    certified.add(coordinate)
        return frozenset(certified)

    def verify(self) -> bool:
        return (
            self.total_reads
            == self.coordinate_count * self.mode_count * self.repetitions_per_mode
            and 0.0 <= self.joint_detection_lower_bound <= self.availability_ceiling <= 1.0
            and 0.0 <= self.all_negative_probability_if_all_present_upper_bound <= 1.0
        )
