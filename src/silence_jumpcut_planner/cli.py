"""CLI for silence-jumpcut-planner."""

from __future__ import annotations

import argparse
import json

from .core import analyze_wav_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="jumpcut-plan", description="Generate consonant-safe jump-cut speech islands from 16-bit WAV audio.")
    parser.add_argument("wav_path", help="Input 16-bit PCM .wav file")
    parser.add_argument("--threshold-db", type=float, default=-38.0)
    parser.add_argument("--min-silence", type=float, default=0.15)
    parser.add_argument("--fps", type=float, default=30.0)
    args = parser.parse_args(argv)

    islands = analyze_wav_file(
        args.wav_path,
        threshold_db=args.threshold_db,
        min_silence_sec=args.min_silence,
        fps=args.fps,
    )
    kept = round(sum(i.duration_sec for i in islands), 3)
    print(json.dumps({"count": len(islands), "kept_seconds": kept, "islands": [i.to_dict() for i in islands]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
