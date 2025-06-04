#!/bin/bash

# 운영체제 확인
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "macOS 환경에서 게임을 실행합니다..."
    
    # Python 확인
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "오류: Python이 설치되어 있지 않습니다."
        echo "https://www.python.org/downloads/ 에서 Python을 설치하세요."
        exit 1
    fi
    
    # 가상환경 생성 및 활성화
    echo "가상환경을 설정합니다..."
    $PYTHON_CMD -m venv venv || { echo "가상환경 생성 실패"; exit 1; }
    source venv/bin/activate || { echo "가상환경 활성화 실패"; exit 1; }
    
    # pygame 설치
    echo "필요한 패키지를 설치합니다..."
    pip install pygame || { echo "pygame 설치 실패"; exit 1; }
    
    # 게임 실행
    echo "지뢰 찾기 게임을 시작합니다..."
    $PYTHON_CMD minesweeper.py
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash 또는 MSYS)
    echo "Windows 환경에서 게임을 실행합니다..."
    
    # Python 확인
    if command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "오류: Python이 설치되어 있지 않습니다."
        echo "https://www.python.org/downloads/ 에서 Python을 설치하세요."
        exit 1
    fi
    
    # 가상환경 생성 및 활성화
    echo "가상환경을 설정합니다..."
    $PYTHON_CMD -m venv venv || { echo "가상환경 생성 실패"; exit 1; }
    source venv/Scripts/activate || { echo "가상환경 활성화 실패"; exit 1; }
    
    # pygame 설치
    echo "필요한 패키지를 설치합니다..."
    pip install pygame || { echo "pygame 설치 실패"; exit 1; }
    
    # 게임 실행
    echo "지뢰 찾기 게임을 시작합니다..."
    $PYTHON_CMD minesweeper.py
    
else
    # Linux 및 기타 Unix
    echo "Linux/Unix 환경에서 게임을 실행합니다..."
    
    # Python 확인
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "오류: Python이 설치되어 있지 않습니다."
        echo "패키지 관리자를 통해 Python을 설치하세요."
        exit 1
    fi
    
    # 가상환경 생성 및 활성화
    echo "가상환경을 설정합니다..."
    $PYTHON_CMD -m venv venv || { echo "가상환경 생성 실패"; exit 1; }
    source venv/bin/activate || { echo "가상환경 활성화 실패"; exit 1; }
    
    # pygame 설치
    echo "필요한 패키지를 설치합니다..."
    pip install pygame || { echo "pygame 설치 실패"; exit 1; }
    
    # 게임 실행
    echo "지뢰 찾기 게임을 시작합니다..."
    $PYTHON_CMD minesweeper.py
fi
