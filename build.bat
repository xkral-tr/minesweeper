pyinstaller src/main.py  --onefile --noconsole --name minesweeper
xcopy "assets" "dist/assets" /e
echo Done!