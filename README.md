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

## 설치 방법
1. Python 3.x 설치
2. 필요한 패키지 설치:
   ```
   pip install pygame
   ```
3. 게임 실행:
   ```
   python minesweeper.py
   ```

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

## 제작자
- 현걸 (hyeongirlife)

## 라이선스
MIT License
