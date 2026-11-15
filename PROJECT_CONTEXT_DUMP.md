# AXIOM RASA — PROJECT CONTEXT SNAPSHOT
**Current Working Directory:** `/Users/axiomrasa/dev/audio-dsp/AxiomRasa_Workspace/01_Active_Products/anechoic-mind`

## 1. Environment & Toolchain Status
```text
macOS Version : 15.7.1 (arm64)
Faust Version : FAUST Version 2.88.0
CMake Version : cmake version 4.5.0
Ninja Version : 1.13.2
JUCE Git Head : 51d11a2be6 JUCE version 8.0.4
Git Status    : ?? .github/
?? .gitignore
?? CHANGELOG.md
?? CMakeLists.txt
?? LICENSE.txt
?? README.md
?? dsp/
?? scripts/
?? src_cpp/
Installed VST3: x86_64 arm64
```

## 2. Workspace Directory Tree (`~/dev/audio-dsp/AxiomRasa_Workspace`)
```text
AxiomRasa_Workspace/
  00_Master_Axiom_Shell/
    Releases/
      AnechoicMind/
        AnechoicMind_v0.1.0_macOS_Universal.zip
        AnechoicMind_v0.1.0_macOS/
          CHANGELOG.md
          LICENSE.txt
          README.md
  01_Active_Products/
    anechoic-mind/
      .gitignore
      CHANGELOG.md
      CMakeLists.txt
      LICENSE.txt
      README.md
      .github/
        workflows/
          cross_platform_build.yml
      dsp/
        anechoic_mind.dsp
        anechoic_mind/
          FaustPluginProcessor.cpp
          anechoic_mind.jucer
      juce_project/
      scripts/
        dump_context.py
        ship_it.py
      src_cpp/
        anechoic_mind.cpp
  02_Torture_Track_DAW/
```

## 3. Core Project Files Content
### File: `CMakeLists.txt`
```txt
cmake_minimum_required(VERSION 3.22)

if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15" CACHE STRING "Minimum macOS deployment version" FORCE)
    set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "Build architectures for macOS" FORCE)
endif()

project(AnechoicMind VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(/Users/axiomrasa/dev/third-party/JUCE ${CMAKE_BINARY_DIR}/JUCE)

juce_add_plugin(AnechoicMind
    COMPANY_NAME "Axiom Rasa"
    BUNDLE_ID "com.axiomrasa.anechoicmind"
    PLUGIN_MANUFACTURER_CODE AxRs
    PLUGIN_CODE AnMn
    FORMATS VST3 AU Standalone
    PRODUCT_NAME "Anechoic Mind"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
)

juce_generate_juce_header(AnechoicMind)

target_sources(AnechoicMind PRIVATE
    dsp/anechoic_mind/FaustPluginProcessor.cpp
)

target_include_directories(AnechoicMind PRIVATE
    ${CMAKE_BINARY_DIR}/AnechoicMind_artefacts
)

target_compile_definitions(AnechoicMind PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    PlugIn=1
)

target_link_libraries(AnechoicMind PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_gui_extra
    juce::juce_opengl
    PUBLIC
    juce::juce_recommended_config_flags
)
```

### File: `dsp/anechoic_mind.dsp`
```dsp
declare name        "Anechoic Mind";
declare version     "0.1.0";
declare author      "Axiom Rasa";
declare license     "Proprietary - Axiom Rasa";
declare description "Phenomenological Isolation and Inner Speech Processor";

import("stdfaust.lib");

// --- Master Axiom Shell & Macro GUI Parameters ---
isolation   = hslider("[0] Isolation Depth [unit:%]", 0.0, 0.0, 1.0, 0.001) : si.smoo;
cranial_res = hslider("[1] Cranial Resonance", 0.5, 0.1, 0.95, 0.001) : si.smoo;
body_level  = hslider("[2] Internal Body Noise", 0.4, 0.0, 1.0, 0.001) : si.smoo;
dry_wet     = hslider("[3] Dry/Wet Mix [unit:%]", 1.0, 0.0, 1.0, 0.001) : si.smoo;
master_gain = hslider("[4] Output Gain [unit:dB]", 0.0, -60.0, 12.0, 0.1) : ba.db2linear : si.smoo;

// --- 1. Outer World Attenuation (Focus to Fringe) ---
outer_cutoff = 150.0 + (16000.0 - 150.0) * pow(1.0 - isolation, 3.0);
outer_gain   = 1.0 - (isolation * 0.8);

muffle(x) = x : fi.lowpass(2, outer_cutoff);

// --- 2. Bone Conduction & Cranial Comb Filter ---
comb_del_sec  = 0.002 + (1.0 - cranial_res) * 0.005;
comb_samples  = max(1.0, comb_del_sec * ma.SR);

cranial_space(x) = x : (+ ~ (de.fdelay(4096, comb_samples) : fi.lowpass(1, 1500.0) : *(cranial_res * 0.85)));

process_channel(x) = (muffle(x) * (1.0 - isolation) + (muffle(x) : cranial_space) * isolation) * outer_gain;

// --- 3. Anechoic Bodily Interior (Bloodstream & Nervous System) ---
body_curve  = pow(isolation, 2.0) * body_level;
pulse_lfo   = os.osc(1.1) * 0.5 + 0.5;
blood_flow  = no.pink_noise : fi.resonbp(65.0 + pulse_lfo * 15.0, 3.0, 1.0) * (body_curve * 0.4);
nerve_whine = os.osc(3840.0 + no.lfnoise(2.0) * 8.0) * (body_curve * 0.012);

internal_noise = blood_flow + nerve_whine;

// --- 4. Spatial Collapse & Axiom Shell Output ---
width = 1.0 - isolation;

engine(l, r) = out_l, out_r
with {
    proc_l = process_channel(l);
    proc_r = process_channel(r);
    mono   = (proc_l + proc_r) * 0.5;
    
    // Stereo field narrows toward center of head as isolation increases
    collapsed_l = proc_l * width + mono * (1.0 - width);
    collapsed_r = proc_r * width + mono * (1.0 - width);
    
    wet_l = collapsed_l + internal_noise;
    wet_r = collapsed_r + internal_noise;
    
    // Master Axiom Shell: Dry/Wet Blend & Speaker Protection Limiter
    mix_l = l * (1.0 - dry_wet) + wet_l * dry_wet;
    mix_r = r * (1.0 - dry_wet) + wet_r * dry_wet;
    
    out_l = mix_l * master_gain : ma.tanh;
    out_r = mix_r * master_gain : ma.tanh;
};

process(l, r) = engine(l, r);
```

