@echo off
setlocal

set GRADLE_VERSION=8.5
set GRADLE_URL=https://services.gradle.org/distributions/gradle-%GRADLE_VERSION%-bin.zip

echo Downloading Gradle wrapper...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%GRADLE_URL%' -OutFile 'gradle.zip'}"

echo Extracting...
powershell -Command "Expand-Archive -Path gradle.zip -DestinationPath . -Force"

echo Cleaning up...
del gradle.zip

echo Gradle wrapper setup complete!
