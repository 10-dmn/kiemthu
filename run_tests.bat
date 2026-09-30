@echo off
echo Running tests...

call venv\Scripts\activate

pytest -q --disable-warnings --html=tests_reports/report.html --self-contained-html

echo Opening report...
start tests_reports\report.html

echo Done.
pause
