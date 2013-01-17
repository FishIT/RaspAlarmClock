#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from WakeupAction import *
import time

version="0.1"


def set_alarm_time():
  alarm_time = raw_input('Bitte Weckzeit eingeben zwischen 00:00 und 23:59 : ')
  return alarm_time+":00"

def alarm_clock(alarm_time, wakeupaction, snoozeinterval):
    while True:
        if alarm_time == time.strftime("%H:%M:%S"):
            wakeupaction.fire()
            break
      
        print "\n"*20
        print "Current time is: {}".format(time.strftime("%H:%M:%S"))
        print "\nAlarm set for: {}".format(alarm_time)
        print "\n"*20      
        time.sleep(1)

    # enter the alarm-terminal
    on = True
    while on:
        answer = raw_input('Schreibe "STOP" um den Wecker zu deaktivieren: ')
        if (answer != "STOP"):
            print "Falsche Eingabe! Aktiviere Snooze!"
            wakeupaction.snooze(snoozeinterval)
            time.sleep(snoozeinterval)
        else:
            # maybe do some advanced stuff before switching off
            # eg. ask the user to solve a mathematic question
            wakeupaction.off()
            on = False
    print "Guten Morgen!"
            

def main():
    parser = OptionParser(usage="usage: %prog options", version="%prog "+version)
    parser.add_option("-d", "--musicDirectory", action="store", dest="musicdir",
                      help="Der Ordner mit der Weckmusik")
    parser.add_option("-t", "--wakeUpTime", action="store", dest="wakeuptime",
                      help="Die Weckzeit (z.B.: \"06:10:15\")")
    parser.add_option("-i", "--snoozeInterval", action="store", dest="snoozeinterval",
                      help="Das Snooze-Interval in Sekunden")

    (options, args) = parser.parse_args()
    
    if args or not options.musicdir or not options.wakeuptime or not options.snoozeinterval:
        parser.print_help()
        parser.exit(1, "Bitte alle Optionen angeben! STOP\n")

    try:
        snoozeInterval = int(options.snoozeinterval)
    except:
        parser.exit(1, "Snooze-Interval war keine gültige Zahl!\n")

    try:
        wakeupTime_dt = time.strptime(options.wakeuptime, '%H:%M:%S')
        wakeupTime = time.strftime("%H:%M:%S",wakeupTime_dt)
        #str(wakeupTime_dt.tm_hour)+":"+str(wakeupTime_dt.tm_min)+":"+str(wakeupTime_dt.tm_sec)

    except:
        parser.exit(1, "Angegebene Weckzeit war ungültig!\n\t Weckzeit-Format: \"HH:MM:SS\", z.B.:\"06:10:15\"\n")

    
    player = MP3Player(options.musicdir)
    alarm_clock(wakeupTime,player, snoozeInterval)

if __name__ == '__main__':
    main()
