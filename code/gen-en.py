#!/usr/bin/env python3
# Generate code/en/ from code/ by translating ONLY user-facing strings
# (rule descriptions, titles, notification text). Key mappings are untouched,
# so the two configs are guaranteed structurally identical.
import os, shutil, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root = parent of code/
MAP = {
    # descriptions
    "Cmd+Shift+V로 Spotlight 클립보드 히스토리 열기 (Win+V 스타일)":
        "Open Spotlight clipboard history with Cmd+Shift+V (Win+V style)",
    "F1~F12: 짧게 = 펑션키, 길게(200ms) = 밝기/볼륨 등 특수키 (F6 제외)":
        "F1–F12: tap = function key, hold (200ms) = brightness/volume/media (F6 excluded)",
    "NumLock/Clear 키로 키패드 모드 토글 (알림 표시)":
        "Toggle keypad mode with NumLock/Clear (shows a notification)",
    "[1순위] Finder: Ctrl+C 복사 / Ctrl+X 잘라내기 / Ctrl+V 붙여넣기·이동":
        "[Priority 1] Finder: Ctrl+C copy / Ctrl+X cut / Ctrl+V paste · move",
    "[2순위] 일반 앱: Ctrl+A/Z/Y/S/F/N/T/W/P/R/L/O/C/X/V → Cmd 동일키 (터미널·IDE 제외, Shift 조합 유지)":
        "[Priority 2] Apps: Ctrl+A/Z/Y/S/F/N/T/W/P/R/L/O/C/X/V → same Cmd key (terminals · IDEs excluded, Shift combos preserved)",
    "오른쪽 Command = 순수 한영키 (지구본 fn 탭, 즉시 발동)":
        "Right Command = Korean/English toggle (globe fn tap, fires instantly)",
    "오른쪽 Option(Alt) = 한자키 (option+Return, Win11 방식)":
        "Right Option (Alt) = Hanja key (option+Return, Win11 style)",
    "커서 모드: 키패드 → 내비게이션 키":
        "Cursor mode: keypad → navigation keys",
    # titles
    "Cmd+Shift+V → Spotlight 클립보드 히스토리 (macOS 26 Tahoe)":
        "Cmd+Shift+V → Spotlight clipboard history (macOS 26 Tahoe)",
    "F키 숏/롱 이중 동작":
        "F-key short/long dual action",
    "Numpad NumLock Toggle (숫자 ↔ 커서 모드)":
        "Numpad NumLock Toggle (number ↔ cursor mode)",
    "Windows식 Ctrl 단축키 v3 (A/Z/Y/S/F/N/T/W/P/R/L/O/C/X/V, Finder 이동 지원, 터미널·IDE 제외)":
        "Windows-style Ctrl shortcuts v3 (A/Z/Y/S/F/N/T/W/P/R/L/O/C/X/V, Finder move support, terminals · IDEs excluded)",
    "한영·한자 v5 (우측 Cmd=한영, 우측 Alt=한자, Win11 방식)":
        "Korean/English · Hanja v5 (Right Cmd=Korean/English, Right Alt=Hanja, Win11 style)",
    # notification text
    "Numpad: 숫자 모드": "Numpad: Number mode",
    "Numpad: 커서 모드": "Numpad: Cursor mode",
    "잘라내기 — 붙여넣으면 이동됨": "Cut — paste to move",
}

src = os.path.join(REPO, "code")
dst = os.path.join(REPO, "code", "en")
if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(os.path.join(dst, "complex_modifications"))

def translate(path_in, path_out):
    s = open(path_in, encoding="utf-8").read()
    for ko, en in MAP.items():
        s = s.replace(ko, en)
    # any Korean left over is a bug — fail loudly
    import re
    leftover = re.findall(r'[가-힣]+', s)
    assert not leftover, f"untranslated Korean in {path_out}: {set(leftover)}"
    open(path_out, "w", encoding="utf-8").write(s)

translate(os.path.join(src, "karabiner.json"), os.path.join(dst, "karabiner.json"))
for f in sorted(glob.glob(os.path.join(src, "complex_modifications", "*.json"))):
    translate(f, os.path.join(dst, "complex_modifications", os.path.basename(f)))
print("generated code/en/")
