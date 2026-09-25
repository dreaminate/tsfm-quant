"""Registry of the 9+1 expert architecture.

Nine specialists, one combiner.
"""

from __future__ import annotations

from tsfm_quant.experts.base import SUPPORTED_BACKBONES, BaseFMExpert

#: The nine specialist slots, in canonical order.
EXPERT_SLOTS: tuple[str, ...] = (
    "Alpha-Dir",
    "Alpha-Ret",
    "Risk-Prob",
    "Risk-Reg",
    "MicroStruct-Deriv",
    "OnChain-ETF",
    "Regime-Gate",
    "RelativeStrength-Spread",
    "Factor-Bridge",
)

#: The single fusion layer on top of the nine specialists.
COMBINER_SLOT = "Z-Combiner"

_REGISTRY: dict[str, type[BaseFMExpert]] = {}


def register(expert_cls: type[BaseFMExpert]) -> type[BaseFMExpert]:
    """Class decorator: add an expert implementation to the registry.

    Refuses slots that aren't part of the declared architecture and backbones
    that aren't supported, so drift is caught at import time, not mid-training.
    """
    if expert_cls.name not in EXPERT_SLOTS:
        raise ValueError(
            f"unknown expert slot {expert_cls.name!r}; declared slots are {EXPERT_SLOTS}"
        )
    if expert_cls.backbone not in SUPPORTED_BACKBONES:
        raise ValueError(
            f"expert {expert_cls.name!r} declares unsupported backbone "
            f"{expert_cls.backbone!r}; expected one of {SUPPORTED_BACKBONES}"
        )
    _REGISTRY[expert_cls.name] = expert_cls
    return expert_cls


def get(name: str) -> type[BaseFMExpert]:
    """Return the implementation registered for a slot."""
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"expert {name!r} has no implementation yet; "
            f"implemented: {implemented() or 'none so far'}"
        ) from None


def implemented() -> list[str]:
    """Slots that have a registered implementation, in canonical order."""
    return [slot for slot in EXPERT_SLOTS if slot in _REGISTRY]


def planned() -> list[str]:
    """Slots still waiting for an implementation, in canonical order."""
    return [slot for slot in EXPERT_SLOTS if slot not in _REGISTRY]
