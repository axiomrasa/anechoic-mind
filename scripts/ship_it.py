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
