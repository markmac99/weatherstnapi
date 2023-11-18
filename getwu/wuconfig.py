# config file
import os

stationid = 'IKIDLI17'


def getWUkey():
    passwordfile = os.path.expanduser('~/.ssh/wupass')
    with open(passwordfile) as inf:
        passwd = inf.readline().strip()
    return passwd


def getOpenhabURL():
    passwordfile = os.path.expanduser('~/.ssh/myohpass')
    with open(passwordfile) as inf:
        username = inf.readline().strip()
        passwd = inf.readline().strip()
    
    ohurl = 'https://{}:{}@myopenhab.org/rest'.format(username, passwd)
    return ohurl
