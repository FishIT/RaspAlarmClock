#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import thread

class mpg123:
    """A wrapper class for mpg123"""
# mpg123 has a lot of features, for example random list playback (from filenames in a file)

# it can directly use web urls:
# mpg123 [ options ] file ... | URL ... | -

# an interesting option is pitch (maybe increase pitch with every snooze pressing?):
#       --pitch value
#              Set  hardware  pitch  (speedup/down,  0 is neutral; 0.05 is 5%).
#              This changes the output sampling rate, so it only works  in  the
#              range your audio system/hardware supports.

#       -d n, --doublespeed n
#              Only play every n'th frame.  This will cause the MPEG stream  to
#              be played n times faster, which can be used for special effects.
#              Can also be combined with the --halfspeed option to play  3  out
#              of  4  frames  etc.  Don't expect great sound quality when using
#              this option.

#       -h n, --halfspeed n
#              Play each frame n times.  This will cause the MPEG stream to  be
#              played  at  1/n'th speed (n times slower), which can be used for
#              special effects. Can also be  combined  with  the  --doublespeed
#              option  to  double every third frame or things like that.  Don't
#              expect great sound quality when using this option.

#      -E file, --equalizer
#              Enables equalization, taken from file.  The file needs  to  con‐
#              tain  32 lines of data, additional comment lines may be prefixed
#              with #.  Each data line consists of two floating-point  entries,
#              separated  by whitespace.  They specify the multipliers for left
#              and right channel of a  certain  frequency  band,  respectively.
#              The  first line corresponds to the lowest, the 32nd to the high‐
#              est frequency band.  Note that you  can  control  the  equalizer
#              interactively with the generic control interface.

#       -C, --control
#              Enable  terminal  control  keys. By default use 's' or the space
#              bar to stop/restart (pause, unpause) playback, 'f' to jump  for‐
#              ward  to the next song, 'b' to jump back to the beginning of the
#              song, ',' to rewind, '.' to fast forward, and 'q' to quit.  Type
#              'h' for a full list of available controls.

#       -R, --remote
#              Activate  generic  control interface.  mpg123 will then read and
#              execute commands from stdin. Basic usage is ``load <filename> ''
#              to  play some file and the obvious ``pause'', ``command.  ``jump
#              <frame>'' will jump/seek to a given point (MPEG  frame  number).
#              Issue ``help'' to get a full list of commands and syntax.

#       --aggressive
#              Tries to get higher priority

    command = "mpg123"
    bufsize = 1024
    soundfile = ""
    subprocess = None
    playing = False
#    stdout = None
#    stderr = None

    def load(self, soundfile):
        self.soundfile = soundfile

    def play(self):
        if (not self.playing):
            self.playing = True
            self.subprocess = Popen(args=self.soundfile, executable=self.command, shell=True, bufsize=self.bufsize, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=False)
            thread.start_new_thread(self._read_stdout,())
            thread.start_new_thread(self._read_stderr,())
            thread.start_new_thread(self._wait_until_the_end_of_the_track,())

    def stop(self):
        if self.playing:
            self.playing = False
            self.subprocess.terminate()

    def is_playing(self):
        return self.playing

    def _read_stderr(self):
        while self.playing:
            self.subprocess.stderr.read(1000)

    def _read_stdout(self):
        while self.playing:
            self.subprocess.stdout.read(1000)

    def _wait_until_the_end_of_the_track(self):
        self.subprocess.wait()
        self.playing = False

