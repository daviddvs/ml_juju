import subprocess, os, netifaces
from netifaces import AF_INET
#repoPath="https://github.com/daviddvs/ml_nfv_ec.git"
wd=os.path.expanduser('~')+"/Documents/ml_nfv_ec/backend"
#subprocess.run(["git", "clone", repoPath, wd])
#subprocess.run(["pip3", "install", "-r", "requirements.txt"], cwd=wd)
#subprocess.run(["python3", "server.py"], cwd=wd)
ifname=netifaces.interfaces()[1]
ip = netifaces.ifaddresses(ifname)[AF_INET][0]['addr']
print(ip)
#netifaces.ifaddresses()
print("app run")
