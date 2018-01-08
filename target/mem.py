#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   collect mem related indicators
#   xianwen.zhang
#   2017-12-12

import os
import json
from smtants.ant.include import log

def mem():
    try:
        if not os.path.exists('/proc/meminfo'):
            log.lg_write(' ==mem== /proc/meminfo is not exists !')
            exit()
        
        f = open('/proc/meminfo', 'r', 1)
        meminfo = f.read().split('\n')

        memtotal  = 0
        memfree   = 0
        buffers   = 0
        cached    = 0
        memused   = 0
        swaptotal = 0
        swapfree  = 0
        swapused  = 0
        for value in meminfo:
            if value.find('MemTotal') > -1:
                memtotal = int(value.split()[1])
            elif value.find('MemFree') > -1:
                memfree = int(value.split()[1])
            elif value.find('Buffers') > -1:
                buffers = int(value.split()[1])
            elif value.find('Cached') > -1:
                cached = int(value.split()[1])
            elif value.find('SwapTotal') > -1:
                swaptotal = int(value.split()[1])
            elif value.find('SwapFree') > -1:
                swapfree = int(value.split()[1])
            
        obj = {}
        obj['mem.memtotal']  = memtotal
        obj['mem.memfree']   = memfree
        obj['mem.buffers']   = buffers
        obj['mem.cached']    = cached
        obj['mem.memused']   = memtotal - memfree - buffers - cached
        obj['mem.swaptotal'] = swaptotal
        obj['mem.swapfree']  = swapfree
        obj['mem.swapused']  = swaptotal - swapfree

        f.close()

        return obj
    except Exception as e:
        log.lg_write(' ==mem.mem== ' + str(e))

def main():
    obj = mem()
    print(obj)

if __name__ == "__main__":
    main()