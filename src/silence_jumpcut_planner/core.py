"""Pure-Python PCM WAV speech-island detector and frame-snapped jump-cut planner."""

from __future__ import annotations

import math
import struct
import wave
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpeechIsland:
    start_sec: float
    end_sec: float

    @property
    def duration_sec(self) -> float:
        return round(self.end_sec - self.start_sec, 4)

    def to_dict(self) -> dict[str, float]:
        d = asdict(self)
        d["duration_sec"] = self.duration_sec
        return d


def snap_to_frame(seconds: float, fps: float = 30.0) -> float:
    return round(round(seconds * fps) / fps, 4)


def detect_islands_from_rms(
    rms_db_windows: list[float],
    window_sec: float = 0.01,
    threshold_db: float = -38.0,
    min_silence_sec: float = 0.15,
    head_pad_sec: float = 0.045,
    tail_pad_sec: float = 0.135,
    fps: float = 30.0,
) -> list[SpeechIsland]:
    total_dur = len(rms_db_windows) * window_sec
    raw_spans: list[list[float]] = []
    in_speech = False
    start = 0.0

    for i, db in enumerate(rms_db_windows):
        t = i * window_sec
        if db >= threshold_db and not in_speech:
            in_speech = True
            start = t
        elif db < threshold_db and in_speech:
            in_speech = False
            raw_spans.append([start, t])
    if in_speech:
        raw_spans.append([start, total_dur])

    if not raw_spans:
        return []

    # Merge spans separated by less than min_silence_sec
    merged: list[list[float]] = [raw_spans[0]]
    for sp in raw_spans[1:]:
        if sp[0] - merged[-1][1] < min_silence_sec:
            merged[-1][1] = sp[1]
        else:
            merged.append(sp)

    # Apply asymmetric head/tail padding & merge any resulting overlaps
    padded: list[list[float]] = []
    for s, e in merged:
        ps = snap_to_frame(max(0.0, s - head_pad_sec), fps)
        pe = snap_to_frame(min(total_dur, e + tail_pad_sec), fps)
        if padded and ps <= padded[-1][1]:
            padded[-1][1] = max(padded[-1][1], pe)
        else:
            padded.append([ps, pe])

    return [SpeechIsland(s, e) for s, e in padded if e > s]


def analyze_wav_file(wav_path: str | Path, window_sec: float = 0.01, **kwargs) -> list[SpeechIsland]:
    with wave.open(str(wav_path), "rb") as wf:
        if wf.getsampwidth() != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported.")
        rate = wf.getframerate()
        channels = wf.getnchannels()
        frames_per_win = max(1, int(rate * window_sec))
        rms_db: list[float] = []
        while True:
            raw = wf.readframes(frames_per_win)
            if not raw:
                break
            count = len(raw) // 2
            samples = struct.unpack(f"<{count}h", raw)
            if channels > 1:
                samples = samples[::channels]
            mean_sq = sum(s * s for s in samples) / max(1, len(samples))
            rms = math.sqrt(mean_sq) / 32768.0
            db = 20.0 * math.log10(max(rms, 1e-7))
            rms_db.append(db)
    return detect_islands_from_rms(rms_db, window_sec=window_sec, **kwargs)
