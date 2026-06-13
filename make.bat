@echo off
if "%1" == "clean" (
  if exist _build rmdir /s /q _build
  if exist .doctrees rmdir /s /q .doctrees
  if exist _sources rmdir /s /q _sources
  if exist _static rmdir /s /q _static
  if exist guide rmdir /s /q guide
  if exist api rmdir /s /q api
  if exist developer rmdir /s /q developer
  if exist css rmdir /s /q css
  if exist js rmdir /s /q js
  if exist img rmdir /s /q img
  del /q *.html 2>nul
  del /q searchindex.js 2>nul
  del /q objects.inv 2>nul
  del /q .buildinfo 2>nul
  exit /b 0
)

python scripts\build_docs.py
