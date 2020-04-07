from configparser import ConfigParser
from subprocess import Popen,PIPE
from shlex import split
import logging
import sys


"""
All the function below are the standard git operation, required by ritmOtt
"""

def handleConfig(gitURL, username, password, repo, mask):
    """
    handleConfig, is a function used to mask the the username : password in the .git/config
    """
    rConfig = ConfigParser()
    rConfig.read(repo + "/.git/config")
    if mask:
        rConfig.set('remote \"origin\"', 'url', gitURL.replace("username", username).replace("password",
                                                                                             password) + "/" + repo + ".git")
    else:
        rConfig.set('remote \"origin\"', 'url', "NONE")
    with open(repo + "/.git/config", "w") as cFIle:
        rConfig.write(cFIle)

def gitClone(gitURL, username, password, repo):
    url = gitURL.replace("username", username).replace("password", password)
    cmd = "git clone " + url + "/" + repo + ".git"
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    return value.returncode, stderr

def gitPull():
    cmd = "git pull origin master"
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    return value.returncode, stderr

def gitListModifyFiles():
    cmd = "git status --short "
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    statusValue = ""
    if stdout.decode().strip():
        statusValue = stdout.decode().strip().split("\n")
    return value.returncode, statusValue, stderr

def gitAdd(fileNames):
    cmd = "git add " + fileNames
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    return value.returncode, stdout, stderr

def gitCommit(commitMSG):
    cmd = "git commit -m \"" + commitMSG + "\""
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    return value.returncode, stdout, stderr

def gitPush():
    cmd = "git push origin master"
    value = Popen(split(cmd), stderr=PIPE, stdin=PIPE, stdout=PIPE)
    stdout, stderr = value.communicate()
    return value.returncode, stdout, stderr

def gitPrintOut(returncode,stdout,error):
    if returncode != 0 :
        ogging.error(error.decode())
        sys.exit(1)
    else:
        logging.debug(stdout.decode())

