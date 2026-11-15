# ANECHOIC MIND (v0.1.0 - Beta Test Build)
**Phenomenological Isolation & Inner Speech Processor**  
*Developed by Axiom Rasa — [axiomrasa.xyz](https://axiomrasa.xyz)*

---

## 1. Overview
**Anechoic Mind** is a real-time stereo insert effect (VST3 / AU / Standalone) designed for cinema post-production, animation, and game audio. Inspired by Don Ihde's *Listening and Voice: Phenomenologies of Sound*, it simulates the perceptual transition of a character dissociating, entering shock, or retreating from the external auditory field (*Fringe*) into an isolated internal cranial space (*Focus*).

Instead of automating 4 different plugins (Lowpass EQ, Comb Filter, Stereo Imager, and Sub-Synth) across 15 automation lanes, **Anechoic Mind** collapses the entire acoustic transition into a single macro: **Isolation Depth**.

---

## 2. Macro Parameters
| Parameter | Range | Description |
| :--- | :--- | :--- |
| **[0] Isolation Depth** | `0.0% - 100%` | **Master Macro.** Simultaneously muffles the outer world, engages cranial bone-conduction, narrows stereo width to mono, and brings up internal physiological noise. |
| **[1] Cranial Resonance** | `0.10 - 0.95` | Controls the feedback and delay time (2ms–7ms) of the internal skull cavity comb resonator. |
| **[2] Internal Body Noise** | `0.00 - 1.00` | Controls the intensity of the procedural bloodstream throb (65–80 Hz) and nervous system high-frequency whine (~3.84 kHz). |
| **[3] Dry/Wet Mix** | `0.0% - 100%` | Blends the unprocessed input signal with the processed isolation engine. |
| **[4] Output Gain** | `-60dB to +12dB` | Master output level feeding into a non-linear `tanh` soft-clipping protection limiter. |

---

## 3. Cross-Platform Installation Guide

### A) macOS (Universal: Apple Silicon M1–M4 & Intel | macOS 10.15+)
1. **Copy Files:**
   * **VST3:** Copy `Anechoic Mind.vst3` to `/Library/Audio/Plug-Ins/VST3/`
   * **AU (Logic Pro / Ableton):** Copy `Anechoic Mind.component` to `/Library/Audio/Plug-Ins/Components/`
   * **Standalone:** Run `Anechoic Mind.app` directly without a DAW.
2. **Unlock Gatekeeper (Run once in Terminal):**
   `xattr -cr "/Library/Audio/Plug-Ins/VST3/Anechoic Mind.vst3" "/Library/Audio/Plug-Ins/Components/Anechoic Mind.component" ~/Library/Audio/Plug-Ins/VST3/"Anechoic Mind.vst3" ~/Library/Audio/Plug-Ins/Components/"Anechoic Mind.component" 2>/dev/null`

### B) Windows (Windows 10 & Windows 11 - 64-bit)
1. **VST3:** Copy `Anechoic Mind.vst3` into `C:\Program Files\Common Files\VST3\`
2. **Standalone:** Run `Anechoic Mind.exe` directly for DAW-less testing.

### C) Linux (Ubuntu / Debian / Arch - x86_64)
1. **VST3:** Copy `Anechoic Mind.vst3` into `~/.vst3/` or `/usr/lib/vst3/`
