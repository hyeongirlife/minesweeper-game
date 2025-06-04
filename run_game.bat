@echo off
echo 지뢰 찾기 게임을 설치하고 실행합니다...

REM Python 확인
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 오류: Python이 설치되어 있지 않습니다.
    echo https://www.python.org/downloads/ 에서 Python을 설치하세요.
    pause
    exit /b 1
)

REM 가상환경 생성 및 활성화
echo 가상환경을 설정합니다...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo 가상환경 생성 실패
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo 가상환경 활성화 실패
    pause
    exit /b 1
)

REM pygame 설치
echo 필요한 패키지를 설치합니다...
pip install pygame
if %ERRORLEVEL% NEQ 0 (
    echo pygame 설치 실패
    pause
    exit /b 1
)

REM 게임 실행
echo 지뢰 찾기 게임을 시작합니다...
python minesweeper.py

pause
