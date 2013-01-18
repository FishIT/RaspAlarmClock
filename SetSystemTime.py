#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import time
import subprocess
import datetime

# TODO: Extend to add optional date setting


version="0.1"
            

def main():
    parser = OptionParser(usage="usage: %prog options", version="%prog "+version)
    parser.add_option("-t", "--systemTime", action="store", dest="systemtime",
                      help="Die Zeit, auf die die System-Uhr eingestellt werden soll (z.B.: \"06:10:15\")")

    (options, args) = parser.parse_args()
    
    if args or not options.systemtime:
        parser.print_help()
        parser.exit(1, "Bitte neue System-Uhrzeit angeben! STOP\n")

    try:
        systemTime_dt = time.strptime(options.systemtime, '%H:%M:%S')
        systemTime = time.strftime("%H:%M:%S",systemTime_dt)
        #str(wakeupTime_dt.tm_hour)+":"+str(wakeupTime_dt.tm_min)+":"+str(wakeupTime_dt.tm_sec)

    except:
        parser.exit(1, "Angegebene Uhrzeit war ungültig!\n\t Uhrzeit-Format: \"HH:MM:SS\", z.B.:\"06:10:15\"\n")

    date = datetime.date.today() 
    #datetime.date.today().strftime("%Y-%m-%d")
    process = subprocess.call("sudo date -s \"@$(date --date=\""+date.strftime("%Y-%m-%d")+" "+systemTime+"\" +%s)\"", shell=True)
    #process.wait()

if __name__ == '__main__':
    main()
