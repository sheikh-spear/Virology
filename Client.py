import requests
import os
import time
from urllib.parse import quote
import time
import base64

url = "http://192.168.1.2"
os.popen("python3 API.py")

while True:
    a = input(">")
    b = a.split(" ")
    if len(b) > 1 and b[1] == "upload":
        e = base64.b64encode(open(b[2], "rb").read())
        a = b[0] + " " + b[1] + " " + str(e, encoding="utf-8") + " " + b[3]
        requests.get(url + ":5000/admin/" + quote(a))
        print(a)
        print("Uploading...")
        time.sleep(4)
        d = (str(requests.get(url + ":5000/get_res").content, 'utf-8'))
    elif len(b) > 1 and b[1] == "download":
        requests.get(url + ":5000/admin/" + quote(a))
        time.sleep(4)
        d = (str(requests.get(url + ":5000/get_res").content, 'utf-8'))
        while d[:2] == "b\"":
            d = d[2:]
            d = d[:-1].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\x82", "é")
        open(b[3], "wb").write(base64.b64decode(d.split("\\n")[3]))
        print("File saved at " + b[3])
    else:
        requests.get(url + ":5000/admin/" + quote(a))
        time.sleep(4)
        d = (str(requests.get(url + ":5000/get_res").content, 'utf-8'))
        if d[:2] == "b\"":
            d = d[2:]
            d = d[:-1].replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\x82", "é")
        print(d)
    pass