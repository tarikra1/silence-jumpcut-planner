# Changelog

All notable changes to `silence-jumpcut-planner` are documented in this file.

## [1.0.0] - 2026-11-25

### Added
- Pure-Python 16-bit PCM RMS envelope analyzer and speech-island detector (`detect_islands_from_rms`).
- Asymmetric `head_pad` (`0.045s`) and `tail_pad` (`0.135s`) protection so trailing consonants and vowels are never clipped.
- Frame-snapped cut range quantizer (`24`, `25`, `30`, `60` fps), CLI (`jumpcut-plan`), and GitHub Actions CI matrix.