### File: `scripts/ship_it.py`
```py
import os
import zipfile

PLUGIN_NAME = "AnechoicMind"
VERSION = "v0.1.0"

ARTEFACTS_DIR = os.path.expanduser("~/dev/audio-dsp/AxiomRasa_Workspace/01_Active_Products/anechoic-mind/build/AnechoicMind_artefacts/Release")
TARGETS = [
    os.path.join(ARTEFACTS_DIR, "VST3", "Anechoic Mind.vst3"),
    os.path.join(ARTEFACTS_DIR, "AU", "Anechoic Mind.component"),
    os.path.join(ARTEFACTS_DIR, "Standalone", "Anechoic Mind.app")
]

RELEASE_DIR = os.path.expanduser(f"~/dev/audio-dsp/AxiomRasa_Workspace/00_Master_Axiom_Shell/Releases/{PLUGIN_NAME}")
ZIP_PATH = f"{RELEASE_DIR}/{PLUGIN_NAME}_{VERSION}_macOS_Universal.zip"

os.makedirs(RELEASE_DIR, exist_ok=True)

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
    for target in TARGETS:
        if os.path.exists(target):
            for root, dirs, files in os.walk(target):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, os.path.dirname(target))
                    zf.write(full_path, rel_path)
        else:
            print(f"[WARN] Hedef bulunamadi: {target}")

    for doc in ["README.md", "CHANGELOG.md", "LICENSE.txt"]:
        if os.path.exists(doc) and os.path.getsize(doc) > 0:
            zf.write(doc, doc)
            print(f"[ADDED DOC] {doc} ({os.path.getsize(doc)} bytes)")

print(f"\n[AXIOM FACTORY] Universal Paket Hazir: {ZIP_PATH}")
```

### File: `.github/workflows/cross_platform_build.yml`
```yml
name: Axiom Rasa Cross-Platform Factory (Win / Mac / Linux)

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_dispatch:

jobs:
  build_plugins:
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: macos-latest
            platform_name: macOS_Universal
          - os: windows-latest
            platform_name: Windows_x64
          - os: ubuntu-22.04
            platform_name: Linux_x64

    runs-on: ${{ matrix.os }}

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install Linux Audio & GUI Dependencies
        if: matrix.os == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y ninja-build libasound2-dev libjack-jackd2-dev \
            ladspa-sdk libcurl4-openssl-dev libfreetype6-dev \
            libx11-dev libxcomposite-dev libxcursor-dev libxext-dev \
            libxinerama-dev libxrandr-dev libxrender-dev libwebkit2gtk-4.0-dev \
            libglu1-mesa-dev mesa-common-dev

      - name: Clone JUCE 8.0.4
        run: git clone --depth 1 --branch 8.0.4 https://github.com/juce-framework/JUCE.git

      - name: Configure CMake
        run: cmake -B build -DCMAKE_BUILD_TYPE=Release

      - name: Build VST3, AU & Standalone
        run: cmake --build build --config Release

      - name: Upload Compiled Plugin Package
        uses: actions/upload-artifact@v4
        with:
          name: AnechoicMind_v0.1.0_${{ matrix.platform_name }}
          path: |
            build/AnechoicMind_artefacts/Release/VST3/**
            build/AnechoicMind_artefacts/Release/AU/**
            build/AnechoicMind_artefacts/Release/Standalone/**
            README.md
            CHANGELOG.md
            LICENSE.txt
```

### File: `.gitignore`
```text
.DS_Store
juce_project/Builds/
juce_project/JuceLibraryCode/
*.build
*.mode1v3
*.pbxuser
*.xcworkspace
*.xcuserdata
*.vst3
*.component
*.clap
*.app
*.zip
*.o
build/
```

### File: `README.md`
```md
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
```

### File: `CHANGELOG.md`
```md
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
```

### File: `LICENSE.txt`
```txt
END-USER LICENSE AGREEMENT (EULA) & BETA TEST LICENSE
Product: Anechoic Mind (v0.1.0)
Author / Brand: Axiom Rasa (https://axiomrasa.xyz)
Copyright (c) 2026 Axiom Rasa. All rights reserved.

1. GRANT OF LICENSE
This software is provided as a pre-release / evaluation copy ("Beta") by Axiom Rasa. You are granted a non-exclusive, non-transferable license to install and use the Software (VST3, AU, and Standalone formats) for testing, evaluation, and audio production feedback.

2. RESTRICTIONS
You may not reverse-engineer, decompile, disassemble, redistribute, resell, or sub-license the binary files or underlying DSP algorithms without prior written consent from Axiom Rasa.

3. DISCLAIMER OF WARRANTY
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL AXIOM RASA BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THE SOFTWARE.
```
