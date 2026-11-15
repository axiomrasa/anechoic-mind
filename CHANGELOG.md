# Changelog — Anechoic Mind

All notable changes to this project will be documented in this file.
Format adheres to Semantic Versioning (SemVer).

## [0.1.0] - 2026-11-15 (Initial MVP Beta)
### Added
- **Universal Binary Build:** Native support for both Apple Silicon (arm64) and Intel (x86_64) macOS architectures across VST3, AU, and Standalone formats.
- **Focus-to-Fringe Attenuation:** Non-linear cubic lowpass filter (16kHz down to 150Hz) linked to Isolation Depth.
- **Cranial Bone-Conduction Engine:** Fractional delay feedback comb filter (2ms - 7ms) simulating internal skull resonance.
- **Anechoic Bodily Interior:** Procedural pink-noise resonant bloodstream generator (65Hz LFO-modulated) and nervous system micro-detuned sine oscillator (3840Hz).
- **Spatial Collapse & Protection:** Automatic stereo-to-mono convergence and tanh soft-clipping output limiter.
