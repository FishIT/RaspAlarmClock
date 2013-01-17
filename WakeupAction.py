#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import thread
import random
import os

class WakeupAction:
    active=False
    
    activelock = thread.allocate_lock()
    firelock = thread.allocate_lock()
    offlock = thread.allocate_lock()

    def fire(self):
        thread.start_new_thread(self._fire,())

    def snooze(self,delaytime=60*2):
        thread.start_new_thread(self._snooze, (delaytime,))

    def _snooze(self,delaytime=60*2):
        self.off()
        time.sleep(delaytime)
        self.fire()

    def off(self):
        thread.start_new_thread(self._off,())

class MP3Player(WakeupAction):
    from mpg123 import mpg123
    from fader import fader

    music_directory = ""
    random = True
    player = mpg123()
    fader = fader()
    music_list = []
    music_list_index = 0
    interval_to_check_if_player_is_playing = 0.1
    

    def __init__(self,music_directory, random = True):
        self.music_directory = music_directory
        self.random = random
        #1. read the files in the music dir
        for root, dirs, files in os.walk(self.music_directory):
            for singlefile in files:
                #2. filter them so that only mp3 files are used
                if singlefile.lower().endswith(".mp3"):
                    self.music_list.append(os.path.join(root, singlefile))
        #3. shuffle the files
        if self.random:
            self._shuffle_music_list()

    def _fire(self):
        self.firelock.acquire()
        self.activelock.acquire()
        self.active = True
        self.activelock.release()
        self.fader.set_volume(0)
        #4. iterate over list, play one song after the other
        while self.active:
            self.player.load(self.music_list[self.music_list_index])
            self.music_list_index += 1
            if self.music_list_index == len(self.music_list):
                self.music_list_index = 0
                if self.random:
                    self._shuffle_music_list()
            self.player.play()
            self.fader._fade_in()
            while self.player.is_playing():
                time.sleep(self.interval_to_check_if_player_is_playing)
        self.firelock.release()

    def _off(self):
        self.offlock.acquire()
        self.activelock.acquire()
        self.active = False
        self.activelock.release()
        # enable a fast fade out
        self.fader.set_fast()
        # use the blocking fade out
        self.fader._fade_out()
        self.player.stop()
        self.offlock.release()

    def _shuffle_music_list(self):
            random.shuffle(self.music_list)
