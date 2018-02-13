#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   xianwen.zhang
#   2017-12-12

import os, io
import urllib, urllib2
import socket
import json
import random
import socket,time  
from multiprocessing import Process
from smtants.ant.include import log
from smtants.ant.target import cpu
from smtants.ant.target import mem

#   check port
def check_port(host, port):
    isOk = False
    try:
        s = socket.socket()
        s.connect((host, int(port)))
        s.close()
        isOk = True
    except:
        log.lg_write(str(host) + ":" + str(port) + " is down !")
    return isOk

#   print debug msg
def debug(tar, ret):
    if ret['res'] == 0:
        log.lg_write(str(tar) + " push is ok !")
    else:
        log.lg_write(str(tar) + " push failed !")

def hbt(data):
    #   get config file
    endpoint     = data['endpoint']
    ip           = data['ip']
    hbtAddrs     = data['hbt']['addrs']
    interval     = data['interval']
    version      = '1.0.0' 

    #   check config file
    if len(hbtAddrs) < 1:
        log.lg_write(" ==ant== hbt addrs config error !")
        exit()

    #   random selection nest
    i = 0
    j = random.randrange(0, len(hbtAddrs))
    while i < len(hbtAddrs):
        hbtAddrsArr = str(hbtAddrs[j]).split(":")
        isOk = check_port(hbtAddrsArr[0], hbtAddrsArr[1])
        if isOk:
            break
        j += 1
        if j == len(hbtAddrs):
            j = 0
        i += 1
    hbtUrl  = 'http://' + str(hbtAddrs[j]) + '/v1/hbt'

    try:
        while True:
            hbtJson = {}
            hbtJson['endpoint'] = endpoint
            hbtJson['ip']       = ip
            hbtJson['version']  = version
            hbtParams = urllib.urlencode(hbtJson).encode(encoding='utf8')
            hbtReq = urllib.urlopen(hbtUrl, hbtParams)
            hbtRet = json.loads(hbtReq.read())
            if hbtRet['res'] > 0:
                log.lg_write(" ==ant== " + str(endpoint) + " hbt failed !")
            time.sleep(int(interval))
    except Exception as e:
        log.lg_write(" ==ant== " + str(e))

def ant(data):
    #   get config file
    endpoint     = data['endpoint']
    nestTimeout  = data['nest']['timeout']
    interval     = data['interval']
    nestAddrs    = data['nest']['addrs']

    #   check config file
    if len(nestAddrs) < 1:
        log.lg_write(" ==ant== nest addrs config error !")
        exit()

    if not nestTimeout:
        nestTimeout = 1000
    
    if not interval:
        interval = 60

    #   random selection nest
    i = 0
    j = random.randrange(0, len(nestAddrs))
    while i < len(nestAddrs):
        nestAddrsArr = str(nestAddrs[j]).split(":")
        isOk = check_port(nestAddrsArr[0], nestAddrsArr[1])
        if isOk:
            break
        j += 1
        if j == len(nestAddrs):
            j = 0
        i += 1

    nestUrl = 'http://' + str(nestAddrs[j]) + '/v1/push'

    targets = {
        'cpu': cpu.cpu, 
        'mem': mem.mem
    }
    try:
        while True:
            timestamp = int(time.time())
            pushJson = {}
            pushJson['endpoint']  = endpoint
            pushJson['step']      = interval
            for tar in dict(targets).keys():
                pushJson['timestamp'] = int(time.time())
                pushJson['value'] = targets.get(tar)()
                nestParams = urllib.urlencode(pushJson).encode(encoding='utf8')
                nestReq = urllib.urlopen(nestUrl, nestParams)
                nestRet = json.loads(nestReq.read())
                if data['debug']:
                    debug(str(tar),nestRet)
                if nestRet['res'] > 0:
                    log.lg_write(" ==ant== target " + str(tar) + " push failed !")
                time.sleep(int(interval / len(targets)))
    except Exception as e:
        log.lg_write(" ==ant== " + str(e))

def main():
    if not os.path.exists('cfg.json'):
        log.lg_write(" ==ant== cfg.json file is not exists !")
        exit()

    f = io.open('cfg.json', 'r', encoding='utf-8')
    data = json.load(f)

    ph = Process(target = hbt, args = (data,))
    ph.start()

    pa = Process(target = ant, args = (data,))
    pa.start()

if __name__ == "__main__":
    main()