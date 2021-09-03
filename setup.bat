@echo off
color a
echo Just a moment ...

pip install --upgrade pip
pip install pycryptodome

echo ___________________________________________________
echo ___________________________________________________
echo Setup Complete, Thank You For Your Patience
set /p launch=Would you like to run The Gobfuscator now?		( Y / N )


if %launch%==y python Gobfuscator.py
if %launch%==Y python Gobfuscator.py