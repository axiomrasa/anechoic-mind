import os
import subprocess

WORKSPACE = os.path.expanduser("~/dev/audio-dsp/AxiomRasa_Workspace")
PROJECT_DIR = os.path.expanduser("~/dev/audio-dsp/AxiomRasa_Workspace/01_Active_Products/anechoic-mind")
JUCE_DIR = os.path.expanduser("~/dev/third-party/JUCE")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "PROJECT_CONTEXT_DUMP.md")

IGNORE_DIRS = {".git", "build", "Builds", "JuceLibraryCode", "__pycache__"}
INCLUDE_FILES = [
    "CMakeLists.txt",
    "dsp/anechoic_mind.dsp",
    "scripts/ship_it.py",
    ".github/workflows/cross_platform_build.yml",
    ".gitignore",
    "README.md",
    "CHANGELOG.md",
    "LICENSE.txt"
]

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except Exception as e:
        return f"Error: {e}"

vst3_bin = os.path.expanduser("~/Library/Audio/Plug-Ins/VST3/Anechoic Mind.vst3/Contents/MacOS/Anechoic Mind")
lipo_cmd = f'lipo -archs "{vst3_bin}" 2>/dev/null'

lines = []
lines.append("# AXIOM RASA — PROJECT CONTEXT SNAPSHOT")
lines.append(f"**Current Working Directory:** `{os.getcwd()}`\n")

lines.append("## 1. Environment & Toolchain Status")
lines.append("```text")
lines.append(f"macOS Version : {run_cmd('sw_vers -productVersion')} ({run_cmd('uname -m')})")
lines.append(f"Faust Version : {run_cmd('faust --version | head -n 1')}")
lines.append(f"CMake Version : {run_cmd('cmake --version | head -n 1')}")
lines.append(f"Ninja Version : {run_cmd('ninja --version')}")
lines.append(f"JUCE Git Head : {run_cmd(f'git -C {JUCE_DIR} log -1 --oneline')}")
lines.append(f"Git Status    : {run_cmd('git status -s') or 'Clean'}")
lines.append(f"Installed VST3: {run_cmd(lipo_cmd) or 'Not found'}")
lines.append("```\n")

lines.append("## 2. Workspace Directory Tree (`~/dev/audio-dsp/AxiomRasa_Workspace`)")
lines.append("```text")
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in sorted(dirs) if d not in IGNORE_DIRS and not d.endswith((".vst3", ".component", ".app"))]
    level = root.replace(WORKSPACE, "").count(os.sep)
    indent = "  " * level
    lines.append(f"{indent}{os.path.basename(root)}/")
    subindent = "  " * (level + 1)
    for f in sorted(files):
        if f != ".DS_Store":
            lines.append(f"{subindent}{f}")
lines.append("```\n")

lines.append("## 3. Core Project Files Content")
for rel_path in INCLUDE_FILES:
    full_path = os.path.join(PROJECT_DIR, rel_path)
    if os.path.exists(full_path):
        lines.append(f"### File: `{rel_path}`")
        ext = os.path.splitext(rel_path)[1].lstrip(".") or "text"
        lines.append(f"```{ext}")
        with open(full_path, "r", errors="ignore") as f:
            lines.append(f.read().strip())
        lines.append("```\n")

report = "\n".join(lines)
with open(OUTPUT_FILE, "w") as f:
    f.write(report)

subprocess.run("pbcopy", input=report.encode("utf-8"), shell=True)
print(f"[AXIOM SNAPSHOT] Tum proje dokumu '{OUTPUT_FILE}' dosyasina yazildi ve PANOYA KOPYALANDI (Cmd+V ile yapistirabilirsin)!")
