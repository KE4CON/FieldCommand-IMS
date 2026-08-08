@echo off
REM ==========================================================================
REM FieldCommand IMS - SD card prep (double-click this file)
REM Runs prep-sd-card.ps1 to make an "insert and go" FieldCommand card.
REM ==========================================================================
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0prep-sd-card.ps1"
