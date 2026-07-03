"""Exact partial identification for delayed reset panels.

A fresh resettable trial can expose one declared exterior coordinate only after
the delay gate.  The resulting signature is an exact partial quotient: it
records the focal baseline, each covered exterior coordinate, and an optional
response-type coordinate exposed by an intervention probe.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Iterable


@dataclass(frozen=True)
class PanelCoverage:
    """Canonical coverage of delayed terminal probes.

    ``read_ports`` is the set of exterior bits observed by terminal reads.
    ``intervention`` records whether the response-type bit is identified.
    Duplicate or wait-only trials contribute no additional coverage.
    """

    module_count: int
    read_ports: frozenset[int]
    intervention: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.module_count, int) or isinstance(self.module_count, bool) or self.module_count < 1:
            raise ValueError("module_count must be a positive integer")
        if not isinstance(self.read_ports, frozenset):
            raise ValueError("read_ports must be a frozenset")
        if any(not isinstance(port, int) or isinstance(port, bool) or not 0 <= port < self.module_count for port in self.read_ports):
            raise ValueError("read_ports contains an invalid exterior port")
        if not isinstance(self.intervention, bool):
            raise ValueError("intervention must be bool")

    @classmethod
    def from_trials(cls, module_count: int, trials: Iterable[str]) -> "PanelCoverage":
        ports: set[int] = set()
        intervention = False
        for trial in trials:
            if trial == "intervene":
                intervention = True
            elif isinstance(trial, str) and trial.startswith("read:"):
                try:
                    ports.add(int(trial.split(":", 1)[1]))
                except ValueError as error:
                    raise ValueError(f"invalid read trial {trial!r}") from error
            elif trial != "wait":
                raise ValueError(f"unknown trial {trial!r}")
        return cls(module_count, frozenset(ports), intervention)

    @property
    def retained_bits(self) -> int:
        """Focal baseline plus distinct covered coordinates."""
        return 1 + len(self.read_ports) + int(self.intervention)

    @property
    def residual_bits(self) -> int:
        """Unidentified exterior and response-type coordinates."""
        return self.module_count + 1 - len(self.read_ports) - int(self.intervention)

    @property
    def quotient_state_count(self) -> int:
        return 1 << self.retained_bits

    @property
    def residual_class_size(self) -> int:
        return 1 << self.residual_bits

    @property
    def is_exact(self) -> bool:
        return len(self.read_ports) == self.module_count and self.intervention

    def add_trial(self, trial: str) -> "PanelCoverage":
        return PanelCoverage.from_trials(self.module_count, self.to_trials() + (trial,))

    def to_trials(self) -> tuple[str, ...]:
        reads = tuple(f"read:{port}" for port in sorted(self.read_ports))
        return reads + (("intervene",) if self.intervention else ())

    def verify(self) -> bool:
        return self.quotient_state_count * self.residual_class_size == 1 << (self.module_count + 2)


def panel_budget_frontier(module_count: int, trial_budget: int, delay: int | None = None, action_budget: int | None = None) -> int:
    """Maximum retained bits under a fresh-trial or total-action budget.

    Without ``action_budget``, every trial can cover one previously uncovered
    terminal probe.  With it, each information-bearing trial costs ``delay+1``
    actions.  The focal baseline is always retained.
    """
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")
    if not isinstance(trial_budget, int) or isinstance(trial_budget, bool) or trial_budget < 0:
        raise ValueError("trial_budget must be a nonnegative integer")
    usable = trial_budget
    if action_budget is not None:
        if not isinstance(delay, int) or isinstance(delay, bool) or delay < 0:
            raise ValueError("delay must be a nonnegative integer when action_budget is supplied")
        if not isinstance(action_budget, int) or isinstance(action_budget, bool) or action_budget < 0:
            raise ValueError("action_budget must be a nonnegative integer")
        usable = min(usable, floor(action_budget / (delay + 1)))
    return 1 + min(usable, module_count + 1)
