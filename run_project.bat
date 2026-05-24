@echo off
echo Starting Resume Analyzer...

cd /d C:\resume_analyzer

start /B cmd /c "cd backend && venv\Scripts\activate && python manage.py runserver"
start /B cmd /c "cd frontend && npm run dev"

echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
echo Press CTRL + C to stop
pause