# silence-jumpcut-planner

[![CI](https://github.com/tarikra1/silence-jumpcut-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/tarikra1/silence-jumpcut-planner/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/release-v1.0.0-0EA5E9.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Zero-dependency Python WAV speech-island detector and frame-snapped jump-cut planner with asymmetric `head_pad` / `tail_pad` protection so trailing syllables are never clipped.**

## Quickstart

```bash
pip install -e .
jumpcut-plan raw_voiceover.wav --threshold-db -38 --min-silence 0.15 --fps 30
```

## License

MIT License — see [LICENSE](LICENSE).
