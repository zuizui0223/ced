"""Delayed addressability and finite-evidence limits.

This standalone core rescues CCOC legacy ID-1.  It separates two quantities:
(1) exact open-interface memory for independently addressable exterior bits, and
(2) the first legal horizon at which those bits can affect observations.

The theorem is conditional on a declared finite prefix grammar.  It does not
infer a delay mechanism or ecological boundary from data.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DelayedExposureFamily:
    """Binary exterior family with ``m`` ports and a delay of ``H`` steps.

    Before ``wait**H fire`` becomes legal, every legal trace observes only the
    focal bit.  A structural context selects one exterior port; firing after the
    delay exposes that port.  Port choice is not an action symbol.
    """

    module_count: int
    delay: int

    def __post_init__(self) -> None:
        if not isinstance(self.module_count, int) or isinstance(self.module_count, bool) or self.module_count < 1:
            raise ValueError("module_count must be a positive integer")
        if not isinstance(self.delay, int) or isinstance(self.delay, bool) or self.delay < 0:
            raise ValueError("delay must be a nonnegative integer")

    @property
    def revealing_horizon(self) -> int:
        return self.delay + 1

    @property
    def closed_interface_bits(self) -> int:
        """One fixed port needs focal plus that port's binary value."""
        return 2

    @property
    def open_interface_bits(self) -> int:
        """All ports may later be structurally attached and separately read."""
        return self.module_count + 1

    @property
    def open_state_count(self) -> int:
        return 1 << self.open_interface_bits

    @property
    def closed_state_count(self) -> int:
        return 1 << self.closed_interface_bits

    def legal_words_through(self, horizon: int) -> tuple[tuple[str, ...], ...]:
        if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon < 0:
            raise ValueError("horizon must be a nonnegative integer")
        words = [()]
        for length in range(1, min(horizon, self.delay) + 1):
            words.append(("wait",) * length)
        if horizon >= self.revealing_horizon:
            words.append(("wait",) * self.delay + ("fire",))
        return tuple(words)

    def is_exterior_blind_through(self, horizon: int) -> bool:
        """Whether no legal word can yet expose a selected exterior bit."""
        return horizon < self.revealing_horizon

    def verify(self) -> bool:
        return (
            self.closed_interface_bits == 2
            and self.open_interface_bits == self.module_count + 1
            and self.is_exterior_blind_through(self.delay)
            and not self.is_exterior_blind_through(self.revealing_horizon)
            and ("wait",) * self.delay + ("fire",) in self.legal_words_through(self.revealing_horizon)
        )


def no_uniform_closure_horizon(proposed_horizon: int) -> DelayedExposureFamily:
    """Return a legal delayed family that defeats a proposed uniform horizon.

    The returned family agrees with a closed comparator on every legal trace
    through ``proposed_horizon`` but differs at the next legal revealing word.
    """
    if not isinstance(proposed_horizon, int) or isinstance(proposed_horizon, bool) or proposed_horizon < 0:
        raise ValueError("proposed_horizon must be a nonnegative integer")
    family = DelayedExposureFamily(module_count=1, delay=proposed_horizon)
    if not family.verify() or not family.is_exterior_blind_through(proposed_horizon):
        raise AssertionError("delayed no-go witness failed verification")
    return family
