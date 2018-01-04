#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   xianwen.zhang
#   2017-12-12

import os
import urllib.request
import urllib.parse
import json
import random
import socket,time  
from smtants.ant.include import log
from smtants.ant.target import cpu
from smtants.ant.target import mem

#   print debug msg
def debug(tar, ret):
    if ret['res'] == 0:
        print(str(tar) + " push is ok !")
    else:
        print(str(tar) + " push failed !")

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
    url = 'http://' + str(nestAddrs[i]) + '/v1/push'

    targets = {
        'cpu': cpu.cpu, 
        'mem': mem.mem
    }

    try:
        while True:
            timestamp = int(time.time())
            pushJson = {}
            pushJson['endpoint']  = endpoint
            pushJson['step']      = nestInterval
            for tar in dict(targets).keys():
                pushJson['timestamp'] = int(time.time())
                items = targets.get(tar)()
                for key in dict(items).keys():
                    pushJson['item']  = key
                    pushJson['value'] = items[key]
                    params = urllib.parse.urlencode(pushJson).encode(encoding='utf8')
                    req = urllib.request.urlopen(url, params)
                    ret = json.loads(req.read())
                    if data['debug']:
                        debug(str(key),ret)
                    if not ret['res'] > 0:
                        log.lg_write_ant(" ==ant== target " + str(tar) + "." + str(key) + " push failed !")
            time.sleep(int(nestInterval / len(targets)))

    except Exception as e:
        log.lg_write_ant(" ==ant== " + str(e))

if __name__ == "__main__":
    ant()