"""tsfm-quant: fine-tuned time-series foundation models for financial forecasting.

A 9+1 expert architecture: nine specialists (direction, return, risk,
microstructure, on-chain, regime, relative strength, factor bridge), each a
fine-tuned time-series foundation model behind one pluggable interface, with
Chronos-2 as the default backbone and a Z-Combiner fusing their outputs.
"""

__version__ = "0.1.0"
