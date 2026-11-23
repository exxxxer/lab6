@echo off
chcp 65001 >nul
cd /d "%~dp0"
where uv >nul 2>&1
if errorlevel 1 (
 echo uv ne naiden. Ustanovite: https://docs.astral.sh/uv/getting-started/installation/
 pause
 exit /b 1
)
if not exist .env copy .env.example .env >nul
uv sync
if errorlevel 1 (pause & exit /b 1)
echo http://127.0.0.1:8000/docs
uv run uvicorn main:app --reload
pause
