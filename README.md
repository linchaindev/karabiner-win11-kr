# karabiner-win11-kr

**Windows 11 한국어 키보드 습관을 macOS에 그대로 이식하는 Karabiner-Elements 설정**

Windows 11 Korean keyboard habits on macOS, powered by [Karabiner-Elements](https://karabiner-elements.pqrs.org/).

윈도우를 오래 쓰다 맥으로 넘어온 한국어 사용자를 위한 설정 모음입니다. 한영키·한자키·NumLock·Ctrl 단축키를 윈도우와 동일한 감각으로 쓸 수 있습니다.

## 기능

| 키 | 동작 | 비고 |
|---|---|---|
| **우측 Cmd** (스페이스바 오른쪽) | 한영 전환 | 윈도우 한영키 위치. 빠르게 연타하거나 다음 키와 겹쳐 눌러도 안 꼬임 |
| **우측 Opt(Alt)** | 한자 변환 | 한글 입력 직후 누르면 한자 후보 목록 (윈도우 한자키와 동일) |
| **NumLock(Clear)** | 키패드 모드 토글 | 숫자 입력 ↔ 커서 이동(Home/End/PgUp/PgDn/화살표/Del) 전환. 토글 시 알림 표시 |
| **Ctrl+C / X / V** | 복사 / 잘라내기 / 붙여넣기 | Finder에서는 Ctrl+X → Ctrl+V로 **파일 이동**까지 지원 |
| **Ctrl+A/Z/Y/S/F/N/T/W/P/R/L/O** | 전체선택/실행취소/재실행/저장/찾기/새창/새탭/탭닫기/인쇄/새로고침/주소창/열기 | Shift 조합 유지 (Ctrl+Shift+T 닫은 탭 복구 등) |
| **Cmd+Shift+V** | 클립보드 히스토리 | Win+V 대응. macOS 26 Tahoe의 Spotlight 클립보드 사용 |

### 설계 원칙

- **터미널·IDE는 건드리지 않음** — Terminal, iTerm2, kitty, WezTerm, Warp, Ghostty, Alacritty, Hyper, VS Code, Cursor, JetBrains 계열에서는 Ctrl+C(SIGINT) 등 원래 기능이 그대로 유지됩니다.
- **한영 전환은 네이티브 경로 사용** — 입력소스를 API로 직접 바꾸지 않고 지구본(fn) 키 이벤트를 발생시켜 macOS 네이티브 전환 경로를 탑니다. 브라우저 입력창에서 IME 상태가 꼬이는 고질적인 문제가 없습니다.
- **한영키는 즉시 발동** — 키를 누르는 순간 전환이 완료되므로, 한영키를 떼기 전에 다음 글자를 치는 빠른 타이핑 습관에서도 Cmd+조합키가 오발동하지 않습니다.
- **Cmd 단축키는 그대로** — Cmd+C/V, Cmd+Tab 등 macOS 기본 단축키는 전부 살아 있습니다. Ctrl과 Cmd 어느 쪽을 눌러도 됩니다.

## 요구 사항

- macOS (Apple Silicon / Intel)
- [Karabiner-Elements](https://karabiner-elements.pqrs.org/) — 설치 스크립트가 자동으로 설치해 줍니다
- 클립보드 히스토리(Cmd+Shift+V)는 macOS 26 Tahoe 이상 필요 (다른 기능은 버전 무관)

## 설치

### 방법 1: 자동 설치 스크립트 (권장)

```bash
curl -fsSL https://raw.githubusercontent.com/linchaindev/karabiner-win11-kr/dev/release/v1/setup-karabiner.sh | bash
```

스크립트가 하는 일:

1. Homebrew 확인 (없으면 설치)
2. Karabiner-Elements 설치 (이미 있으면 건너뜀)
3. 기존 카라비너 설정 백업 후 본 설정 배포
4. 시스템 설정 자동 적용 — 지구본 키 = 입력 소스 변경, Caps Lock 한영 전환 끄기
5. Karabiner 실행 (권한 승인 팝업 유도)

### 방법 2: 수동 설치

```bash
git clone https://github.com/linchaindev/karabiner-win11-kr.git
mkdir -p ~/.config/karabiner/assets
cp karabiner-win11-kr/code/karabiner.json ~/.config/karabiner/
cp -R karabiner-win11-kr/code/complex_modifications ~/.config/karabiner/assets/
defaults write com.apple.HIToolbox AppleFnUsageType -int 1
defaults write com.apple.HIToolbox TISRomanSwitchState -int 0
```

> 기존 카라비너 설정이 있다면 `~/.config/karabiner`를 먼저 백업하세요. `karabiner.json`이 통째로 교체됩니다. 기존 룰을 유지하고 싶다면 `code/complex_modifications/`의 파일만 `~/.config/karabiner/assets/complex_modifications/`에 넣고 Karabiner UI의 Complex Modifications → Add rule에서 원하는 룰만 선택하세요.

### 설치 후 수동 확인 (macOS 보안상 자동화 불가)

1. 드라이버(시스템 확장) 허용 팝업 승인
2. 시스템 설정 → 개인정보 보호 및 보안 → 입력 모니터링에서 `karabiner_grabber` 허용
3. (선택) 시스템 설정 → Spotlight → **Clipboard** 켜기 — Cmd+Shift+V용
4. 시스템 설정 → 키보드 → 입력 소스에 한글(두벌식)과 ABC 두 개만 있는지 확인 — 제3의 입력소스가 있으면 한영 토글 순환이 어긋날 수 있습니다

## 폴더 구조

```
├── code/                          # 카라비너 설정 원본
│   ├── karabiner.json             # 전체 룰이 활성화된 완성 설정
│   └── complex_modifications/     # 룰별 개별 파일 (선택 설치용)
│       ├── hangul-toggle.json         # 한영키·한자키
│       ├── windows-style-copy.json    # Ctrl 단축키 + Finder 파일 이동
│       ├── numpad-numlock-toggle.json # NumLock 토글
│       └── spotlight-clipboard.json   # 클립보드 히스토리
└── release/
    └── v1/
        └── setup-karabiner.sh     # 자동 설치 스크립트 (설정 내장, 단일 파일)
```

## 커스터마이즈

- **일부 기능만 쓰고 싶다면**: `code/complex_modifications/`의 파일을 개별 설치하세요 (위 방법 2 참고).
- **터미널·IDE 예외 목록 수정**: `windows-style-copy.json`의 `bundle_identifiers` 배열에 앱의 번들 ID를 추가/제거하면 됩니다. 번들 ID는 `osascript -e 'id of app "앱이름"'`으로 확인할 수 있습니다.
- **Ctrl 매핑 키 추가**: `windows-style-copy.json`의 manipulator 하나를 복사해서 `key_code`만 바꾸면 됩니다.

## 문제 해결

| 증상 | 해결 |
|---|---|
| 한영 전환이 안 됨 | 시스템 설정 → 키보드 → "지구본 키를 누르면"이 **입력 소스 변경**인지 확인 |
| Caps Lock으로도 한영이 전환됨 | 시스템 설정 → 키보드 → 입력 소스 편집 → "Caps Lock 키로 ABC 입력 소스 전환" 끄기 (스크립트가 자동 적용하지만 재로그인 필요할 수 있음) |
| NumLock 토글이 안 먹음 | 키보드마다 NumLock이 `keypad_num_lock` 또는 `keypad_clear`로 들어옵니다. 둘 다 매핑돼 있지만, 그래도 안 되면 Karabiner-EventViewer로 실제 key_code를 확인하세요 |
| Cmd+Shift+V가 안 뜸 | macOS 26 Tahoe 이상 + 시스템 설정 → Spotlight → Clipboard 활성화 필요. Spotlight 단축키를 Cmd+Space에서 바꿨다면 룰 수정 필요 |
| 룰이 아예 안 먹음 | Karabiner 입력 모니터링 권한, 드라이버 승인 여부 확인 |

## 라이선스

MIT
