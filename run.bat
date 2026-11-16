@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

rem Load .env for Docker Compose and the Python process when present.
if exist ".env" (
  for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
    if not "%%~A"=="" set "%%~A=%%~B"
  )
)

if /i "%~1"=="stop" (
  where docker >nul 2>&1
  if errorlevel 1 (
    echo [error] docker is not available on PATH.
    exit /b 1
  )
  echo [info] Stopping services...
  docker compose down
  exit /b %ERRORLEVEL%
)

if not defined NEO4J_PASSWORD (
  echo [error] NEO4J_PASSWORD is not set. Copy .env.example to .env or export it.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [error] .venv is missing. Run: python -m venv .venv
  echo         Then: .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
  exit /b 1
)

where docker >nul 2>&1
if errorlevel 1 (
  echo [error] docker is not available on PATH.
  exit /b 1
)

echo [info] Restarting services: stop if running, then start.
for /f "tokens=*" %%I in ('docker compose ps --status running -q neo4j 2^>nul') do set "RUNNING=%%I"
if defined RUNNING (
  docker compose down
  if errorlevel 1 exit /b 1
)

docker compose up -d
if errorlevel 1 exit /b 1

set /a ATTEMPTS=0
:wait_healthy
set "STATUS="
set "CID="
for /f "tokens=*" %%I in ('docker compose ps -q neo4j 2^>nul') do set "CID=%%I"
if not defined CID goto retry
for /f "tokens=*" %%H in ('docker inspect --format "{{.State.Health.Status}}" !CID! 2^>nul') do set "STATUS=%%H"
if /i "!STATUS!"=="healthy" goto ready

:retry
set /a ATTEMPTS+=1
if !ATTEMPTS! GEQ 60 goto timeout
ping -n 4 127.0.0.1 >nul
goto wait_healthy

:timeout
echo [error] Neo4j did not become healthy in time.
echo         If the logs show authentication failures, the .env password does not match
echo         the existing Neo4j volume. Use the original password, or recreate the volume:
echo         docker compose down -v
exit /b 1

:ready
echo [info] Neo4j is healthy.
.\.venv\Scripts\python.exe -c "from validation_service.bootstrap import create_neo4j_connection; connection = create_neo4j_connection(); print('Neo4j connectivity:', connection.verify()); connection.close()"
if errorlevel 1 exit /b 1

if exist "src\validation_service\__main__.py" (
  echo [info] Starting application...
  .\.venv\Scripts\python.exe -m validation_service
) else (
  echo [info] No application entrypoint yet; services and connectivity are ready.
)
exit /b 0
