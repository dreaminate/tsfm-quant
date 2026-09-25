# Roadmap

Build in public: each milestone ships, gets a post on X, and only then does
the next one start. Scope below is the agreed plan; dates are deliberately
absent — quality gates, not calendar, drive releases.

## M1 — core engine, first publishable result

- [ ] Market-data collection (OHLCV, derivatives, on-chain) in
      `tsfm_quant.data.fetch`
- [ ] Feature engineering and no-leakage walk-forward guards, with unit
      tests on the guards themselves
- [ ] `Chronos2Expert` implementing `BaseFMExpert` (zero-shot first)
- [ ] Zero-shot baseline on Alpha-Dir's target, evaluated with directional
      and calibration metrics
- [ ] First fine-tune of Alpha-Dir (Chronos-2); compare against zero-shot
- [ ] Demo GIF + README update + launch post on X

**Exit criterion:** one command reproduces fetch → features → zero-shot →
fine-tuned forecast for Alpha-Dir on BTC/USDT 1h.

## M2 — the full 9+1 system

- [ ] Implement the remaining 8 experts on `BaseFMExpert` slots
- [ ] TFT expert on the `tft-legacy` backbone as a third option
- [ ] Z-Combiner; end-to-end fused forecast
- [ ] Benchmark table on a fixed dataset + split: Chronos-2 zero-shot vs
      fine-tuned vs TFT expert, same metrics everywhere
- [ ] PyPI release `0.2.0` + Show HN post

**Exit criterion:** the benchmark table is reproducible from a clean clone
with `make benchmark`.

## M3 — open weights, honest backtest

- [ ] Publish fine-tuned checkpoints to Hugging Face Hub
- [ ] Loader that resolves checkpoints by expert + backbone + version
- [ ] Full backtest report honoring the honest-backtest pledge (fees,
      slippage, walk-forward, losing periods included)
- [ ] r/algotrading post + blog write-up

**Exit criterion:** `tsfm-quant predict --expert alpha-dir` downloads weights
and emits a forecast without any local training.

## Non-goals

- Live-trading execution: order placement, position sizing, and exchange keys
  never enter this repository.
- Chasing every new TSFM release: backbones are added when they earn a slot
  on the benchmark, not on release day.
