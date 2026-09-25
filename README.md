<div align="center">

# tsfm-quant

**Fine-tuned time-series foundation models for multi-task crypto & financial forecasting**

Open weights · Honest backtests · Pluggable backbones

[![CI](https://github.com/dreaminate/tsfm-quant/actions/workflows/ci.yml/badge.svg)](https://github.com/dreaminate/tsfm-quant/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![GitHub stars](https://img.shields.io/github/stars/dreaminate/tsfm-quant?style=social)](https://github.com/dreaminate/tsfm-quant)

*Phase 0 — scaffolding. First Chronos-2 fine-tune lands with Milestone 1.
Built in public; progress is posted on X as each milestone ships.*

</div>

---

## Why

Crypto markets are noisy, multi-scale, and regime-driven — exactly where a
single monolithic model fails. tsfm-quant decomposes the problem instead:
**nine specialist experts, each a fine-tuned time-series foundation model,
fused by a learned combiner.**

The bet, stated plainly: fine-tuned TSFMs beat both their zero-shot selves
and task-specific deep models on financial targets — a result now repeatedly
documented (e.g. multi-scale fine-tuning work at NeurIPS). This repo tests
that bet in public, with open weights and honest backtests.

## Architecture

```
 market / derivatives / on-chain data
        │   fetch · features · no-leakage guards            (M1)
        ▼
 ┌────────────────────────────────────────────────────────────────┐
 │  9 specialists — each a fine-tuned FM behind BaseFMExpert      │
 │  Alpha-Dir                 direction                           │
 │  Alpha-Ret                 return magnitude                    │
 │  Risk-Prob                 tail-risk probability               │
 │  Risk-Reg                  risk regression                     │
 │  MicroStruct-Deriv         derivatives microstructure          │
 │  OnChain-ETF               on-chain + ETF flows                │
 │  Regime-Gate               market-state gating                 │
 │  RelativeStrength-Spread   cross-asset relative strength       │
 │  Factor-Bridge             factor exposure bridging            │
 └───────────────────────────┬────────────────────────────────────┘
                             ▼
                      Z-Combiner ──► fused forecasts
```

Every expert implements `BaseFMExpert` — `load()` / `finetune()` / `predict()` —
and declares its backbone. The registry only accepts the nine declared slots
and three supported backbones (`chronos-2`, `moirai-2`, `tft-legacy`), so
architecture drift fails at import time, not mid-training.

<!-- TODO(M1): replace this diagram with a rendered image + a demo GIF of the
     first fine-tuned Alpha-Dir forecast. -->

## Roadmap

| Milestone | Delivers                                                                        | Status        |
| --------- | ------------------------------------------------------------------------------- | ------------- |
| M1        | Data pipelines; Chronos-2 zero-shot baseline; first fine-tuned expert (Alpha-Dir); demo GIF | in progress |
| M2        | All 9 experts on FM slots; Z-Combiner; benchmark table: zero-shot vs fine-tuned vs TFT expert |              |
| M3        | Open fine-tuned checkpoints (HF Hub); honest backtest report                     |               |

Details live in [ROADMAP.md](ROADMAP.md).

## Quickstart

Requires Python 3.10+.

```bash
git clone https://github.com/dreaminate/tsfm-quant.git
cd tsfm-quant
pip install -e ".[dev]"
```

Sanity-check the skeleton (a PyPI release ships with M2):

```bash
python -c "from tsfm_quant.experts import EXPERT_SLOTS, planned; print(planned())"
pytest -q
```

## Honest-backtest pledge

Every backtest this project publishes will be:

- **net of fees and slippage** — never gross returns dressed up as tradable;
- **walk-forward** — time-ordered splits, no shuffling across the boundary;
- **leakage-guarded** — no-leakage split rules enforced by unit tests, not by
  convention;
- **published whole** — losing periods appear next to winning ones. If a
  release's numbers survive only on a cherry-picked window, that's a bug
  report, not a benchmark.

## Project layout

```
src/tsfm_quant/
├── experts/     BaseFMExpert interface + 9+1 registry   (this is the contract)
├── data/        fetch / features / no-leakage guards    (lands in M1)
└── ...
tests/           contract tests for the interface and registry
```

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are
marked `good first issue`; a stub expert for an unimplemented slot or a
data-fetch adapter for one exchange are both self-contained starts.

## License

[Apache-2.0](LICENSE) — same as the Chronos-2 backbone this project
fine-tunes.

## Credits

- [Chronos](https://github.com/amazon-science/chronos-forecasting) — the
  default backbone.
