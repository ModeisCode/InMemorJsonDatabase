from lexer import getLexedData
import json
from colorama import Fore
import socket
import os

ascii_imjdb = """
 ___                                    _              ___  ___  
 |_ _|_ _  _ __  ___ _ __  ___ _ _ _  _ (_)___ ___ _ _ |   \| _ \ 
  | || ' \| '  \/ -_\ '  \/ _ \ '_| || || (_-</ _ \ ' \| |) | _ \ 
 |___|_||_|_|_|_\___|_|_|_\___/_|  \_, |/ /__/\___/_||_|___/|___/ 
                                   |__/__/                        
                        VERSION: 1.0.0
"""


class Key:
    def __init__(self,name,args) -> None:
        self.name = name
        self.args = args
    def addNewValue(self,value):
        self.args.append(value)
    def addNewValueList(self,values):
        for value in values:
            self.args.append(value)
    def getValue(self):
        return self.args

class Group:
    def __init__(self,name :str,args: list) -> None:
        self.name = name
        self.keys_args = args
    def __init__(self,name) -> None:
        self.name = name
        self.keys_args = []
    def newKey(self,name,args):
        key = Key(name,args)
        self.key_args.append(key)
    def newKeyWithKey(self,key :Key):
        self.keys_args.append(key)
    def getKey(self,name):
        c = 0
        for key in self.keys_args:
            if key.name == name:
                return (name,key.args)
            c += 1
    def delKey(self,name):
        c = 0
        for key in self.keys_args:
            if key.name == name:
                self.keys_args.remove(key) 
            c += 1       
    def delKeyValue(self,name,value):
        c = 0
        for key in self.keys_args:
            if key.name == name:
                for arg in key.args:
                    key.args.remove(value)
            c += 1         
    def showAllKeys(self):
        for key in self.keys_args:
            print(key.name , key.args)

#IN_GROUP_MODE = False
#IN_GROUP_GROUP = None
GROUPS = []
LOG = ""

def printErr(text :str):
    print(Fore.RED + text + Fore.RESET)

def printInfo(text :str):
    print(Fore.LIGHTGREEN_EX + text + Fore.RESET)


def startConfigFile():
    data = {
    "ip": "localhost",
    "port": 9999,
    "username": "admin",
    "password": "default",
    "version" : "latest"
    }

    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)

def readConfigFile(string :str):
    with open("settings.json") as f:
        data = json.load(f)
    json_data = data[string]
    print(json_data)
    return json_data

def saveToLog(text :str):
    global LOG
    LOG += (text + "\n")

def newGroup(group :Group):
    global GROUPS
    GROUPS.append(group)

def isGroupExists(group_name :str):
    global GROUPS
    for group in GROUPS:
        if group.name == group_name:
            return group
    return False

def addKeyToGroup(key :Key , group_name :str):
    groupData = isGroupExists(group_name)
    if groupData != False:
        groupData.newKeyWithKey(key)
        printInfo("NEW KEY HAS ADDED TO GROUP: " + groupData.name + " KEY_NAME:" + key.name)
        print(key.args)
    else:
        printErr("ERROR/GROUP_NOT_FOUND/imjdb:99541/THE GROUP SPECIFIED DOES NOT EXISTS")
        printErr("ERROR/ERROR_IN_ADDING_TO_MEMORY/imjdb:90015/ERROR IN ADDING KEY TO MEMORY")

def checkError(errs):
    if errs['TO_INDEXED_KEY_NOT_ENOUGH'] == 0 and errs['COMMAND_NOT_ENOUGH'] == 0 and errs['PARAMETER_NOT_ENOUGH'] == 0:
        return True
    else:
        return False

def applyInstruction(instruction):
    if instruction['COMMAND'] == 'NEWGROUP':
        try:
            newGroup(Group(instruction['GROUP']))
            printInfo("GROUP HAS BEEN ADDED! GROUP_NAME:" + instruction['GROUP'])
        except:
            printErr("")
    elif instruction['COMMAND'] == 'ADD':
        addKeyToGroup(Key(instruction['KEY'],instruction['VALUES']),instruction['GROUP'])
    elif instruction['COMMAND'] == 'SHOWGROUPS':
        pass

async def startSocketServer(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen()
    conn , addr = await s.accept()
    cmd = ""
    while cmd not in ("q","quit","exit"):
        cmd = conn.recv(4096).decode("utf-8")
        print(cmd)
        instruction, errs = getLexedData(cmd)
        applyInstruction(instruction)
        print(errs)
        
isInstructionEnabled = False    
input_text = Fore.LIGHTGREEN_EX + '[$]' + Fore.RESET

def clearTerminal():
    try:
        os.system("clear")
    except:
        printErr("imjdb:49001:COMMAND_EXECUTION_FAILED")
        printErr("CANNOT CLEAR TERMINAL. CODE MIGHT BE DOES NOT EXISTS YOUR TERMINAL OR OPERATING SYSTEM VERSION ")

def applyCommands(cmd :str):
    global isInstructionEnabled,input_text
    if cmd == "rconf":
        rc = input('Please insert config data to get:')
        try:
            readConfigFile(rc)
        except FileNotFoundError as fnfe:
            print(fnfe.args)
    elif cmd == "go":
        isInstructionEnabled = True
        input_text = Fore.LIGHTGREEN_EX + '[$INSTRUCTION$]' + Fore.RESET
    elif cmd == "clear":
        clearTerminal()

def startApp():
    print(ascii_imjdb)
    global isInstructionEnabled,input_text
    startConfigFile()
    cmd = ""
    while cmd not in ("q","quit","exit"):
        cmd = input(input_text)
        print(Fore.LIGHTMAGENTA_EX + cmd + Fore.RESET)
        if isInstructionEnabled:
            if cmd in ("clear","cls"):
                clearTerminal()
            else:
                instruction, errs = getLexedData(cmd)
                applyInstruction(instruction)
                print(errs)
        else:
            applyCommands(cmd)
        

'''
key = Key("mykey",[15,"hacked"])
group = Group("mygroup",[key,Key("mynewkey",["client",45])])
group.getKey("mynewkey")
group.delKey("mynewkey")
group.showAllKeys()
print(group.getKey("mynewkey"))


input_text = "ADD mygroup mykey 100,\"my string value\""

GROUPS.append(Group("mygroup"))
instruction, errs = getLexedData(input_text)
#print(checkError(errs))
#print(instruction,errs)
applyInstruction(instruction)


for g in GROUPS:
    print("groups",g.keys_args[0].name,len(GROUPS))
'''

startApp()
