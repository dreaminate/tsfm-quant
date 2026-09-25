"""Contract tests for the expert slot interface and the 9+1 registry."""

import pytest

from tsfm_quant.experts import (
    COMBINER_SLOT,
    EXPERT_SLOTS,
    SUPPORTED_BACKBONES,
    BaseFMExpert,
    ForecastRequest,
    implemented,
    planned,
    register,
)


class _Minimal(BaseFMExpert):
    name = "Risk-Prob"
    backbone = "chronos-2"

    def load(self) -> None: ...

    def predict(self, request):  # noqa: ANN001 - stub
        return None

    def finetune(self, train, val=None, **kwargs):  # noqa: ANN001 - stub
        return {}


def test_architecture_is_nine_experts_plus_one_combiner():
    assert len(EXPERT_SLOTS) == 9
    assert len(set(EXPERT_SLOTS)) == 9  # no duplicate slots
    assert COMBINER_SLOT == "Z-Combiner"
    assert COMBINER_SLOT not in EXPERT_SLOTS
    assert "chronos-2" in SUPPORTED_BACKBONES  # default backbone stays first-class


def test_backbone_must_be_supported():
    with pytest.raises(ValueError, match="unsupported backbone"):
        _Minimal(backbone="gpt-4")
    assert _Minimal(backbone="moirai-2").backbone == "moirai-2"


def test_forecast_request_defaults_are_independent():
    a = ForecastRequest(symbol="BTC/USDT", freq="1h", horizon=24)
    a.context["ohlcv"] = "frame"
    b = ForecastRequest(symbol="ETH/USDT", freq="1d", horizon=7)
    assert b.context == {}
    assert b.extras == {}


def test_register_rejects_unknown_slot():
    class Rogue(_Minimal):
        name = "Not-A-Slot"

    with pytest.raises(ValueError, match="unknown expert slot"):
        register(Rogue)


def test_register_rejects_unsupported_backbone():
    class BadBackbone(_Minimal):
        name = "Risk-Reg"
        backbone = "arima"

    with pytest.raises(ValueError, match="unsupported backbone"):
        register(BadBackbone)


def test_register_and_lookup():
    @register
    class RiskProbStub(_Minimal):
        name = "Risk-Prob"
        backbone = "chronos-2"

    assert "Risk-Prob" in implemented()
    assert "Risk-Prob" not in planned()
    from tsfm_quant.experts import get

    assert get("Risk-Prob") is RiskProbStub


def test_planned_is_the_complement_of_implemented():
    assert set(implemented()) | set(planned()) == set(EXPERT_SLOTS)
    assert not (set(implemented()) & set(planned()))
