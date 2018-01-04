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
        obj['cpu.user']        = int(cpuTarItems[1])
        obj['cpu.nice']        = int(cpuTarItems[2])
        obj['cpu.system']      = int(cpuTarItems[3])
        obj['cpu.idle']        = int(cpuTarItems[4])
        obj['cpu.iowait']      = int(cpuTarItems[5])
        obj['cpu.irq']         = int(cpuTarItems[6])
        obj['cpu.softirq']     = int(cpuTarItems[7])
        obj['cpu.stealstolen'] = int(cpuTarItems[8])
        obj['cpu.guest']       = int(cpuTarItems[9])

        f.close()

        return obj
    except Exception as e:
        log.lg_write_ant(" ==cpu.cpu== " + str(e))

def main():
    obj = cpu()
    print(obj)

if __name__ == "__main__":
    main()