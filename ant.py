#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   xianwen.zhang
#   2017-12-12

import os
import json
import random
import socket,time  
from smtants.ant.include import log
from smtants.ant.target import cpu
from smtants.ant.target import mem

def ant():
    if not os.path.exists('cfg.json'):
        log.lg_write_ant(" ==ant== cfg.json file is not exists !")
        exit()

    f = open('cfg.json', encoding='utf-8')
    data = json.load(f)

    #   get config file
    endpoint     = data['endpoint']
    nestTimeout  = data['nest']['timeout']
    nestInterval = data['nest']['interval']
    nestAddrs    = data['nest']['addrs']

    #   check config file
    if len(nestAddrs) < 1:
        log.lg_write_ant(" ==ant== addrs config error !")
        exit()

    if not nestTimeout:
        nestTimeout = 1000
    
    if not nestInterval:
        nestInterval = 60

    #   random selection nest
    i = random.randrange(0, len(nestAddrs))
    sk = nestAddrs[i].split(':')

    if len(sk) < 2:
        log.lg_write_ant(" ==ant== addrs config error !")
        exit()

    HOST = sk[0]
    PORT = sk[1]

    timestamp = int(time.time())

    try:
        while True:
            timestamp = int(time.time())

            tar = {}
            tar['endpoint']  = endpoint
            tar['timestamp'] = timestamp
            tar['step']      = nestInterval
            
            #   cpu
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            s.connect((HOST, int(PORT)))
            tar['dataType'] = 'cpu'
            tar['value']    = cpu.cpu()
            s.send(str(tar).encode()) 
            s.close() 
            time.sleep(int(nestInterval / 2))

            #   mem
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            s.connect((HOST, int(PORT)))
            tar['dataType'] = 'mem'
            tar['value']    = mem.mem()
            s.send(str(tar).encode()) 
            s.close() 
            time.sleep(int(nestInterval / 2))

            #   
    except Exception as e:
        log.lg_write_ant(" ==ant== " + str(e))
        exit()

if __name__ == "__main__":
    ant()