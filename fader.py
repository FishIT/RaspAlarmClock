#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import time, thread

class fader:
    """A simple wrapper for amixer to fade in and out"""
    maximum = 65536
    steps = 100
    speed = 1000	#values from 1 to 10000
    actual_value = 0

    command = "amixer"
    action = "set"
    device = "Master"
    on = "unmute"
    to = ">"
    devnull = "/dev/null"

    bufsize = 1024
    subprocess = None
    lock = thread.allocate_lock()

    def _unmute(self):
        self.subprocess = Popen([self.command,self.action,self.device,self.on,self.to,self.devnull])
        self.subprocess.wait()

    def set_volume(self,level):
        self.lock.acquire()
        self.actual_value = level
        self._set_actual_value()
        self.lock.release()

    def _set_actual_volume(self):
        self.subprocess = Popen([self.command,self.action,self.device,str(self.actual_value),self.to,self.devnull])
        self.subprocess.wait()

    def set_slow(self):
        self.lock.acquire()
        self.steps = 100
        self.speed = 1000
        self.lock.release()

    def set_fast(self):
        self.lock.acquire()
        self.steps = 10
        self.speed = 10000
        self.lock.release()

    def fade_in(self):
        thread.start_new_thread(self._fade_in,())

    def _fade_in(self):
        self.lock.acquire()
        self._unmute()
        while self.actual_value < self.maximum:
            self.actual_value += self.maximum/self.steps
            if (self.actual_value > self.maximum):
                self.actual_value = self.maximum
            self._set_actual_volume()
            time.sleep(10/self.speed)
        self.lock.release()

    def fade_out(self):
        thread.start_new_thread(self._fade_out,())

    def _fade_out(self):
        self.lock.acquire()
        while self.actual_value > 0:
            self.actual_value -= self.maximum/self.steps
            if (self.actual_value < 0):
                self.actual_value = 0
            self._set_actual_volume()
            time.sleep(10/self.speed)
        self.lock.release()

