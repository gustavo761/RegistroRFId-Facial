@echo off

mysqldump -h 192.168.100.32 -u director -pjmpadmin joseManuelPando > C:\RegistroRfidFacial\CopiasSeguridad\%date:~-4,4%-%date:~-7,2%-%date:~-10,2%-%time:~0,2%-%time:~3,2%-%time:~6,2%.sql