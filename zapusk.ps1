netsh advfirewall firewall add rule name="Flask 5000" dir=in action=allow protocol=TCP localport=5000
netstat -an | findstr 5000
wsl
