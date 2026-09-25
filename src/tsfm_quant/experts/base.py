"""Pluggable foundation-model expert slot interface.

Every expert in the 9+1 architecture talks to the rest of the system through
this interface, so backbones stay swappable: Chronos-2 is the default,
Moirai-2 is a second slot, and TFT is available as a third backbone.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

#: The only backbones an expert may declare. Keeping this closed is what makes
#: the slot list the single source of truth for what the system depends on.
SUPPORTED_BACKBONES: tuple[str, ...] = ("chronos-2", "moirai-2", "tft-legacy")


@dataclass(frozen=True)
class ForecastRequest:
    """One expert's view of a prediction task.

    context: aligned history keyed by modality (ohlcv, derivatives, on-chain,
    ...) — concrete frame type is fixed when the data layer lands in M1.
    """

    symbol: str
    freq: str  # "1h" | "4h" | "1d"
    horizon: int
    context: dict[str, Any] = field(default_factory=dict)
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ForecastResult:
    """Expert output handed to the Z-Combiner."""

    symbol: str
    freq: str
    horizon: int
    predictions: Any  # backbone-specific tensor/array; normalized by the combiner
    meta: dict[str, Any] = field(default_factory=dict)


class BaseFMExpert(ABC):
    """Contract for a foundation-model expert.

    Subclasses declare ``name`` (one of the nine slots in
    ``tsfm_quant.experts.registry.EXPERT_SLOTS``) and ``backbone`` (one of
    ``SUPPORTED_BACKBONES``); the registry enforces both at registration.
    """

    name: str = "base"
    backbone: str = "chronos-2"

    def __init__(self, backbone: str | None = None) -> None:
        if backbone is not None:
            if backbone not in SUPPORTED_BACKBONES:
                raise ValueError(
                    f"unsupported backbone {backbone!r}; expected one of {SUPPORTED_BACKBONES}"
                )
            self.backbone = backbone

    @abstractmethod
    def load(self) -> None:
        """Load backbone weights (base or fine-tuned checkpoint)."""

    @abstractmethod
    def predict(self, request: ForecastRequest) -> ForecastResult:
        """Zero-shot or fine-tuned forecast for one request."""

    @abstractmethod
    def finetune(self, train: Any, val: Any | None = None, **kwargs: Any) -> dict[str, Any]:
        """Fine-tune the backbone; returns a metrics dict."""
