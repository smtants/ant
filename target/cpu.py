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
            log.lg_write(" ==cpu== /proc/stat is not exists !")
            exit()
        
        f = open('/proc/stat', 'r', 1)
        cpuTarItems = f.readline().split()

        obj = {}
        total = int(cpuTarItems[1]) + int(cpuTarItems[2]) + int(cpuTarItems[3]) + int(cpuTarItems[4]) + int(cpuTarItems[5]) + int(cpuTarItems[6]) + int(cpuTarItems[7]) + int(cpuTarItems[8]) + int(cpuTarItems[9])
        obj['cpu.user']        = round(int(cpuTarItems[1]) / total, 3)
        obj['cpu.nice']        = round(int(cpuTarItems[2]) / total, 3)
        obj['cpu.system']      = round(int(cpuTarItems[3]) / total, 3)
        obj['cpu.idle']        = round(int(cpuTarItems[4]) / total, 3)
        obj['cpu.iowait']      = round(int(cpuTarItems[5]) / total, 3)
        obj['cpu.irq']         = round(int(cpuTarItems[6]) / total, 3)
        obj['cpu.softirq']     = round(int(cpuTarItems[7]) / total, 3)
        obj['cpu.stealstolen'] = round(int(cpuTarItems[8]) / total, 3)
        obj['cpu.guest']       = round(int(cpuTarItems[9]) / total, 3)

        f.close()

        return obj
    except Exception as e:
        log.lg_write(" ==cpu.cpu== " + str(e))

def main():
    obj = cpu()
    print(obj)

if __name__ == "__main__":
    main()