    @echo off
    echo Запуск проверок кода
    start cmd /c "black ."
    start cmd /c "flake8 app"
    start cmd /c "isort ."

    echo Завершаем все java процессы
    taskkill /F /IM java.exe >nul 2>&1
    timeout /t 3 >nul

    echo Запуск сервера SonarQube...
    start cmd /k "C:\Users\korot\Downloads\sonarqube-25.5.0.107428\bin\windows-x86-64\StartSonar.bat"

    echo Ожидание запуска SonarQube (проверка localhost:9000)
    timeout /t 30 >nul

    echo Запуск Sonar Scanner...
    start cmd /c "sonar-scanner & timeout /t 4 & exit"

    echo Запуск сервера uvicorn...
    start cmd /k "uvicorn app.main:app --reload --host localhost --port 8000"
