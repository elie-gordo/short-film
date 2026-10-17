"""Procedural sound design for the TENSION teaser (30 s, no third-party audio).

Usage: python script/sound.py edit/public/sfx.wav --sfx-only   (effects only, used with the music)
       python script/sound.py edit/public/sound.wav              (effects + synthetic drone, no music)
Cue times are in seconds on the master timeline (30 fps, see blender/film.py SHOTS).
"""
import sys
import wave

import numpy as np

SR = 48000
DURATION = 31.5
LIMITER_DRIVE = 2.5
rng = np.random.default_rng(7)
t = np.arange(int(SR * DURATION)) / SR


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def env(start, attack, hold, release):
    e = np.zeros_like(t)
    a0, a1 = start, start + attack
    h1 = a1 + hold
    r1 = h1 + release
    m = (t >= a0) & (t < a1)
    e[m] = (t[m] - a0) / attack
    e[(t >= a1) & (t < h1)] = 1.0
    m = (t >= h1) & (t < r1)
    e[m] = 1 - (t[m] - h1) / release
    return e


def drone():
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
    x = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t)
         + 0.25 * np.sin(2 * np.pi * 110.3 * t)) * lfo
    swell = env(0.0, 3.0, 20.0, 7.0) * 0.12 + env(23.5, 1.5, 3.5, 1.5) * 0.08
    return x * swell


def creak(start, length, pitch, gain):
    """Stick-slip spring creak: resonant noise gated by an irregular pulse train."""
    n = int(length * SR)
    i0 = int(start * SR)
    noise = rng.standard_normal(n)
    rate = pitch * (1 + 0.3 * np.sin(np.linspace(0, 3 * np.pi, n)))
    phase = np.cumsum(rate / SR)
    gate = (np.sin(2 * np.pi * phase) > 0.6).astype(float)
    tone = np.sin(2 * np.pi * np.cumsum((900 + 300 * np.sin(np.linspace(0, 2 * np.pi, n))) / SR))
    x = (0.4 * noise + tone) * gate
    shape = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    out = np.zeros_like(t)
    out[i0:i0 + n] = lowpass(x * shape, 2500) * gain
    return out


def click(start, gain, freq=2200):
    n = int(0.06 * SR)
    i0 = int(start * SR)
    k = np.arange(n) / SR
    x = (rng.standard_normal(n) * 0.6 + np.sin(2 * np.pi * freq * k)) * np.exp(-k * 90)
    out = np.zeros_like(t)
    out[i0:i0 + n] = x * gain
    return out


def clank(start, gain):
    n = int(0.5 * SR)
    i0 = int(start * SR)
    k = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * k) * np.exp(-k * d) for f, d in ((420, 9), (1130, 14), (2710, 22)))
    out = np.zeros_like(t)
    out[i0:i0 + n] = x * gain
    return out


def hum(start, end):
    on = env(start, 0.05, end - start - 1.2, 1.2)
    x = (np.sin(2 * np.pi * 100 * t) + 0.35 * np.sin(2 * np.pi * 200 * t)
         + 0.15 * np.sin(2 * np.pi * 300 * t))
    return x * on * 0.05


def flicker(start, gain):
    return click(start, gain, 3200) + hum(start, start + 0.12) * 1.5


def build(with_drone):
    # Without the drone (music takes its place) the effects keep their natural dynamics.
    mix = drone() if with_drone else np.zeros_like(t)
    mix += creak(2.0, 2.2, 38, 0.10)    # P02 spring macro
    mix += click(4.6, 0.12, 1500)       # P03 cap tick
    mix += creak(10.5, 3.2, 26, 0.22)   # P05 lower arm lifts
    mix += creak(14.2, 1.4, 44, 0.16)   # P06 elbow
    mix += creak(16.2, 1.0, 52, 0.14)   # P07 head tips
    mix += clank(17.3, 0.10)            # P07 settle
    mix += creak(18.3, 0.8, 60, 0.08)   # P08 damped bounce
    mix += clank(18.9, 0.05)
    mix += click(22.8, 0.45)            # P09 button
    mix += flicker(24.2, 0.25)          # P10 flicker x2
    mix += flicker(24.55, 0.25)
    mix += click(24.95, 0.30, 2800)
    mix += hum(24.95, 30.8)             # bulb on through the end card
    fade = np.clip((DURATION - t) / 1.5, 0, 1)
    mix *= fade
    mix /= np.max(np.abs(mix))
    if with_drone:
        mix = np.tanh(mix * LIMITER_DRIVE)  # soft limiter: lifts RMS toward web loudness
    mix /= np.max(np.abs(mix)) / 0.79   # about -2 dBFS peak (AAC overshoots)
    left = mix
    right = np.roll(mix, int(0.0004 * SR))  # slight width
    return np.stack([left, right], axis=1)


def main(path, with_drone):
    data = (build(with_drone) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    print(f"wrote {path}")


if __name__ == "__main__":
    main(sys.argv[1], with_drone="--sfx-only" not in sys.argv)
