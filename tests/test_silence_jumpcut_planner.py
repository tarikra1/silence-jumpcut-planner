import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import math
import struct
import tempfile
import unittest
import wave

from silence_jumpcut_planner.core import analyze_wav_file, detect_islands_from_rms


class TestSilenceJumpcutPlanner(unittest.TestCase):
    def test_detect_islands_merges_short_breaths_and_splits_pauses(self) -> None:
        windows = [-18.0] * 50 + [-60.0] * 40 + [-18.0] * 50
        islands = detect_islands_from_rms(windows, window_sec=0.01, min_silence_sec=0.20, fps=30.0)
        self.assertEqual(len(islands), 2)
        self.assertGreater(islands[0].end_sec, 0.5)

    def test_analyze_synthetic_wav(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wav_p = Path(tmp) / "voice.wav"
            rate = 16000
            with wave.open(str(wav_p), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(rate)
                tone = [int(12000 * math.sin(2 * math.pi * 220 * i / rate)) for i in range(rate // 2)]
                silence = [0] * (rate // 2)
                samples = tone + silence + tone
                wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))

            islands = analyze_wav_file(wav_p, min_silence_sec=0.25)
            self.assertEqual(len(islands), 2)


if __name__ == "__main__":
    unittest.main()
