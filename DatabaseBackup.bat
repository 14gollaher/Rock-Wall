

:: Set the below path to your locaiton of 7-Zip install
set PATH=%PATH%;C:\Program Files\7-Zip\
echo %PATH%
7z


7z a RockWall_%date:~-4,4%%date:~-7,2%%date:~-10,2%.7z RockWall.db
move /-y "RockWall_%date:~-4,4%%date:~-7,2%%date:~-10,2%.7z" "C:\Users\mattg\Documents\Database Backups"