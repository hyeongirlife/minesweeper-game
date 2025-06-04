# 지뢰 찾기 게임 (Minesweeper Game)

Amazon Q로 만든 지뢰 찾기 게임입니다.

## 특징
- 메인 페이지와 게임 페이지 구성
- 초급, 중급, 고급 난이도 지원
- 지뢰 폭발 시 애니메이션 효과
- 한글 지원
- 움직이는 지뢰 애니메이션 배경
- 게임 오버 시 재시작 모달

## 스크린샷
![메인 화면](screenshots/main_screen.png)
![게임 화면](screenshots/game_screen.png)
![폭발 효과](screenshots/explosion.png)

## 설치 및 실행 방법

### 방법 1: 자동 설치 스크립트 사용 (가장 쉬운 방법)
```bash
# 1. 저장소 복제
git clone https://github.com/hyeongirlife/minesweeper-game.git
cd minesweeper-game

# 2. 실행 스크립트 실행
# Windows
run_game.bat

# macOS/Linux
./run_game.sh
```
이 스크립트는 자동으로 가상환경을 생성하고, 필요한 패키지를 설치한 후 게임을 실행합니다.

### 방법 2: 가상환경 수동 설정
```bash
# 1. 저장소 복제
git clone https://github.com/hyeongirlife/minesweeper-game.git
cd minesweeper-game

# 2. 가상환경 생성 및 활성화
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 3. 필요한 패키지 설치
pip install -r requirements.txt

# 4. 게임 실행
# Windows
python minesweeper.py

# macOS/Linux
python3 minesweeper.py
```

### 방법 3: 직접 설치
```bash
# 1. 저장소 복제
git clone https://github.com/hyeongirlife/minesweeper-game.git
cd minesweeper-game

# 2. 필요한 패키지 설치
# Windows
pip install pygame

# macOS/Linux
pip3 install pygame

# 3. 게임 실행
# Windows
python minesweeper.py

# macOS/Linux
python3 minesweeper.py
```

### 방법 4: ZIP 다운로드 (Git 없이)
1. GitHub 페이지에서 "Code" 버튼 클릭 > "Download ZIP" 선택
2. 다운로드한 ZIP 파일 압축 해제
3. 압축 해제한 폴더에서:
   - Windows: `run_game.bat` 실행
   - macOS/Linux: 터미널에서 `chmod +x run_game.sh && ./run_game.sh` 실행

## 게임 조작법
- 메인 페이지에서 "게임 시작" 버튼 클릭: 게임 시작
- 좌클릭: 칸 열기
- 우클릭: 깃발 설치/제거
- 상단 영역 더블클릭: 난이도 메뉴 열기
- 이모티콘 클릭: 게임 재시작

## 난이도
- 초급: 9x9 격자, 10개 지뢰
- 중급: 16x16 격자, 40개 지뢰
- 고급: 30x16 격자, 99개 지뢰

## 문제 해결
- **pygame 설치 오류**: 시스템에 따라 추가 종속성이 필요할 수 있습니다.
  - Ubuntu/Debian: `sudo apt-get install python3-pygame`
  - macOS: `brew install sdl sdl_image sdl_mixer sdl_ttf portmidi`
- **한글 표시 문제**: 시스템에 한글 폰트가 없는 경우 영문으로 표시될 수 있습니다.

## 제작자
- 현걸 (hyeongirlife)

## 라이선스
MIT License
