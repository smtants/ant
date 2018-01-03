#! /usr/bin python
# -*- coding:utf-8 -*-
#
#   collect CPU related indicators
#   xianwen.zhang
#   2017-12-12

import os
import sys
import json
from smtants.ant.include import log

def cpu():
    try:
        if not os.path.exists('/proc/stat'):
            log.lg_write_ant(" ==cpu== /proc/stat is not exists !")
            exit()
        
        f = open('/proc/stat', 'r', 1)
        cpuTarItems = f.readline().split()

        obj = {}
        obj['cpu.user']        = cpuTarItems[1]
        obj['cpu.nice']        = cpuTarItems[2]
        obj['cpu.system']      = cpuTarItems[3]
        obj['cpu.idle']        = cpuTarItems[4]
        obj['cpu.iowait']      = cpuTarItems[5]
        obj['cpu.irq']         = cpuTarItems[6]
        obj['cpu.softirq']     = cpuTarItems[7]
        obj['cpu.stealstolen'] = cpuTarItems[8]
        obj['cpu.guest']       = cpuTarItems[9]

        f.close()

        return obj
    except Exception as e:
        log.lg_write_ant(" ==cpu.cpu== " + str(e))

def main():
    obj = cpu()
    print(obj)

if __name__ == "__main__":
    main()